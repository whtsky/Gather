# -*- coding:utf-8 -*-

from flask import Blueprint, abort, jsonify
from flask import request, g
from flask.ext.classy import FlaskView, route
from gather.account.forms import LoginForm, RegisterForm, SettingsForm
from gather.account.models import Account
from gather.node.models import Node
from gather.topic.forms import CreateTopicForm, ReplyForm
from gather.topic.models import Topic


bp = Blueprint("api", __name__, url_prefix="/api")


class GatherAPIView(FlaskView):
    def before_request(self, name, *args, **kwargs):
        if g.user is not None:
            if name in ("post", "put"):
                return abort(403)
        else:
            token = request.values.get("token", None)
            if token:
                user = Account.query.filter_by(api_token=token).first()
                if not user:
                    return jsonify(
                        error="Wrong Token"
                    )
                g.user = user


class GatherModelView(GatherAPIView):
    model = None
    model_name = ""

    def __init__(self):
        if not self.model_name:
            self.model_name = self.model.__name__.lower()
        self.model_name_s = self.model_name + "s"

    def index(self):
        page = int(request.values.get("page", 1))
        Model = self.model
        models = Model.query.order_by(Model.id.desc())
        paginator = models.paginate(page=page)
        return jsonify({
            'page': page,
            'total': paginator.total,
            'total_page': paginator.pages,
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
        form = SettingsForm(obj=user)
        if form.validate_on_submit():
            form.save()
            return jsonify(
                msg="Settins updated"
            )
        return jsonify(
            error=form.errors.values()[0]
        )

    @route("/authorize/", methods=["POST"])
    def authorize(self):
        form = LoginForm()
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

    def post(self):
        form = CreateTopicForm()
        if form.validate_on_submit():
            topic = form.create()
            return jsonify(
                msg="Created topic",
                topic=topic.to_dict()
            )
        return jsonify(
            error=form.errors.values()[0]
        )

TopicView.register(bp)


class NodeView(GatherModelView):
    model = Node

NodeView.register(bp)


class ReplyView(GatherModelView):
    def post(self):
        form = ReplyForm()
        if form.validate_on_submit():
            topic = form.create()
            return jsonify(
                msg="Created reply",
                reply=reply.to_dict()
            )
        return jsonify(
            error=form.errors.values()[0]
        )

ReplyView.register(bp)
