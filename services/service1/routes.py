from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json, os, asyncio

router = APIRouter()

@router.post("")
async def service1_handler(request: Request):
    payload = await request.json()
    await asyncio.sleep(1.0)

    template_path = os.path.join(os.path.dirname(__file__), "response_template.json")
    with open(template_path) as f:
        response_data = json.load(f)

    response_data.update({
        "status": "ok",
        "userId": payload.get("userId"),
        "action": payload.get("action")
    })
    return JSONResponse(content=response_data)