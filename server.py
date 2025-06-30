from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server

from crewai import Crew, Task, Agent, LLM
from crewai_tools import RagTool

import nest_asyncio
nest_asyncio.apply()

server = Server()
llm = LLM(model="openai/gpt-4", max_tokens=1024)

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4",
        }
    },
    "embedding_model": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-ada-002"
        }
    }
}
rag_tool = RagTool(config=config,  
                   chunk_size=1200,       
                   chunk_overlap=200,     
                  )
rag_tool.add("data/ResumenMuyResumido.pdf", data_type="pdf_file")


@server.agent()
async def policy_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    "This is an agent which assists to students on Database Management questions ."

    insurance_agent = Agent(
        role="Database Management Teacher", 
        goal="Determine whether something is covered or not",
        backstory="You are an expert  Database Management designed to assist with coverage queries",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[rag_tool], 
        max_retry_limit=5
    )
    
    task1 = Task(
         description=input[0].parts[0].content,
         expected_output = "A comprehensive response as to the users question",
         agent=insurance_agent
    )
    crew = Crew(agents=[insurance_agent], tasks=[task1], verbose=True)
    
    task_output = await crew.kickoff_async()
    yield Message(parts=[MessagePart(content=str(task_output))])

if __name__ == "__main__":
    server.run(port=8001)