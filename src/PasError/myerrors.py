
class BaseError(BaseException):
    def __init__(self,_args):
        super().__init__(_args)

class SyntxError(BaseError):
    def __init__(self,_args):
        super().__init__(_args)


