from fastapi import APIRouter, Response
import asyncio
from common.utils import load_soap_xml
import os

router = APIRouter()

@router.post("")
async def service3_handler():
    await asyncio.sleep(0.5)

    # Get the base directory for service1
    base_dir = os.path.dirname(__file__)
    response_xml = load_soap_xml("callbackRes.xml", base_dir)

    return Response(content=response_xml, media_type="application/xml")
