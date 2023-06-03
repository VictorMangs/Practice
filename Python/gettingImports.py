import ast
import pkg_resources
from pipreqs import pipreqs


def get_requirements(script_path):
    # Generate requirements file using pipreqs
    requirements = pipreqs.get_all_imports('/'.join(script_path.split('/')[0:-1]))
    # Parse the requirements file
    #with open(requirements_file, "r") as file:
    #    requirements = [line.strip() for line in file]

    # Parse the AST of the script
    with open(script_path, "r") as file:
        tree = ast.parse(file.read())

    # Extract additional requirements from the AST
    additional_requirements = extract_additional_requirements(tree)

    # Combine requirements from the requirements file and additional analysis
    all_requirements = set(requirements + additional_requirements)

    # Retrieve package versions
    requirements_with_versions = get_package_versions(all_requirements)

    return requirements_with_versions


def extract_additional_requirements(tree):
    additional_requirements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                additional_requirements.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module if node.module is not None else ""
            for alias in node.names:
                additional_requirements.append(f"{module_name}")
    return additional_requirements

def get_package_versions(requirements):
    versions = {}
    for requirement in requirements:
        try:
            version = pkg_resources.get_distribution(requirement).version
            versions[requirement] = version
        except pkg_resources.DistributionNotFound:
            versions[requirement] = "Not Found"
    return versions


# Example usage
script_path = "./Python/getImports/mp3_mp4_converter.py"
requirements = get_requirements(script_path)

print("Requirements:")
for requirement, version in requirements.items():
    print(f"{requirement}=={version}")