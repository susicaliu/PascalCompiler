import llvmlite.ir as ir
class GenTable(object):
    def __init__(self):
        self.variable_table = {}
        self.record_table = {}
        self.type_table = {}
        self.func_table = {}

        self.variable_scope = {}
        self.type_scope = {}
        self.func_scope = {}

    def add_variable(self, variable_name, address, variable_type, scope_id):
        self.variable_table.setdefault(variable_name, []).append((address, variable_type))
        self.variable_scope.setdefault(scope_id, []).append(variable_name)

    def add_type(self, variable_name, variable_type, scope_id):
        self.type_table.setdefault(variable_name, []).append(variable_type)
        self.type_scope.setdefault(scope_id, []).append(variable_name)

    def add_function(self, func_name, func_block, scope_id):
        self.func_table.setdefault(func_name, []).append(func_block)
        self.func_scope.setdefault(scope_id, []).append(func_name)

    def add_record_variable(self, key_name, variable_name, address, variable_type):
        self.variable_table.setdefault(key_name, {}).setdefault(variable_name, []).append((address, variable_type))

    def get_type(self, type_name):
        res = self.type_table.get(type_name)
        if (res is not None):
            res = res[-1]
        else:
            raise Exception("Error: {0} is not exist!".format(type_name))
        return res

    def get_record_variable_addr(self, name, name2):
        res = self.variable_table.get(name)
        if (res is not None):
            res = res[-1].get(name2)
            if (res is not None):
                res = res[-1][0]
            else:
                raise Exception("Error: {0} is not exist!".format(name2))
        else:
            raise Exception("Error: {0} is not exist!".format(name))
        return res

    def get_record_variable_addr_type(self, name, name2):
        res = self.variable_table.get(name)
        if (res is not None):
            res = res[-1].get(name2)
            if (res is not None):
                return res[-1][0], res[-1][1]
            else:
                raise Exception("Error: {0} is not exist!".format(name2))

        else:
            raise Exception("Error: {0} is not exist!".format(name))


    def get_variable_addr_type(self, name):
        res = self.variable_table.get(name)
        if (res is not None):
            return res[-1][0], res[-1][1]
        else:
            raise Exception("Error: {0} is not exist!".format(name))

    def get_func(self, name):
        res = self.func_table.get(name)
        if (res is not None):
            res = res[-1]
        else:
            raise Exception("Error: {0} is not exist!".format(name))
        return res

    def get_variable_addr(self, name):
        res = self.variable_table.get(name)
        if (res is not None):
            return res[-1][0]
        else:
            raise Exception("Error: {0} is not exist!".format(name))

    def get_address(self, _id):
        res = self.get_variable_addr(_id)
        return res


    def delete_scope(self, scope_id):
        for name in self.variable_scope.get(scope_id, []):
            res = self.variable_table.get(name)
            if (res is not None):
                del res[-1]
            else:
                raise Exception("Error: {0} is not exist!".format(name))
        del self.variable_scope[scope_id]
        scope_id += 1
        for name in self.func_scope.get(scope_id, []):
            res = self.func_table.get(name)
            if (res is not None):
                del res[-1]
            else:
                raise Exception("Error: {0} is not exist!".format(name))
        if scope_id in self.func_scope:
            del self.func_scope[scope_id]

    def type_convert(self, type):
        if (isinstance(type, ir.Type)):
            return type
        if (type in ['integer', 'int']):
            return ir.IntType(32)
        if (type in ['real']):
            return ir.DoubleType()
        if (type in ['boolean']):
            return ir.IntType(1)
        if (type in ['void']):
            return ir.VoidType()
        if (type in ['char']):
            return ir.IntType(8)
        raise Exception('Error: invalid data type')