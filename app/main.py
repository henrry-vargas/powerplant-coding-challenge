from fastapi import FastAPI, HTTPException
from .models import Payload, ProductionPlan
from .logic import calculate_production_plan
from typing import List

app = FastAPI(title="Powerplant Production Plan API")

@app.post("/productionplan", response_model=List[ProductionPlan])
async def production_plan(payload: Payload):
    try:
        return calculate_production_plan(payload)
    except Exception as e:
        print(f"Error calculating production plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
