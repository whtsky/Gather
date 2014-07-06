# -*- coding:utf-8 -*-
from flask import g, jsonify

from gather.api import need_auth, EXCLUDE_COLUMNS

from gather.extensions import api_manager
from gather.topic.models import Topic, Reply


bp = api_manager.create_api_blueprint(
    Topic,
    methods=["GET", "POST"],
    preprocessors={
        'POST': [need_auth],
    },
    include_methods=["have_read"],
    exclude_columns=EXCLUDE_COLUMNS
)


@bp.route("/topic/<int:topic_id>/mark_read")
def _mark_read_for_topic(topic_id):
    need_auth()
    topic = Topic.query.get_or_404(topic_id)
    topic.mark_read(g.token_user)
    return jsonify({"code": 200})


def _update_topic_updated(result=None, **kw):
    if not result:
        return
    reply = Reply.query.get(result["id"])
    reply.topic.updated = reply.created
    reply.topic.clear_read()
    reply.topic.save()


reply_bp = api_manager.create_api_blueprint(
    Reply,
    methods=["POST"],
    preprocessors={
        'POST': [need_auth],
    },
    postprocessors={
        'POST': [_update_topic_updated]
    },
    exclude_columns=EXCLUDE_COLUMNS
)
