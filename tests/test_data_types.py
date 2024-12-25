import pytest
from ..file import File

# Sample schemas for testing
schemas = [
    {"id": "int:rand", "name": "str:rand", "created_at": "timestamp:"},
    {"id": "int:5", "name": "str:fixed_name", "created_at": "timestamp:"},
    {"id": "int:rand(10,20)", "name": "str:rand", "status": "[\"active\", \"inactive\"]"},
]

# Expected data types
expected_types = [
    {"id": int, "name": str, "created_at": float},
    {"id": int, "name": str, "created_at": float},
    {"id": int, "name": str, "status": str},
]

@pytest.mark.parametrize("schema, expected_type", zip(schemas, expected_types))
def test_data_type(schema, expected_type):
    file_instance = File("filename", schema)
    for key, expected in expected_type.items():
        assert isinstance(file_instance.result[key], expected), f"{key} is not of type {expected}"

@pytest.mark.parametrize("schema", schemas)
def test_different_schemas(schema):
    file_instance = File("filename", schema)
    assert isinstance(file_instance.result, dict)
    assert set(file_instance.result.keys()) == set(schema.keys())

