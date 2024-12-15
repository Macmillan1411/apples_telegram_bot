import httpx

from config import FASTAPI_URL


async def create_apple(name: str, type: str, description: str, image: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FASTAPI_URL}/apples/",
            json={
                "name": name,
                "type": type,
                "description": description,
                "image": image,
            },
        )
        return response.json() if response.status_code == 201 else None


async def get_apple(apple_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FASTAPI_URL}/apples/{apple_id}")
        return response.json() if response.status_code == 200 else None


async def list_apples():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FASTAPI_URL}/apples/")
        return response.json() if response.status_code == 200 else []


async def update_apple(
    apple_id: int, name: str, type: str, description: str, image: str
):
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{FASTAPI_URL}/apples/{apple_id}",
            json={
                "name": name,
                "type": type,
                "description": description,
                "image": image,
            },
        )
        return response.json() if response.status_code == 200 else None


async def delete_apple(apple_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{FASTAPI_URL}/apples/{apple_id}")
        return response.status_code == 204  # Success code for deletion
