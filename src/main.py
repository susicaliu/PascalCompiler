from PasParser.parser import parser
from PasGenerator.codegenerator import *
import llvmlite.binding as llvm
import argparse
arg = argparse.ArgumentParser()
arg.add_argument("--input_file", help='specify the input file',default='test_case/test_for.pas',required=False)
arg.add_argument( "--opt_level",
                        type=int, help="specify the optimization level",default=1,required=False)
if __name__ == '__main__':
    args=arg.parse_args()
    # All these initializations are required for code generation!
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()  # yes, even this one

    codestr = open(args.input_file, 'r').read()
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
    llvmmod = llvm.parse_assembly(llvm_ir)
    if args.opt_level:
        level = args.opt_level
        if level > 0:
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = level
            pm = llvm.create_module_pass_manager()
            pmb.populate(pm)
            pm.run(llvmmod)
            llvm_ir = str(llvmmod)

    print("====================IR====================")
    f_ir = open('ir_code.txt', 'w')
    f_ir.write(llvm_ir)
    print("====================IR====================")


    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    asm = target_machine.emit_assembly(llvmmod)

    print("====================X86====================")
    f_asm = open('asm_code.s', 'w')
    f_asm.write(asm)
    print("====================X86====================")

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    obj = target_machine.emit_object(llvmmod)
    print("====================OBJ====================")
    f_obj = open("obj_code.obj", "wb")
    f_obj.write(obj)
    print("====================OBJ====================")

    
    print("====================MCJLT====================")
    jlt = llvm.create_mcjit_compiler(llvmmod, target_machine)
    
    print("====================MCJLT====================")