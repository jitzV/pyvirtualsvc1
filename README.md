mkdir user_service && cd user_service
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install fastapi uvicorn
pip freeze > requirements.txt
pip install -r requirements.txt

virtual-services/
├── main.py
├── common/
│   └── utils.py                 # shared helpers (e.g., JSON loader)
├── services/
│   ├── service1/
│   │   ├── routes.py
│   │   ├── response_template.json
│   │   └── __init__.py
│   ├── service2/
│   │   ├── routes.py
│   │   ├── response_template.json
│   │   └── __init__.py
│   └── ...
├── requirements.txt
└── README.md

## Virtual Services Platform

This FastAPI-based project hosts multiple virtual services. Each service is modular and located under the `services/` directory. To start the server:

```bash
uvicorn main:app --reload
```
