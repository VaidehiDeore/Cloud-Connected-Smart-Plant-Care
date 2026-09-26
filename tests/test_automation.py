from automation.watering_engine import decide

def test_dry():
    assert decide(20,30,80,10,False,True).watering_required

def test_moist():
    assert not decide(50,30,80,10,False,True).watering_required

def test_low_tank():
    assert decide(20,30,5,10,False,True).reason=="water_tank_low"

def test_pump_on():
    assert decide(20,30,80,10,True,True).reason=="pump_already_on"
