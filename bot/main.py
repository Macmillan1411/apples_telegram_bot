import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from states import AppleForm, AppleUpdateForm

from config import BOT_TOKEN
from handlers import (
    send_welcome,
    send_help,
    add_apple,
    process_apple_name,
    process_apple_type,
    process_apple_description,
    process_apple_image_url,
    get_apple_command,
    list_apples_command,
    update_apple_command,
    delete_apple_command,
    process_name,
    process_type,
    process_description,
    process_image_url,
    process_apple_id,
)

# Configure logging
logging.basicConfig(level=logging.INFO)


async def main():
    # Initialize Bot and Dispatcher
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Register handlers using filters
    dp.message.register(send_welcome, Command("start"))
    dp.message.register(send_help, Command("help"))
    dp.message.register(add_apple, Command("add_apple"))

    # Register handlers for the create states
    dp.message.register(process_apple_name, AppleForm.waiting_for_name)
    dp.message.register(process_apple_type, AppleForm.waiting_for_type)
    dp.message.register(process_apple_description, AppleForm.waiting_for_description)
    dp.message.register(process_apple_image_url, AppleForm.waiting_for_image_url)

    dp.message.register(get_apple_command, Command("get_apple"))
    dp.message.register(list_apples_command, Command("list_apples"))

    # Register handlers for the update states
    dp.message.register(update_apple_command, Command("update_apple"))
    dp.message.register(process_apple_id, AppleUpdateForm.waiting_for_apple_id)
    dp.message.register(process_name, AppleUpdateForm.waiting_for_name)
    dp.message.register(process_type, AppleUpdateForm.waiting_for_type)
    dp.message.register(process_description, AppleUpdateForm.waiting_for_description)
    dp.message.register(process_image_url, AppleUpdateForm.waiting_for_image_url)

    dp.message.register(delete_apple_command, Command("delete_apple"))

    # Start polling
    try:
        logging.info("Starting bot...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
