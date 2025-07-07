from services import service1, service2, service3, soap, callback_ack, callback  # Import all service modules

# Define all services and their corresponding routers
SERVICES = {
    "service1": {"router": service1.router, "prefix": "/stub/service1"},
    "service2": {"router": service2.router, "prefix": "/stub/service2"},
    "service3": {"router": service3.router, "prefix": "/stub/service3"},
    "service4": {"router": soap.router, "prefix": "/soap"},
    "service5": {"router": callback_ack.router, "prefix": "/endpoint"},
    "service6": {"router": callback.router, "prefix": "/callback"},
}