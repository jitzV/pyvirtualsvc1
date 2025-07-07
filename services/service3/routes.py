from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import asyncio
from common.utils import load_json_template
import os

router = APIRouter()

@router.post("")
async def service3_handler(request: Request):
    payload = await request.json()
    await asyncio.sleep(0.5)

    # Get the base directory for service1
    base_dir = os.path.dirname(__file__)
    response_data = load_json_template("response_template.json", base_dir)


    response_data.update({
        "session": payload.get("session"),
        "flagConfirmed": payload.get("flag", False),
        "responseCode": 200
    })
    return JSONResponse(content=response_data)

# Example GET endpoint
@router.get("/info")
async def service3_info():
    # Example data to return
    info_data = {
        "service": "service3",
        "description": "This is a GET endpoint for service3.",
        "status": "active",
        "version": "1.0.0"
    }
    return JSONResponse(content=info_data)