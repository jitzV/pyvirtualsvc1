from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json, os, asyncio

router = APIRouter()

@router.post("")
async def service3_handler(request: Request):
    payload = await request.json()
    await asyncio.sleep(0.5)

    template_path = os.path.join(os.path.dirname(__file__), "response_template.json")
    with open(template_path) as f:
        response_data = json.load(f)

    response_data.update({
        "session": payload.get("session"),
        "flagConfirmed": payload.get("flag", False),
        "responseCode": 200
    })
    return JSONResponse(content=response_data)