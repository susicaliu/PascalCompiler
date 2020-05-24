from PasParser.parser import parser
from PasGenerator.codegenerator import *
import llvmlite.binding as llvm

if __name__ == '__main__':
    # All these initializations are required for code generation!
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()  # yes, even this one

    codestr = open('test.pas', 'r').read()
    ast = parser.parse(codestr)

    print("====================AST====================")
    print(ast)
    print("====================AST====================")

    visible = True
    if visible:
        f = open('parsetree.dot', 'w')
        f.write('digraph g {\n')
        ast.vis(f)
        f.write('}\n')
        f.close()
        os.system('dot -Tpng parsetree.dot -o parsetree.png')
    else:
        ast.travle()

    codegen = CodeGenerator('Test')
    codegen.generate(ast)
    llvm_ir = str(codegen.module)

    print("====================IR====================")
    f_ir = open('ir_code.txt', 'w')
    f_ir.write(llvm_ir)
    print(llvm_ir)
    print("====================IR====================")

    llvmmod = llvm.parse_assembly(llvm_ir)
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    asm = target_machine.emit_assembly(llvmmod)

    print("====================X86====================")
    f_asm = open('asm_code.txt', 'w')
    f_asm.write(asm)
    print(asm)
    print("====================X86====================")
