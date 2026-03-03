# tests/test_storage_utils.py
import os
import tempfile
import shutil
import pytest
import importlib

from app.sharedlib.storage_utils import safe_filename



def test_basic_text():
    assert safe_filename("Tech Expo") == "tech_expo"

def test_leading_and_trailing_spaces():
    assert safe_filename("  Tech Expo  ") == "tech_expo"

def test_multiple_spaces():
    assert safe_filename("Tech   Expo   2026") == "tech_expo_2026"

def test_special_characters_removed():
    assert safe_filename("Tech@Expo#2026!") == "techexpo2026"

def test_mixed_case():
    assert safe_filename("TeCh ExPo") == "tech_expo"

def test_numbers_preserved():
    assert safe_filename("Expo 2026") == "expo_2026"

def test_only_special_characters():
    assert safe_filename("@#$%^") == ""

def test_empty_string():
    assert safe_filename("") == ""
