from acp_sdk.client import Client
import asyncio
from colorama import Fore 

async def example() -> None:
    async with Client(base_url="http://localhost:8001") as client:
        run = await client.run_sync(
            agent="policy_agent", input="Que es una matriz de incidencia?"
        )
        print(Fore.YELLOW + run.output[0].parts[0].content + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(example())
    print(Fore.GREEN + "Run completed successfully!" + Fore.RESET)
    