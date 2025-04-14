from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json, os, asyncio

router = APIRouter()

@router.post("")
async def service2_handler(request: Request):
    payload = await request.json()
    await asyncio.sleep(2.0)

    template_path = os.path.join(os.path.dirname(__file__), "response_template.json")
    with open(template_path) as f:
        response_data = json.load(f)

    response_data.update({
        "ack": True,
        "receivedTransactionId": payload.get("transactionId"),
        "currentStatus": payload.get("status")
    })
    return JSONResponse(content=response_data)