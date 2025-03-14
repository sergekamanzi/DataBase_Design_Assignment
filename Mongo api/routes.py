from fastapi import APIRouter, HTTPException
import controllers

router = APIRouter()

# CREATE a client with related data
@router.post("/clients/")
async def create_client_with_details(data: dict):
    return await controllers.create_client_with_details(data)

# GET a client with all related data
@router.get("/clients/{client_id}")
async def get_client_with_details(client_id: str):
    client_data = await controllers.get_client_details(client_id)
    if not client_data:
        raise HTTPException(status_code=404, detail="Client not found")
    return client_data

# UPDATE a client and related data
@router.put("/clients/{client_id}")
async def update_client(client_id: str, update_data: dict):
    result = await controllers.update_client(client_id, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Client not found")
    return result

# DELETE a client and all related data
@router.delete("/clients/{client_id}")
async def delete_client(client_id: str):
    result = await controllers.delete_client(client_id)
    if not result:
        raise HTTPException(status_code=404, detail="Client not found")
    return result
