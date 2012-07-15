from handlers import auth

__all__ = ['handlers', 'ui_modules']

handlers = []
handlers.extend(auth.handlers)

ui_modules = {}
