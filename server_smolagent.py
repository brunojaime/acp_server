from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from smolagents import CodeAgent,DuckDuckGoSearchTool,LiteLLMModel,VisitWebpageTool

server = Server()

model = LiteLLMModel(model_id="openai/gpt-4o", max_tokens=2048)    

@server.agent()
async def learning_agent(input: list[Message]) -> AsyncGenerator[RunYield,RunYieldResume]:
       "This is a CodeAgent which supports the University helping students with their questions."    
       agent=CodeAgent(
            tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
            model=model,  
       )
       prompt = input[0].parts[0].content
       response = agent.run(prompt)
       yield Message(parts=[MessagePart(content=str(response))])




if __name__ == "__main__":
    server.run(port=8002)
