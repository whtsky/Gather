from handlers import account, member, node, topic

__all__ = ['handlers', 'ui_modules']

handlers = []
handlers.extend(account.handlers)
handlers.extend(member.handlers)
handlers.extend(node.handlers)
handlers.extend(topic.handlers)

ui_modules = {}
ui_modules.update(**node.ui_modules)
ui_modules.update(**topic.ui_modules)
