try:
    import swisseph as swe
except Exception as e:
    raise RuntimeError('pyswisseph not installed')

def compute_all_swe(y,m,d,hour,lat,lon):
    # user must provide ephemeris files at app/ephe and EPHE_PATH env var or default
    import os
    ephe = os.environ.get('EPHE_PATH','./app/ephe')
    swe.set_ephe_path(ephe)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = swe.julday(y,m,d,hour)
    planets = {}
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    for name,code in [('Sun',swe.SUN),('Moon',swe.MOON),('Mars',swe.MARS),('Mercury',swe.MERCURY),('Jupiter',swe.JUPITER),('Venus',swe.VENUS),('Saturn',swe.SATURN),('Rahu',swe.TRUE_NODE)]:
        pos = swe.calc_ut(jd, code, flags)[0][0] % 360.0
        planets[name] = {'lon': pos}
    planets['Ketu'] = {'lon': (planets['Rahu']['lon']+180.0)%360.0}
    asc = swe.houses_ex(jd, swe.FLG_SIDEREAL, lat, lon, b'E')[1][0] % 360.0
    bucket = {i: [] for i in range(12)}
    for pname,pdata in planets.items():
        idx = int(pdata['lon']//30)%12
        bucket[idx].append(pname)
    moon_lon = planets['Moon']['lon']
    span = 360.0/27.0
    nak_index = int(moon_lon//span)%27
    nak = 'Nakshatra'
    return {'ascendant': asc, 'houses': [], 'planets': planets, 'bucket': bucket, 'moon_nakshatra': nak, 'moon_pada': 1}
