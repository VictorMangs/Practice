import ast

class astVisitor(ast.NodeVisitor):
    def visit_Module(self, node:ast.AST):
        self.generic_visit(node)
    
    def visit_Import(self, node:ast.AST):
        for imp in node.names:
            print('Import : '+imp.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node:ast.AST):
        print('From: '+node.module,end=' importing ')
        print(','.join([item.name for item in node.names]))
        self.generic_visit(node)

    def visit_ClassDef(self, node:ast.AST):
        print('Class: '+node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node:ast.AST):
        print('\t Function: '+node.name)
        self.generic_visit(node)

    def visit_arg(self, node:ast.AST):
        print('\t Argument: '+node.arg)
        self.generic_visit(node)

def main(scriptName):

    script = open(scriptName).read()
    node = ast.parse(script)
    
    astVisitor().visit_Module(node)

if __name__=='__main__':
    script = 'YamlTkinter.py'
    main(script)