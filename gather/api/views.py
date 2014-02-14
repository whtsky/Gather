# -*- coding:utf-8 -*-

from flask import Blueprint, abort, jsonify
from flask import request, url_for, g
from flask.ext.classy import FlaskView, route
from gather.utils import get_page
from gather.account.forms import LoginForm, RegisterForm, SettingsForm
from gather.account.models import Account
from gather.node.models import Node
from gather.topic.models import Topic


bp = Blueprint("api", __name__, url_prefix="/api")


class GatherAPIView(FlaskView):
    def before_request(self, *args, **kwargs):
        if not g.user:
            token = request.args.get("token", None)
            if token:
                user = Account.query.get(api_token=token)
                g.user = user


class GatherModelView(FlaskView):
    model = None
    model_name = ""

    def __init__(self):
        if not self.model_name:
            self.model_name = self.model.__name__.lower()
        self.model_name_s = self.model_name + "s"

    def index(self):
        page = get_page()
        Model = self.model
        models = Model.query.order_by(Model.id.desc())
        paginator = models.paginate(page=page)
        return jsonify({
            'page': page,
            'total': paginator.total,
            self.model_name_s: [m.to_dict() for m in paginator.items]}
        )

    def get(self, id):
        m = self.model.query.get_or_404(id)
        return jsonify({
            self.model_name: m.to_dict()
        })


class UserView(GatherModelView):
    model = Account
    model_name = "user"

    def put(self, id):
        user = Account.query.get_or_404(id)
        if g.user != user:
            return abort(403)
        # TODO: Support Put

    def post(self):
        # TODO: Support Post
        pass

    @route("/authorize/", methods=["POST"])
    def authorize(self):
        form = LoginForm()
        form.csrf_enabled = False
        if not form.validate_on_submit():
            return jsonify(
                token="",
                msg="Wrong username/password"
            )
        user = form.user
        if not user.api_token:
            user.generate_api_token()
        return jsonify(
            token=user.api_token
        )


UserView.register(bp)


class TopicView(GatherModelView):
    model = Topic

TopicView.register(bp)


class NodeView(GatherModelView):
    model = Node


class ReplyView(GatherModelView):
    pass
