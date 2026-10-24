# examples/quickstart.py
import asyncio
from nebulawrap.client import NebulaClient
from nebulawrap.providers.openai_adapter import OpenAIAdapter

async def main():
    provider = OpenAIAdapter(api_key="...")  # implement adapter per provider
    client = NebulaClient(provider)
    res = await client.generate("Write a haiku about resilience in two lines.")
    print(res['text'])
    print("GoldenDAG:", res['decision_capsule']['golden_dag'])

if __name__=="__main__":
    asyncio.run(main())
