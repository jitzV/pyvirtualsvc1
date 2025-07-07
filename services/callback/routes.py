import asyncio
import os
from fastapi import APIRouter, Request
from fastapi.responses import Response
import httpx
import xml.etree.ElementTree as ET
import logging
from common.utils import load_soap_xml

router = APIRouter()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Namespace map - adjust based on your XML
NS = {
    'ns1': 'http://example.com/ns1',
    'ns2': 'http://example.com/ns2'
}

# Callback URL - replace with your target
CALLBACK_URL = "http://localhost:8080/endpoint"

# Predefined delay in seconds before sending the callback
CALLBACK_DELAY_SECONDS = 5


@router.post("/stub")
async def receive_stub(request: Request):
    body = await request.body()
    logging.info("Received Request:\n%s", body.decode())

    try:
        root = ET.fromstring(body)

        # Find serviceID with namespace-aware search
        service_id_elem = root.find(".//ns1:serviceID", NS)
        if service_id_elem is None:
            return Response(content="serviceID not found", status_code=400)

        service_id = service_id_elem.text
        logging.info(f"Extracted serviceID: {service_id}")

        # Send Acknowledgement Response
        ack_response = f"""
        <ns1:Acknowledgement xmlns:ns1="http://example.com/ns1">
            <ns1:status>Received</ns1:status>
        </ns1:Acknowledgement>
        """

        # Trigger callback with delay (don't block main thread)
        asyncio.create_task(send_callback(service_id))

        return Response(content=ack_response, media_type="application/xml")

    except ET.ParseError:
        logging.error("Invalid XML received")
        return Response(content="Invalid XML", status_code=400)


async def send_callback(service_id: str):
    try:
        logging.info(f"Waiting {CALLBACK_DELAY_SECONDS} seconds before sending callback...")
        await asyncio.sleep(CALLBACK_DELAY_SECONDS)

        # Load callback XML template
        # Get the base directory for service1
        base_dir = os.path.dirname(__file__)
        callback_xml = load_soap_xml("callbackReq.xml", base_dir)

        # Replace serviceID placeholder
        callback_xml = callback_xml.replace("{serviceID}", service_id)
        logging.info(f"Callback Request:\n{callback_xml}")

        # Send callback
        async with httpx.AsyncClient() as client:
            response = await client.post(CALLBACK_URL, content=callback_xml, headers={"Content-Type": "application/xml"})

        # Validate response
        logging.info(f"Callback Response Code: {response.status_code}")
        logging.info(f"Callback Response Body:\n{response.text}")

    except Exception as e:
        logging.error(f"Error during callback: {e}")
