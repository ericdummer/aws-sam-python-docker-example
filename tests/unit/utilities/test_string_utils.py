import json
import pytest
import uuid

from utilities.string_utils import *

def test_is_uuid():
    assert is_uuid("123e4567-e89b-12d3-a456-426614174000")
    assert not is_uuid("123e4567-e89b-12d3-a456-426614174")

def test_to_uuid():
    assert to_uuid("123e4567-e89b-12d3-a456-426614174000")
    assert to_uuid("123e4567") is None

def test_dollar_string_to_float():
    assert dollar_string_to_float("$1,000.00") == 1000.0
    assert dollar_string_to_float("$1,000") == 1000.0
    assert dollar_string_to_float("$1,000.00") == 1000.0
    assert dollar_string_to_float("$1,000.00") == 1000.0
