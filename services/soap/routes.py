from fastapi import APIRouter, Request, Response
import asyncio
from xml.etree import ElementTree as ET


import logging
from xml.etree import ElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("")
async def soap_order(request: Request):
    body = await request.body()
    # Parse the incoming SOAP XML
    root = ET.fromstring(body)
    ns = {
        "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "ord": "http://example.com/order"
    }
    # Find RequestID in Header
    request_id_elem = root.find(".//ord:RequestID", ns)
    request_id = request_id_elem.text if request_id_elem is not None else "UNKNOWN"

    # Prepare response XML with replaced RequestID
    response_xml = RESPONSE_XML.replace("<ord:RequestID>REQ-7890</ord:RequestID>", f"<ord:RequestID>{request_id}</ord:RequestID>")

    await asyncio.sleep(0.5)

    return Response(content=response_xml, media_type="application/xml")