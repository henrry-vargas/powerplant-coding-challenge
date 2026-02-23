from pydantic import BaseModel, Field, ConfigDict
from typing import List
from enum import Enum

class PowerPlantType(str, Enum):
    GAS_FIRED = "gasfired"
    TURBOJET = "turbojet"
    WIND_TURBINE = "windturbine"

class PowerPlant(BaseModel):
    name: str
    type: PowerPlantType
    efficiency: float
    pmin: float
    pmax: float

class Fuels(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    gas_price: float = Field(..., alias="gas(euro/MWh)")
    kerosine_price: float = Field(..., alias="kerosine(euro/MWh)")
    co2_price: float = Field(..., alias="co2(euro/ton)")
    wind_percent: float = Field(..., alias="wind(%)")

class Payload(BaseModel):
    load: float
    fuels: Fuels
    powerplants: List[PowerPlant]

class ProductionPlan(BaseModel):
    name: str
    p: float
