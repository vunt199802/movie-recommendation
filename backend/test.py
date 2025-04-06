import asyncio
import httpx

BASE_URL = "http://localhost:8000"

# 10 concurrent GET requests to "/"
async def call_root(client: httpx.AsyncClient, i: int):
    response = await client.get(f"{BASE_URL}/")
    print(f"[Root #{i}] Status: {response.status_code}, Response: {response.json()}")

# 10 concurrent POST requests to "/translate"
async def call_recommend(client: httpx.AsyncClient, i: int):
    payload = {
        "favorite_movie_with_reason": "The Shawshank Redemption Because it taught me to never give up hope no matter how hard life gets",
        "release_year_preference": "I want to watch movies that were released after 1990",
        "mood_preference": "I want to watch something stupid and fun"
    }
    response = await client.post(f"{BASE_URL}/recommend", json=payload)
    print(f"[Recommend #{i}] Status: {response.status_code}, Response: {response.json()}")

# Entry point for concurrency
async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []

        # Add 10 GET and 10 POST requests
        for i in range(10):
            tasks.append(call_root(client, i))
            tasks.append(call_recommend(client, i))

        # Run all 20 concurrently
        await asyncio.gather(*tasks)

# Run the script
if __name__ == "__main__":
    asyncio.run(main())