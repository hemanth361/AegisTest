import ast
import random
from typing import List, Dict, Union, Optional, Set, Tuple

def parse_function_definition(code):
    """
    Parses Python code to extract function definitions, names, and parameters.

    Args:
        code: Python code as a string.

    Returns:
        tuple: A tuple containing the function name and a list of parameters,
               where each parameter is a dictionary with 'name' and 'type' keys.
               Returns (None, None) if no function definition is found or an error occurs.
    """
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                parameters = []

                for arg, default in zip(
                        node.args.args,
                        [None] * (len(node.args.args) - len(node.args.defaults)) + node.args.defaults,
                ):
                    parameter_name = arg.arg
                    if arg.annotation:
                        if isinstance(arg.annotation, ast.Subscript):
                            # Handle complex types like list[int], dict[str, int]
                            base_type = arg.annotation.value.id if isinstance(arg.annotation.value, ast.Name) else "any"
                            if isinstance(arg.annotation.slice, ast.Index):
                                sub_type = arg.annotation.slice.value.id if isinstance(arg.annotation.slice.value, ast.Name) else "any"
                                data_type = f"{base_type}[{sub_type}]"
                            elif isinstance(arg.annotation.slice, ast.Tuple):
                                sub_types = [
                                    elt.id if isinstance(elt, ast.Name) else "any"
                                    for elt in arg.annotation.slice.elts
                                ]
                                data_type = f"{base_type}[{', '.join(sub_types)}]"
                            else:
                                data_type = base_type
                        else:
                            # Handle simple types
                            data_type = arg.annotation.id if isinstance(arg.annotation, ast.Name) else "any"
                    else:
                        data_type = "any"

                    # Mark parameter as Optional if it has a default value
                    if default is not None:
                        data_type = f"Optional[{data_type}]"

                    parameters.append({"name": parameter_name, "type": data_type})
                return function_name, parameters
    except SyntaxError as e:
        print(f"Syntax error in code: {e}")
        return None, None

def generate_test_inputs(parameters: List[Dict[str, str]], num_tests=10,
                         int_range=(-100, 100), float_range=(-10.0, 10.0),
                         string_length=10) -> List[Dict[str, Union[int, float, str, bool, List, Dict, Set, Tuple, None]]]:
    """
    Generates random test inputs for given function parameters, incorporating boundary value analysis, equivalence partitioning,
    and support for various data types.

    Args:
        parameters: A list of dictionaries, where each dictionary represents a parameter
                    with 'name' and 'type' keys.
        num_tests: The number of test inputs to generate.
        int_range: A tuple representing the minimum and maximum values for integer parameters.
        float_range: A tuple representing the minimum and maximum values for float parameters.
        string_length: The desired length of randomly generated strings.

    Returns:
        list: A list of dictionaries, where each dictionary represents a set of
             test inputs for the function.
    """
    test_inputs = []
    for _ in range(num_tests):  # Generate specified number of test inputs
        inputs = {}
        for param in parameters:
            param_type = param["type"]
            if param_type == "int":
                # Boundary value analysis and equivalence partitioning for integers
                inputs[param["name"]] = random.choice([
                    int_range[0],  # Minimum boundary
                    int_range[0] + (int_range[1] - int_range[0]) // 4,  # Below zero
                    0,    # Zero
                    int_range[1] - (int_range[1] - int_range[0]) // 4,  # Above zero
                    int_range[1],   # Maximum boundary
                    random.randint(int_range[0], int_range[0] + (int_range[1] - int_range[0]) // 2),  # Below zero range
                    random.randint(int_range[1] // 2, int_range[1]),      # Above zero range
                ])
            elif param_type == "float":
                # Boundary value analysis and equivalence partitioning for floats
                inputs[param["name"]] = random.choice([
                    float(int_range[0]),  # Minimum boundary
                    float(int_range[0]) + (float(int_range[1]) - float(int_range[0])) / 4,  # Below zero
                    0.0,    # Zero
                    float(int_range[1]) - (float(int_range[1]) - float(int_range[0])) / 4,  # Above zero
                    float(int_range[1]),   # Maximum boundary
                    random.uniform(float(int_range[0]), float(int_range[0]) + (float(int_range[1]) - float(int_range[0])) / 2),  # Below zero range
                    random.uniform(float(int_range[1]) / 2, float(int_range[1])),      # Above zero range
                ])
            elif param_type == "str":
                # Equivalence partitioning for strings
                inputs[param["name"]] = random.choice([
                    "",        # Empty string
                    "a",       # Single character
                    "hello",   # Short string
                    "This is a longer string.",  # Long string
                    "special_characters!@#$%^&*()",  # Special characters
                    ''.join(random.choices(string.ascii_letters, k=string_length)),  # Random string
                ])
            elif param_type == "bool":
                inputs[param["name"]] = random.choice([True, False])
            elif param_type.startswith("list"):
                base_type = param_type[5:-1]  # Extract base type from list[type]
                if base_type == "int":
                    inputs[param["name"]] = [random.randint(0, 10) for _ in range(5)]
                elif base_type == "str":
                    inputs[param["name"]] = [''.join(random.choices(string.ascii_letters, k=5)) for _ in range(3)]
                elif base_type == "float":
                    inputs[param["name"]] = [random.uniform(0.0, 10.0) for _ in range(3)]
                elif base_type == "bool":
                    inputs[param["name"]] = [random.choice([True, False]) for _ in range(3)]
                else:
                    inputs[param["name"]] = [0] * 5  # Default for unknown list types
            elif param_type.startswith("dict"):
                base_type = param_type[5:-1]  # Extract base type from dict[key_type, value_type]
                if base_type == "str, int":
                    inputs[param["name"]] = {"key1": 1, "key2": 2}
                else:
                    inputs[param["name"]] = {}  # Default for unknown dict types
            elif param_type.startswith("set"):
                base_type = param_type[4:-1]  # Extract base type from set[type]
                if base_type == "int":
                    inputs[param["name"]] = set(random.randint(0, 10) for _ in range(5))
                elif base_type == "str":
                    inputs[param["name"]] = set([''.join(random.choices(string.ascii_letters, k=5)) for _ in range(3)])
                else:
                    inputs[param["name"]] = set()  # Default for unknown set types
            elif param_type.startswith("tuple"):
                base_type = param_type[5:-1]  # Extract base type from tuple[type]
                if base_type == "int":
                    inputs[param["name"]] = tuple(random.randint(0, 10) for _ in range(3))
                elif base_type == "str":
                    inputs[param["name"]] = tuple([''.join(random.choices(string.ascii_letters, k=5)) for _ in range(3)])
                elif base_type == "float":
                    inputs[param["name"]] = tuple(random.uniform(0.0, 10.0) for _ in range(3))
                else:
                    inputs[param["name"]] = tuple([0] * 3)  # Default for unknown tuple types
            elif param_type.startswith("Optional"):
                base_type = param_type[9:-1]  # Extract base type from Optional[type]
                if random.choice([True, False]):  # 50% chance of being None
                    inputs[param["name"]] = None
                else:
                    if base_type == "int":
                        inputs[param["name"]] = random.randint(int_range[0], int_range[1])
                    elif base_type == "float":
                        inputs[param["name"]] = random.uniform(float_range[0], float_range[1])
                    elif base_type == "str":
                        inputs[param["name"]] = ''.join(random.choices(string.ascii_letters, k=string_length))
                    else:
                        inputs[param["name"]] = 0  # Default for unknown optional types
            else:
                inputs[param["name"]] = 0  # Default for unknown types
                test_inputs.append(inputs)
                return test_inputs