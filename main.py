from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from services_config import SERVICES  # Import the centralized service configuration
import uvicorn
import os
from datetime import datetime, timedelta
import socket
import logging
from contextlib import asynccontextmanager
from common.utils import load_soap_xml_files

SOAP_XML_DATA = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logging.info("FastAPI application is starting up (process loading).")
    global SOAP_XML_DATA
    soap_dir = os.path.join(os.path.dirname(__file__), "services", "soap")
    SOAP_XML_DATA = load_soap_xml_files(soap_dir)
    logging.info(f"Loaded {len(SOAP_XML_DATA)} SOAP XML files at startup.")
    yield
    # Shutdown actions
    logging.info("Uvicorn process is shutting down (app shutdown event).")

app = FastAPI(lifespan=lifespan)

# Set global logging level and format
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG, WARNING, ERROR as needed
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Capture the service load time and hostname/IP address
service_load_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Global dictionaries to track hits, last access time, and response times
service_data = {service: {"hits": 0, "last_access_time": None, "response_times": []} for service in SERVICES.keys()}

# Middleware to track hits, last access time, and response times
@app.middleware("http")
async def track_service_data(request: Request, call_next):
    path = request.url.path
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = datetime.now()

    # Identify the service being accessed
    service = None
    for service_name in service_data.keys():
        if path.startswith(f"/stub/{service_name}"):
            service = service_name
            service_data[service]["hits"] += 1
            service_data[service]["last_access_time"] = now
            break

    response = await call_next(request)
    end_time = datetime.now()

    # Calculate and store response time only for valid services
    if service:
        response_time = (end_time - start_time).total_seconds() * 1000  # in milliseconds
        service_data[service]["response_times"].append(response_time)

    return response

# Endpoint to retrieve service details
@app.get("/hits")
async def get_hits():
    total_hits = sum(data["hits"] for data in service_data.values())
    current_time = datetime.now()
    total_response_time = 0
    total_services_with_response_time = 0

    service_details = {}
    for service, data in service_data.items():
        avg_response_time = (
            sum(data["response_times"]) / len(data["response_times"])
            if data["response_times"]
            else 0
        )
        if avg_response_time > 0:
            total_response_time += avg_response_time
            total_services_with_response_time += 1

        service_details[service] = {
            "hits": data["hits"],
            "last_access_time": data["last_access_time"] or "N/A",
            "avg_response_time": f"{avg_response_time:.2f} ms",
            "status": "Active" if data["last_access_time"] and 
            (current_time - datetime.strptime(data["last_access_time"], "%Y-%m-%d %H:%M:%S")) < timedelta(seconds=100) #inactive timeout
            else "Inactive",
        }

    total_avg_response_time = (
        total_response_time / total_services_with_response_time
        if total_services_with_response_time > 0
        else 0
    )

    return {
        "total": total_hits,
        "services": service_details,
        "total_avg_response_time": f"{total_avg_response_time:.2f} ms",
        "service_load_time": service_load_time,
        "hostname": hostname,
        "ip_address": ip_address,
    }

# Endpoint to reset hit counters, last access times, and response times
@app.post("/reset")
async def reset_hits():
    for data in service_data.values():
        data["hits"] = 0
        data["last_access_time"] = None
        data["response_times"] = []  # Clear the response times list
    return {"message": "Hit counters reset successfully"}

# Serve the dashboard HTML
@app.get("/", response_class=FileResponse)
async def dashboard():
    html_path = os.path.join(os.path.dirname(__file__), "templates", "dashboard.html")
    return FileResponse(html_path)

# Dynamically include routers for all services
for service_name, service_info in SERVICES.items():
    app.include_router(service_info["router"], prefix=service_info["prefix"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, log_level="info")

