"""
This module contains unit tests for the core functionality of the Aegis Test project,
specifically the `parse_function_definition` and `generate_test_inputs` functions.
"""

import pytest
from app.utils import parse_function_definition, generate_test_inputs  # Import the functions from utils.py

def test_parse_function_definition():
    """Test with a simple function"""
    code = """
    def my_function(x: int, y: float):
        return x + y
    """
    function_name, parameters = parse_function_definition(code)
    assert function_name == "my_function"
    assert parameters == [{"name": "x", "type": "int"}, {"name": "y", "type": "float"}]

    # Test with a function without type hints
    code = """
    def add(a, b):
        return a + b
    """
    function_name, parameters = parse_function_definition(code)
    assert function_name == "add"
    assert parameters == [{"name": "a", "type": "any"}, {"name": "b", "type": "any"}]

    # Test with optional parameters
    code = """
    def greet(name: str, greeting: str = "Hello"):
        return f"{greeting}, {name}!"
    """
    function_name, parameters = parse_function_definition(code)
    assert function_name == "greet"
    assert parameters == [{"name": "name", "type": "str"}, {"name": "greeting", "type": "Optional[str]"}]

    # Test with invalid code
    code = "invalid code"
    function_name, parameters = parse_function_definition(code)
    assert function_name is None and parameters is None

    # Test with list type annotations
    code = """
    def process_numbers(numbers: list[int]):
        return sum(numbers)
    """
    function_name, parameters = parse_function_definition(code)
    assert function_name == "process_numbers"
    assert parameters == [{"name": "numbers", "type": "list[int]"}]

    # Test with dict type annotations
    code = """
    def update_inventory(item: str, quantity: dict[str, int]):
        return quantity.get(item, 0) + 1
    """
    function_name, parameters = parse_function_definition(code)
    assert function_name == "update_inventory"
    assert parameters == [{"name": "item", "type": "str"}, {"name": "quantity", "type": "dict[str, int]"}]

def test_generate_test_inputs():
    """Test with basic parameters"""
    parameters = [{"name": "x", "type": "int"}, {"name": "y", "type": "float"}]
    test_inputs = generate_test_inputs(parameters)
    assert len(test_inputs) == 10

    for inputs in test_inputs:
        assert "x" in inputs and "y" in inputs
        assert isinstance(inputs["x"], int)
        assert isinstance(inputs["y"], float)

    """Test with optional parameters"""
    parameters = [{"name": "x", "type": "int"}, {"name": "y", "type": "Optional[str]"}]
    test_inputs = generate_test_inputs(parameters)
    assert len(test_inputs) == 10

    for inputs in test_inputs:
        assert "x" in inputs and "y" in inputs
        assert isinstance(inputs["x"], int)
        assert inputs["y"] is None or isinstance(inputs["y"], str)

    """Test with list parameters"""
    parameters = [{"name": "numbers", "type": "list[int]"}]
    test_inputs = generate_test_inputs(parameters)
    assert len(test_inputs) == 10

    for inputs in test_inputs:
        assert "numbers" in inputs
        assert isinstance(inputs["numbers"], list)
        assert all(isinstance(num, int) for num in inputs["numbers"])

    """Test with dict parameters"""
    parameters = [{"name": "quantity", "type": "dict[str, int]"}]
    test_inputs = generate_test_inputs(parameters)
    assert len(test_inputs) == 10

    for inputs in test_inputs:
        assert "quantity" in inputs
        assert isinstance(inputs["quantity"], dict)
        assert all(isinstance(key, str) and isinstance(value, int) for key, value in inputs["quantity"].items())

if __name__ == "__main__":
    test_parse_function_definition()
    test_generate_test_inputs()