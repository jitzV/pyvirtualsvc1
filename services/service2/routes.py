from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import asyncio
from common.utils import load_json_template
import os

router = APIRouter()

@router.post("")
async def service2_handler(request: Request):
    payload = await request.json()
    await asyncio.sleep(1.0)

    # Get the base directory for service1
    base_dir = os.path.dirname(__file__)
    response_data = load_json_template("response_template.json", base_dir)

    response_data.update({
        "status": "success",
        "userId": payload.get("userId"),
        "details": payload.get("details")
    })
    return JSONResponse(content=response_data)