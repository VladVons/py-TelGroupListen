from telethon import TelegramClient, events

# Замініть ці значення на свої
API_ID = '27489309'
API_HASH = 'aa5afcef4665d19b80710ef1d9ce9b46'
BOT_TOKEN = '8179886965:AAHe_4_jOxWbvfLLifMv-gmK8AYKpDRv-pI'
SESSION = 'data/sessions/myName.session'

Client = TelegramClient('bot_session1', API_ID, API_HASH)
bot = Client.start(bot_token=BOT_TOKEN)

async def message_handler(event):
    print('got it', event.text)
    await event.respond(f"Привіт! {event.text}")

Client.add_event_handler(message_handler, events.NewMessage())

print("Бот запущено!")
Client.run_until_disconnected()
