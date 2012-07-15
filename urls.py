from handlers import account, member, node, post

__all__ = ['handlers', 'ui_modules']

handlers = []
handlers.extend(account.handlers)
handlers.extend(member.handlers)
handlers.extend(node.handlers)
handlers.extend(post.handlers)

ui_modules = {}
