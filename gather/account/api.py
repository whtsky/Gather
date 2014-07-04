# -*- coding:utf-8 -*-

from flask import request, jsonify
from gather.account.models import Account
from gather.extensions import api_manager


__all__ = ["bp"]


def patch_single_preprocessor(instance_id=None, data=None, **kw):
    """Accepts two arguments, `instance_id`, the primary key of the
    instance of the model to patch, and `data`, the dictionary of fields
    to change on the instance.

    """
    token = request.headers.get("token", None)
    user = Account.query.filter_by(api_token=token).first()
    return user and user.id == instance_id


# 需要一点小 hack ..
bp = api_manager.create_api_blueprint(
    Account,
    methods=["GET", "PUT"],
    preprocessors=dict(PUT_SINGLE=[patch_single_preprocessor],),
    include_columns=["created", "css", "description", "email", "feeling_lucky", "id", "role", "username", "website"],
)


@bp.route("/authorize/", methods=["POST"])
def _account_authorize():
    from .forms import LoginForm
    form = LoginForm()
    if not form.validate_on_submit():
        return jsonify(
            code=400,
            msg="Wrong username/password"
        )
    user = form.user
    if not user.api_token:
        user.generate_api_token()
    return jsonify(
        code=200,
        token=user.api_token
    )
