
import os
import sys
import json
import pytest

# Ensure src/ is in the Python path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from json_to_csv import ExportToCSV

TESTS_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(TESTS_DIR, 'data')
REFERENCE_PATH = os.path.join(DATA_DIR, 'original_format_reference.json')

@pytest.fixture
def reference_json():
    with open(REFERENCE_PATH, encoding='utf-8') as f:
        return json.load(f)

def test_to_records_matches_reference(reference_json):
    exporter = ExportToCSV(reference_json)
    records = exporter.to_records()
    # Check that the output is a list and not empty
    assert isinstance(records, list)
    assert len(records) > 0
    # Check that the first record contains expected keys
    expected_keys = {'id', 'annotation_id', 'annotator', 'text', 'audio', 'image'}
    assert expected_keys.issubset(records[0].keys())
    # Optionally, check the structure of the first record matches a precomputed expectation
    # (add more detailed checks as needed)
