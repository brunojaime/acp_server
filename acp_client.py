
import asyncio
from acp_sdk.client import Client
from colorama import Fore

async def run_university_workflow() -> None:
    async with Client(base_url="http://localhost:8001") as database_manager,Client(base_url="http://localhost:8002") as university_helper:
        run1 = await university_helper.run_sync(
            agent="learning_agent",input="Me gustaria que me cuentes que es un grafo"
        
        )
        content= run1.output[0].parts[0].content
        print(Fore.LIGHTMAGENTA_EX + content + Fore.RESET)

        run2 = await database_manager.run_sync(
            agent="policy_agent",input=f"Context: {content} . Y qué es una matriz de adyacencia?"
        )
        print(Fore.YELLOW + run2.output[0].parts[0].content + Fore.RESET)        

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_university_workflow())