from dataclasses import dataclass

@dataclass
class Decision:
    watering_required: bool
    reason: str

def decide(moisture, threshold, tank, minimum_tank, pump_on, cooldown_complete):
    if moisture >= threshold: return Decision(False,"moisture_above_threshold")
    if tank <= minimum_tank: return Decision(False,"water_tank_low")
    if pump_on: return Decision(False,"pump_already_on")
    if not cooldown_complete: return Decision(False,"cooldown")
    return Decision(True,"low_moisture")
