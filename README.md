# Powerplant Coding Challenge

REST API to calculate the production plan for a set of powerplants based on load, fuel prices, and plant constraints.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Docker (Optional)

## Installation

### Local Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the API
Start the server on port 8888:
```bash
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8888
```

### Docker
Build and run the container:
```bash
docker build -t powerplant-api .
docker run -p 8888:8888 powerplant-api
```

## API Endpoint

### POST `/productionplan`
Accepts a JSON payload describing the load, fuel costs, and available powerplants. Returns the optimal production plan.

Example usage with `curl`:
```bash
curl -X POST http://localhost:8888/productionplan \
  -H "Content-Type: application/json" \
  -d @example_payloads/payload1.json
```

## Implementation Details

- **Algorithm**: The solution implements a merit-order allocation strategy using a recursive backtracking solver to satisfy Pmin/Pmax constraints.
- **Costs**: Marginal costs are calculated per MWh, including CO2 emission allowances (0.3 ton/MWh) for gas-fired plants.
- **Validation**: Input/output data validation is handled via Pydantic models.
