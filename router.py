import asyncio
import nest_asyncio
from acp_sdk.client import Client
from smolagents import LiteLLMModel
from smolagents.models import ChatMessage

#AgentCollection will structure the ACP agents in a forma to be able to use them
#ACPCallingAgent will be a router agent
from fastacp import AgentCollection, ACPCallingAgent 
from colorama import Fore
nest_asyncio.apply()


base_model = LiteLLMModel(model_id="openai/gpt-4o", max_tokens=2048)

def model(messages, **kwargs):
    fixed_messages = []
    for m in messages:
        if isinstance(m, dict):
            fixed_messages.append(ChatMessage(
                role=m["role"],
                content=m["content"][0]["text"] if isinstance(m["content"], list) else m["content"]
            ))
        else:
            fixed_messages.append(m)
    return base_model(fixed_messages, **kwargs)


async def run_university_workflow() -> None:
    async with Client(base_url="http://localhost:8001") as database_manager, Client(base_url="http://localhost:8002") as university_helper:
        # Create an AgentCollection with the agents
        agent_collection = await AgentCollection.from_acp(database_manager, university_helper)
        acp_agents = {agent.name: {"agent":agent,"client":client} for client,agent in agent_collection.agents }
        print(acp_agents)

        acpagent= ACPCallingAgent(
            acp_agents=acp_agents,
            model=model,
           
        )
        result = await acpagent.run("Necesito ayuda con una pregunta de base de datos, ¿puedes ayudarme a decir que es una matriz de incidencia?")
        print(Fore.YELLOW + f"final result: {result}" + Fore.RESET)
if __name__ == "__main__":
    asyncio.run(run_university_workflow())
    
        

