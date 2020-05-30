f_wa = open('warning_logs.txt', 'w')
class BaseWarning(object):
    def __init__(self, name, lineno = -1, colno = -1):
        super().__init__()
        self.name = name
        self.lineno = lineno
        self.colno = colno
        self.warning_type = 'Base'

    def log(self):
        f_wa.write("%s warning: %s at line %d, col %d." % (self.warning_type, self.name, self.lineno, self.colno))

class TypeWaring(BaseWarning):
    def __init__(self, name, lineno = -1, colno = -1):
        super().__init__(name, lineno, colno)