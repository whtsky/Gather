from handlers import account, member, node, topic, dashboard, others, api

__all__ = ['handlers', 'ui_modules']

handlers = []
handlers.extend(account.handlers)
handlers.extend(member.handlers)
handlers.extend(node.handlers)
handlers.extend(topic.handlers)
handlers.extend(dashboard.handlers)
handlers.extend(others.handlers)
handlers.extend(api.handlers)

ui_modules = {}
ui_modules.update(**node.ui_modules)
ui_modules.update(**topic.ui_modules)
