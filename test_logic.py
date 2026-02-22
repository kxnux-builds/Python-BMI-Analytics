import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import bmi_logic

def test_calculate_bmi():
    assert bmi_logic.calculate_bmi(70, 1.75) == 22.9
    assert bmi_logic.calculate_bmi(100, 1.80) == 30.9

def test_categorize_bmi():
    assert bmi_logic.categorize_bmi(17.0) == "Underweight"
    assert bmi_logic.categorize_bmi(18.5) == "Normal"
    assert bmi_logic.categorize_bmi(24.9) == "Normal"
    assert bmi_logic.categorize_bmi(25.0) == "Overweight"
    assert bmi_logic.categorize_bmi(30.0) == "Obese"

def test_validate_inputs_valid():
    is_valid, msg, w, h = bmi_logic.validate_inputs("75", "1.8")
    assert is_valid is True
    assert w == 75.0
    assert h == 1.8

def test_validate_inputs_invalid():
    is_valid, msg, w, h = bmi_logic.validate_inputs("abc", "1.8")
    assert is_valid is False
    assert "numeric" in msg

    is_valid, msg, w, h = bmi_logic.validate_inputs("10", "1.8") # Weight too low
    assert is_valid is False