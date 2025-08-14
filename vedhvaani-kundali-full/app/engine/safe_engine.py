import hashlib
from datetime import datetime
NAK = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
 "Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
 "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]

PLANETS = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]

def seed_hash(*parts):
    s = "|".join(map(str, parts))
    import hashlib
    return hashlib.sha256(s.encode()).hexdigest()

def hex_to_float(hhex, maxv=360.0):
    chunk = (hhex[:8]).ljust(8, "0")
    v = int(chunk, 16)
    return (v / 0xFFFFFFFF) * maxv

def compute_all_safe(y,m,d,hour,lat,lon):
    # simple deterministic positions
    seed = seed_hash(y,m,d,hour,lat,lon)
    positions = {}
    for i,p in enumerate(PLANETS):
        hh = seed[i*6:(i+1)*6] + seed[-6:]
        positions[p] = {"lon": round(hex_to_float(hh),4)}
    asc = (((hour % 24)/24.0)*360.0 + (lon%360.0))%360.0
    bucket = {i: [] for i in range(12)}
    for pname,pdata in positions.items():
        idx = int(pdata['lon']//30)%12
        bucket[idx].append(pname)
    moon_lon = positions['Moon']['lon']
    span = 360.0/27.0
    nak_index = int(moon_lon//span)%27
    nak = NAK[nak_index]
    pada = int(((moon_lon%span)/span)*4)+1
    return {"ascendant": asc, "houses": [], "planets": positions, "bucket": bucket, "moon_nakshatra": nak, "moon_pada": pada}
