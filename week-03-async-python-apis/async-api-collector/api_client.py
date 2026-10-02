import httpx


async def fetch_data(client, name, url):
    try:
        response = await client.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        print(f"✓ {name} received")

        return data

    except httpx.TimeoutException:
        print(f"✗ {name} timed out")

    except httpx.HTTPStatusError as error:
        print(f"✗ {name} failed: HTTP {error.response.status_code}")

    except httpx.RequestError as error:
        print(f"✗ {name} request failed: {error}")

    return []