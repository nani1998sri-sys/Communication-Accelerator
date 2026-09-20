import asyncio
import logging
import httpx
from config import settings
from app.llm import LLMClient
from app.prompts import DAILY_PROMPT
from app.storage import save_lesson, save_message, load_state
log = logging.getLogger(__name__)
BASE = "https://api.telegram.org/bot"
def allowed(chat_id): return not settings.telegram_allowed_chat_id or str(chat_id) == settings.telegram_allowed_chat_id
async def send_message(client, chat_id, text): await client.post(f"{BASE}{settings.telegram_bot_token}/sendMessage", json={"chat_id": chat_id, "text": text[:4000]})
async def daily_lesson():
    lesson = await LLMClient().complete(DAILY_PROMPT); save_lesson(lesson); return lesson
async def handle_update(client, update):
    message = update.get("message", {}); chat_id = message.get("chat", {}).get("id"); text = (message.get("text") or "").strip()
    if chat_id is None or not allowed(chat_id): return
    save_message(str(chat_id), "user", text)
    if text == "/chatid": answer = f"Your Telegram chat ID is: {chat_id}"
    elif text in ("/start", "/help"): answer = "Executive Communication Coach\n\nCommands: /daily /practice /word /phrase /debate /presentation /interview /feedback /chatid /help"
    elif text == "/daily": answer = await daily_lesson()
    elif text == "/feedback": answer = await LLMClient().complete("Review recent practice and give three strengths, three improvements, and tomorrow's plan.\n" + str(load_state())[-10000:])
    elif text.startswith("/"): answer = await LLMClient().complete(f"Create a practical interactive exercise for {text}. Ask one question at a time and wait for the learner's answer.")
    else: answer = await LLMClient().complete(text)
    save_message(str(chat_id), "assistant", answer); await send_message(client, chat_id, answer)
async def run_bot():
    if not settings.telegram_bot_token: raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")
    offset = None
    async with httpx.AsyncClient(timeout=70) as client:
        while True:
            params = {"timeout": 50};
            if offset is not None: params["offset"] = offset
            response = await client.get(f"{BASE}{settings.telegram_bot_token}/getUpdates", params=params); response.raise_for_status()
            for update in response.json().get("result", []):
                offset = update["update_id"] + 1
                try: await handle_update(client, update)
                except Exception: log.exception("Update failed")
if __name__ == "__main__": logging.basicConfig(level=logging.INFO); asyncio.run(run_bot())
