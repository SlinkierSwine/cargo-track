#!/usr/bin/env python3
import httpx
import asyncio


async def test_service():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8001/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_service()) 