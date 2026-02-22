import re

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculates BMI using standard metric units."""
    return round(weight_kg / (height_m ** 2), 1)

def categorize_bmi(bmi: float) -> str:
    """Accurate medical ranges for BMI classification."""
    if bmi < 18.5: return "Underweight"
    elif bmi < 25.0: return "Normal"
    elif bmi < 30.0: return "Overweight"
    else: return "Obese"

def convert_weight(weight_str: str, unit: str) -> tuple[bool, str, float]:
    """Converts weight to kg based on the selected unit."""
    try:
        w = float(weight_str)
        if unit == "lbs":
            w = w * 0.453592
        return True, "", round(w, 2)
    except ValueError:
        return False, "Invalid weight format. Use numbers only.", 0.0

def convert_height(height_str: str, unit: str) -> tuple[bool, str, float]:
    """Converts height to meters based on the selected unit using Regex."""
    try:
        if unit == "ft'in":
            match = re.match(r"(\d+)[\'\.\-\s,]+(\d+)?", height_str.strip())
            if match:
                feet = float(match.group(1))
                inches = float(match.group(2)) if match.group(2) else 0.0
            else:
                feet = float(height_str)
                inches = 0.0
            total_inches = (feet * 12) + inches
            return True, "", round(total_inches * 0.0254, 3)
        
        elif unit == "cm":
            return True, "", round(float(height_str) / 100.0, 3)
        
        else: # "m"
            return True, "", round(float(height_str), 3)
            
    except ValueError:
        return False, "Invalid height format.", 0.0

def validate_inputs(w_str: str, w_unit: str, h_str: str, h_unit: str) -> tuple[bool, str, float, float]:
    """Master validator that handles conversions and bounds checking."""
    w_valid, w_err, weight_kg = convert_weight(w_str, w_unit)
    if not w_valid: return False, w_err, 0.0, 0.0
    
    h_valid, h_err, height_m = convert_height(h_str, h_unit)
    if not h_valid: return False, h_err, 0.0, 0.0
    
    if not (20 <= weight_kg <= 300):
        return False, "Converted weight must be between 20kg and 300kg.", 0.0, 0.0
    if not (0.5 <= height_m <= 2.5):
        return False, "Converted height must be between 0.5m and 2.5m.", 0.0, 0.0

    return True, "", weight_kg, height_m

def calculate_moving_average(data: list, window: int = 3) -> list:
    """Calculates a simple moving average for smoothing trend lines."""
    if len(data) < window: return data 
    moving_averages = []
    for i in range(len(data)):
        if i < window - 1: moving_averages.append(None) 
        else:
            window_slice = data[i - window + 1 : i + 1]
            moving_averages.append(sum(window_slice) / window)
    return moving_averages