import os
import json
import tempfile
import pytest
from ..validator import Validator


@pytest.fixture
def temp_schema_file():
    schema = {
        "id": "int:rand",
        "name": "str:rand",
        "created_at": "timestamp:"
    }
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
        temp_file.write(json.dumps(schema).encode('utf-8'))
        temp_file_path = temp_file.name
    yield temp_file_path
    os.remove(temp_file_path)


def test_validator_with_json_schema(temp_schema_file):
    validator = Validator(
        path='.',
        count=10,
        name='test_file',
        prefix='test_',
        schema=temp_schema_file,
        lines=5,
        clear=False,
        threads=1
    )

    expected_schema = {
        "id": "int:rand",
        "name": "str:rand",
        "created_at": "timestamp:"
    }
    assert validator.data_schema == expected_schema
