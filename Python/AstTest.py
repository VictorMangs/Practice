import ast


def extract_functions(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    functions = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            parameters = [arg.arg for arg in node.args.args]
            functions.append({"name": node.name, "parameters": parameters})
        elif isinstance(node, ast.ClassDef):
            for class_node in ast.iter_child_nodes(node):
                if isinstance(class_node, ast.FunctionDef):
                    parameters = [arg.arg for arg in class_node.args.args if arg.arg!='self']
                    function_name = f"{node.name}.{class_node.name}"
                    functions.append({"name": function_name, "parameters": parameters})

    return functions


if __name__ == '__main__':
    script_path = './Python/tkinter_memory.py'
    extracted_functions = extract_functions(script_path)
    used = []
    with open('./Python/tkinter_memory.md', 'w') as file:
        file.write("# Extracted Functions:\n\n")
        for func in extracted_functions:
            if '.' in func['name']:
                if func['name'].split('.')[0] in used:
                    file.write(f">### Function: {func['name'].split('.')[1]}\n")
                else:
                    file.write(f"## Class: {func['name'].split('.')[0]}\n")
                    file.write(f">### Function: {func['name'].split('.')[1]}\n")
                    used.append(func['name'].split('.')[0])
            else:
                file.write(f"## Function: {func['name']}\n\n")
            if len(func["parameters"])>0:
                file.write(f">&emsp; **_Parameters:_** {', '.join(func['parameters'])}\n\n")
            else:
                file.write("\n\n")