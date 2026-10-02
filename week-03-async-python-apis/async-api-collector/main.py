import asyncio
import httpx

from api_client import fetch_data


async def main():

    print("Fetching API data...\n")

    async with httpx.AsyncClient() as client:

        users, posts, todos = await asyncio.gather(
            fetch_data(
                client,
                "Users",
                "https://jsonplaceholder.typicode.com/users"
            ),
            fetch_data(
                client,
                "Posts",
                "https://jsonplaceholder.typicode.com/wrong"
            ),
            fetch_data(
                client,
                "Todos",
                "https://jsonplaceholder.typicode.com/todos"
            )
        )

    print("\nResults")
    print("--------------------")
    print(f"Users: {len(users)}")
    print(f"Posts: {len(posts)}")
    print(f"Todos: {len(todos)}")


asyncio.run(main())