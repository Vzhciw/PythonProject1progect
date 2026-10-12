import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart

TOKEN = "8792769490:AAFpAT-_gN7FHatz07czf-90fcno4dVXaio"
ADMIN_ID = 5411474773

bot = Bot(token=TOKEN)
dp = Dispatcher()

message_mapping = {}


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Отправь мне любое сообщение, текст, фото или стикер — я анонимно передам его создателю."
    )


@dp.message(F.from_user.id != ADMIN_ID)
async def forward_to_admin(message: types.Message):
    try:
        await bot.send_message(ADMIN_ID, "📩 Новое анонимное сообщение:")

        sent_message = await bot.copy_message(
            chat_id=ADMIN_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )

        message_mapping[sent_message.message_id] = message.from_user.id

        await message.answer("✅ Ваше сообщение успешно отправлено анонимно!")
    except Exception as e:
        await message.answer("❌ Ошибка при отправке сообщения.")
        print(f"Ошибка: {e}")


@dp.message(F.from_user.id == ADMIN_ID)
async def reply_to_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("⚠️ Чтобы ответить пользователю, сделай Reply (Ответить) на пересланное сообщение!")
        return

    replied_message_id = message.reply_to_message.message_id
    target_user_id = message_mapping.get(replied_message_id)

    if not target_user_id:
        await message.answer("❌ Не удалось найти пользователя для этого сообщения.")
        return

    try:
        await bot.send_message(
            chat_id=target_user_id,
            text=f"💬 Ответ от создателя бота:\n\n{message.text}"
        )
        await message.answer("✅ Ответ успешно отправлен пользователю!")
    except Exception as e:
        await message.answer(f"❌ Не удалось отправить ответ. Ошибка: {e}")


async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())