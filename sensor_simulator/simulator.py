import argparse, logging, math, random, time
from datetime import datetime, timezone
import httpx

logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | simulator | %(message)s")
log=logging.getLogger("simulator")

class PlantSimulator:
    def __init__(self):
        self.moisture=55.0; self.temperature=28.0; self.humidity=62.0; self.light=50.0; self.tank=100.0; self.tick=0

    def update(self):
        self.tick += 1
        self.moisture=max(5,self.moisture-1+random.uniform(-.15,.15))
        self.temperature=max(15,min(40,self.temperature+random.uniform(-.3,.3)))
        self.humidity=max(30,min(90,self.humidity+random.uniform(-.8,.8)))
        self.light=max(0,min(100,50+45*math.sin((self.tick%120)/120*2*math.pi)))

    def water(self):
        self.moisture=min(100,self.moisture+10)
        self.tank=max(0,self.tank-2.5)
        log.info("Virtual pump applied: moisture=%.1f%%",self.moisture)

    def payload(self,device):
        return {"device_id":device,"soil_moisture":round(self.moisture,2),"temperature":round(self.temperature,2),
                "humidity":round(self.humidity,2),"light_level":round(self.light,2),"water_tank_level":round(self.tank,2),
                "timestamp":datetime.now(timezone.utc).isoformat()}

def send(client,url,payload,key):
    delay=1
    for attempt in range(1,4):
        try:
            r=client.post(url+"/api/sensors/data",json=payload,headers={"x-api-key":key},timeout=5)
            r.raise_for_status(); return r.json()
        except httpx.HTTPError as e:
            log.warning("API attempt %s/3 failed: %s",attempt,e)
            if attempt<3: time.sleep(delay); delay*=2
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--url",default="http://127.0.0.1:8000")
    ap.add_argument("--interval",type=float,default=5)
    ap.add_argument("--device",default="PLANT-001")
    ap.add_argument("--api-key",default="change-device-key")
    ap.add_argument("--offline",action="store_true")
    a=ap.parse_args()
    sim=PlantSimulator()
    log.info("Starting %s",a.device)
    with httpx.Client() as client:
        while True:
            sim.update(); p=sim.payload(a.device)
            log.info("soil=%s%% temp=%sC humidity=%s%% light=%s%%",p["soil_moisture"],p["temperature"],p["humidity"],p["light_level"])
            if not a.offline:
                result=send(client,a.url,p,a.api_key)
                if result and result.get("automation")=="watered": sim.water()
                elif result is None: log.error("Backend unavailable; continuing simulation")
            time.sleep(a.interval)

if __name__=="__main__": main()
