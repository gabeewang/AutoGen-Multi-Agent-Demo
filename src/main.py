import os
from dotenv import load_dotenv
from pathlib import Path

import asyncio  
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from tools import search_web, fetch_url, write_file

load_dotenv()

system_prompt_researcher = Path("src/prompts/system_prompt_researcher.md").read_text(encoding="utf-8")
system_prompt_writer = Path("src/prompts/system_prompt_writer.md").read_text(encoding="utf-8")

async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        base_url="https://api.siliconflow.com/v1",
        model="deepseek-ai/DeepSeek-V3.2",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
        model_info={
            "family": "openai",
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": False
        }
    )

    researcher = AssistantAgent(
        name="Researcher",
        model_client=model_client,
        system_message=system_prompt_researcher,
        tools=[search_web, fetch_url]
    )

    writer = AssistantAgent(
        name="Writer",
        model_client=model_client,
        system_message=system_prompt_writer,
        tools=[write_file]
    )

    team = RoundRobinGroupChat(
        participants=[researcher, writer],
        max_turns=10
    )

    # 幫我整理Vue最新的測試版本Vue3.6的更新內容重點，並將內容經由整理，儲存至src資料夾中，檔名為vue3.6_.md
    task = input("請輸入指派任務(輸入 'exit' 即離開): ")

    if task.lower() == "exit":
        return

    async for event in team.run_stream(task=task):
        source = getattr(event, "source", None)
        content = getattr(event, "content", None)

        if source in {"Researcher", "Writer"} and isinstance(content, str):
            print(f"{source}:")
            print(content)
            print()


    await model_client.close()

asyncio.run(main())