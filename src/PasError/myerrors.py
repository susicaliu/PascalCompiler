# class BaseError(BaseException):
#     def __init__(self,_args):
#         super().__init__(_args)

# class TokenError(BaseError):
#     def __init__(self,_args):
#         super().__init__(_args)
# class SyntxError(BaseError):
#     def __init__(self,_args):
#         super().__init__(_args)

# class TypError(BaseError):
#     def __init__(self,_args):
#         super().__init__(_args)

# class DefineError(BaseError):
#     def __init__(self,_args):
#         super().__init__(_args)

f_er = open('errors_log.txt', 'w')
class BaseError(object):
    def __init__(self, name, lineno = -1, colno = -1):
        super().__init__()
        self.name = name
        self.lineno = lineno
        self.colno = colno
        self.error_type = 'Base'

    def log(self):
        f_er.write("%s error: %s at line %d, col %d." % (self.error_type, self.name, self.lineno, self.colno))

class TokenError(BaseError):
    def __init__(self, name, lineno = -1, colno = -1):
        super().__init__(name, lineno, colno)
        self.error_type = 'Token'
        
class SyntxError(BaseError):
    def __init__(self, name, lineno = -1, colno = -1):
        super().__init__(name, lineno, colno)
        self.error_type = 'Syntax'

class TypError(BaseError):
    def __init__(self, name, lineno = -1, colno = -1):
        super().__init__(name, lineno, colno)
        self.error_type = 'Type'

class DefineError(BaseError):
    def __init__(self, name, lineno = -1, colno = -1):
        super().__init__(name, lineno, colno)
        self.error_type = 'Define'