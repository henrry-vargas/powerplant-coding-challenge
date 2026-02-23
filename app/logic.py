from typing import List
from .models import Payload, ProductionPlan, PowerPlantType

def calculate_production_plan(payload: Payload) -> List[ProductionPlan]:
    """
    Calculates the production plan by first deciding which plants are active (Unit Commitment)
    and then distributing the load (Economic Dispatch).
    """
    load = payload.load
    fuels = payload.fuels
    plants = payload.powerplants

    # Pre-calculate costs and adjusted capacities
    plant_data = []
    for p in plants:
        cost = 0.0
        pmax = p.pmax
        
        if p.type == PowerPlantType.WIND_TURBINE:
            pmax = p.pmax * (fuels.wind_percent / 100.0)
        elif p.type == PowerPlantType.GAS_FIRED:
            cost = (fuels.gas_price / p.efficiency) + (0.3 * fuels.co2_price)
        elif p.type == PowerPlantType.TURBOJET:
            cost = fuels.kerosine_price / p.efficiency
        
        plant_data.append({
            "name": p.name,
            "cost": cost,
            "pmax": round(pmax, 1),
            "pmin": p.pmin
        })

    # Sort by merit order (cheapest first)
    plant_data.sort(key=lambda x: (x["cost"], -x["pmax"]))

    # Step 1: Unit Commitment - Find a combination of plants that can satisfy the load
    # We use backtracking to find the first combination (cheapest due to sorting) 
    # where Sum(Pmin) <= Load <= Sum(Pmax)
    
    def find_commitment(index, current_pmin, current_pmax):
        # Base case: if we found a valid range
        if current_pmin <= load <= current_pmax + 0.01:
            return []
        
        # If we went through all plants without finding a solution
        if index >= len(plant_data):
            return None

        # Try including the current plant (merit order priority)
        data = plant_data[index]
        res = find_commitment(index + 1, current_pmin + data["pmin"], current_pmax + data["pmax"])
        if res is not None:
            return [index] + res
        
        # Try skipping the current plant
        res = find_commitment(index + 1, current_pmin, current_pmax)
        if res is not None:
            return res
            
        return None

    active_indices = find_commitment(0, 0, 0)
    
    # If no solution found
    if active_indices is None:
        return [ProductionPlan(name=p.name, p=0.0) for p in plants]

    # Step 2: Economic Dispatch - Distribute the load among active plants
    # Start everyone at Pmin, then distribute remaining load greedily
    results = {data["name"]: 0.0 for data in plant_data}
    total_dispatched = 0.0
    
    # Set all active plants to Pmin
    for idx in active_indices:
        data = plant_data[idx]
        results[data["name"]] = data["pmin"]
        total_dispatched += data["pmin"]
    
    # Distribute the remaining load following merit order
    remaining_load = round(load - total_dispatched, 1)
    for idx in active_indices:
        if remaining_load <= 0:
            break
        
        data = plant_data[idx]
        can_take = round(data["pmax"] - data["pmin"], 1)
        take = min(remaining_load, can_take)
        
        results[data["name"]] = round(results[data["name"]] + take, 1)
        remaining_load = round(remaining_load - take, 1)

    # Return results in merit order (matching the required format/expectations)
    return [ProductionPlan(name=data["name"], p=results[data["name"]]) for data in plant_data]
