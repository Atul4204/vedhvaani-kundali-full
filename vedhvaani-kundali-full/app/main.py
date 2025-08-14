from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os, json
from .engine import compute_all_safe, compute_all_swe
from .charts import north_indian, south_indian
from .pdf import make_pdf_report

app = FastAPI(title="VedhVaani Kundali Engine")

class KundaliRequest(BaseModel):
    y: int
    m: int
    d: int
    hour: float
    lat: float
    lon: float
    tz: float = 5.5
    lang: str = "hi"
    chart_style: str = "north"
    use_swe: bool = False

@app.get("/")
def root():
    return {"status": "VedhVaani Kundali API running"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/kundali/basic")
def kundali_basic(req: KundaliRequest = Body(...)):
    # choose engine: SWE if requested and available, otherwise fallback safe
    if req.use_swe:
        try:
            data = compute_all_swe(req.y, req.m, req.d, req.hour, req.lat, req.lon)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"SWE engine error: {e}")
    else:
        data = compute_all_safe(req.y, req.m, req.d, req.hour, req.lat, req.lon)
    # attach chart svg
    bucket = data.get('bucket', {})
    if req.chart_style.lower().startswith('south'):
        svg = south_indian.draw_chart(int(data['ascendant']//30), bucket)
    else:
        svg = north_indian.draw_chart(int(data['ascendant']//30), bucket)
    data['chart_svg'] = svg
    data['lang'] = req.lang
    data['chart_style'] = req.chart_style
    return data

@app.post("/kundali/pdf")
def kundali_pdf(req: KundaliRequest = Body(...)):
    # get kundali data
    payload = req.dict()
    payload['use_swe'] = bool(req.use_swe)
    # reuse basic endpoint logic
    resp = kundali_basic(req)
    # render pdf
    out_path = make_pdf_report(resp, lang=req.lang)
    return FileResponse(out_path, media_type='application/pdf', filename=os.path.basename(out_path))
