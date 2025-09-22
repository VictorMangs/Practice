# To do list

# Arguments (num and item to modify/view)

# Functions/Methods 
# Add,remove,view,complete

import sys

def usage():
    print(f"Run 'python {sys.argv[0]} add' to add todo items")
    print(f"Run 'python {sys.argv[0]} view' to view todo items")
    print(f"Run 'python {sys.argv[0]} remove' to remove todo items")

def add_todo():
    task = input("Please enter task to add: ")
    with open("todo_list.txt","a") as file:
        file.write(task)
        file.write("\n")

def view_todo():
    try:
        with open("todo_list.txt","r") as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error:{e}")
        sys.exit("Error reading file, please try again.")

def remove_todo():
    task = input("Please enter task to remove: ")
    if task:
        content = view_todo().split("\n")
        new_content = [item for item in content if item.lower() != task.lower()]
        print(new_content)
        with open("todo_list.txt","w") as file:
            file.writelines(new_content)
    else:
        print("Empty tasks cannot be deleted!")

arg_len = len(sys.argv)
if arg_len <2:
    print("No arguments provided")
    usage()
else:
    item = None
    if arg_len>3: print("Ignoring extraneous arguments")
    if arg_len>2: item = sys.argv[2]
    match sys.argv[1]:
        case "view":
            if arg_len>2: print("Ignoring extraneous arguments")
            print(view_todo())
        case "remove":
            remove_todo()
        case "add":
            add_todo()
        case _:
            print("Error parsing arguments, please see usage below.")
            usage()

