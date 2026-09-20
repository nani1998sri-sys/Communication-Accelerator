import asyncio, sys
from app.llm import LLMClient
from app.prompts import DAILY_PROMPT
from app.storage import save_lesson
from app.telegram import run_bot
async def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "daily"
    if command == "daily":
        lesson = await LLMClient().complete(DAILY_PROMPT); save_lesson(lesson); print(lesson)
    elif command == "bot": await run_bot()
    else: raise SystemExit("Use: python -m app.cli daily|bot")
if __name__ == "__main__": asyncio.run(main())
