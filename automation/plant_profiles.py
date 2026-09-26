PLANT_PROFILES = {
    "SUCCULENT": 20,
    "TOMATO": 40,
    "HERB": 35,
    "INDOOR PLANT": 30,
}

def get_threshold(plant_type):
    return PLANT_PROFILES.get(plant_type.strip().upper(), 30)
