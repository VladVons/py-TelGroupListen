import asyncio
from telethon import TelegramClient, events

# Замініть ці значення на свої
API_ID = '27489309'
API_HASH = 'aa5afcef4665d19b80710ef1d9ce9b46'
BOT_TOKEN = '8179886965:AAHe_4_jOxWbvfLLifMv-gmK8AYKpDRv-pI'
#SESSION = 'data/sessions/myName.session'
SESSION = 'bot_session1'

async def message_handler(event):
    print('got it', event.text)
    await event.respond(f"Привіт! {event.text}")

async def Session():
    async with TelegramClient(SESSION, API_ID, API_HASH) as Client:
        await Client.start(bot_token=BOT_TOKEN)

        Client.add_event_handler(message_handler, events.NewMessage())
        await Client.run_until_disconnected()

asyncio.run(Session())
