import asyncio
from telethon import TelegramClient, events

# Конфігурація
aName = "data/sessions/myName.session"
aParams = {
    "api_id": 27489309,
    "api_hash": "aa5afcef4665d19b80710ef1d9ce9b46"
}
bot_token = "8179886965:AAHe_4_jOxWbvfLLifMv-gmK8AYKpDRv-pI"

aConf = {'event': 'NewMessage'}  # Тип події
ConfGroup = [-1001234567890]  # ID груп, де працюватиме бот

ConfEvent = aConf.get('event', 'NewMessage')
EventType = getattr(events, ConfEvent, None)

async def main():
    async with TelegramClient(aName, **aParams) as Client:
        await Client.start(bot_token=bot_token)
        print("Бот працює...")

        if EventType:
            class Handler:
                @staticmethod
                async def OnEvent(event):
                    await event.respond(f'Отримано {ConfEvent} в {event.chat_id}')

            # Додаємо обробник
            Client.add_event_handler(Handler.OnEvent, EventType(chats=ConfGroup))
        else:
            print(f"❌ Помилка: Подія {ConfEvent} не знайдена в Telethon!")

        await Client.run_until_disconnected()  # Бот працює у фоновому режимі

asyncio.run(main())

from telethon import TelegramClient, events

# # Введіть свої дані
# API_ID = '27489309'
# API_HASH = 'aa5afcef4665d19b80710ef1d9ce9b46'
# BOT_TOKEN = '8179886965:AAHe_4_jOxWbvfLLifMv-gmK8AYKpDRv-pI'

# # Створення клієнта
# bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# # Обробник вхідних повідомлень
# @bot.on(events.NewMessage())
# async def handler(event):
#     print('got it')
#     await event.respond('Привіт! Як справи?')

# # Запуск бота
# print("Бот запущено!")
# bot.run_until_disconnected()
