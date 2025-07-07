# Virtual Services Platform

This FastAPI-based project hosts multiple virtual services and SOAP callback stubs. Each service is modular and located under the `services/` directory. The platform supports JSON and SOAP payloads, asynchronous callbacks, and is designed for integration testing and simulation.

## Project Structure

```
virtual-services/
├── main.py
├── common/
│   └── utils.py                 # shared helpers (e.g., JSON/XML loader)
├── services/
│   ├── service1/
│   │   ├── routes.py
│   │   ├── response_template.json
│   │   └── __init__.py
│   ├── service2/
│   │   ├── routes.py
│   │   ├── response_template.json
│   │   └── __init__.py
│   ├── callback/
│   │   ├── routes.py            # SOAP callback stub logic
│   │   ├── callbackReq.xml      # Callback XML template
│   │   └── ...
│   └── ...
├── requirements.txt
└── README.md
```

## Setup

1. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   # On Linux/Mac:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

## Running Tests

Run all tests with:

```bash
pytest -v
# OR
pytest -v ./test_main.py
```

## Features

- Modular FastAPI app with multiple virtual services
- SOAP callback stub with async callback and XML template replacement
- JSON and XML template loading utilities
- Logging for all requests, responses, and errors
- Easy extension for new services or endpoints

## Example SOAP Callback Flow

1. **POST** a SOAP XML to `/stub` (see `services/callback/routes.py`).
2. The service extracts `serviceID` from the request, sends an immediate XML acknowledgment, and schedules an async callback.
3. After a delay, the callback XML (with the correct `serviceID` inserted) is sent to the configured callback URL.

## Customization

- Edit `CALLBACK_URL` and `CALLBACK_DELAY_SECONDS` in `services/callback/routes.py` as needed.
- Place your callback XML template in the same folder and ensure it contains a `{serviceID}` placeholder.
- Add new services by creating a new folder under `services/` and registering its router in `main.py`.

## License

MIT License


