# -*- coding:utf-8 -*-

from flask import g, jsonify, request
from gather.account.models import Account
from gather.api import need_auth, EXCLUDE_COLUMNS
from gather.extensions import api_manager


__all__ = ["bp"]


def patch_single_preprocessor(instance_id=None, data=None, **kw):
    """Accepts two arguments, `instance_id`, the primary key of the
    instance of the model to patch, and `data`, the dictionary of fields
    to change on the instance.

    """
    return g.token_user.id == instance_id


# 需要一点小 hack ..
bp = api_manager.create_api_blueprint(
    Account,
    methods=["GET", "PUT"],
    preprocessors=dict(PUT_SINGLE=[need_auth, patch_single_preprocessor],),
    exclude_columns=EXCLUDE_COLUMNS
)


@bp.route("/account/authorize/", methods=["POST"])
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


@bp.route("/account/change_password/", methods=["POST"])
def _change_password():
    new_password = request.form["password"]
    user = Account.query.filter_by(username="Madimo").first_or_404()
    user.change_password(new_password)
    user.save
    return jsonify(
        code=200,
        user=user
    )
