from aiogram import Bot
from aiogram.types import Message
import html

from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State
from aiogram.filters import Command

from api_requests import (
    create_apple,
    get_apple,
    list_apples,
    update_apple,
    delete_apple,
)
from states import AppleForm, AppleUpdateForm


async def send_welcome(message: Message, bot: Bot):
    await message.answer(
        "Welcome to the Apple Bot! Use /help to see available commands."
    )


async def send_help(message: Message, bot: Bot):
    help_text = """
    Available Commands:
    /add_apple  - Add a new apple
    /get_apple <id> - Get apple details by ID
    /list_apples - List all apples
    /update_apple  - Update apple
    /delete_apple <id> - Delete apple by ID
    """
    help_text = html.escape(help_text)
    await message.answer(help_text, parse_mode="HTML")


async def add_apple(message: Message, bot: Bot, state: FSMContext):
    await message.answer("Please provide the name of the apple.")
    await state.set_state(AppleForm.waiting_for_name)


async def process_apple_name(message: Message, bot: Bot, state: FSMContext):
    # Save the name the user provides
    name = message.text
    await state.update_data(name=name)  # Store name in the state context

    # Ask for the apple's type
    await message.answer("Please provide the type of the apple.")
    await state.set_state(AppleForm.waiting_for_type)  # Move to the next state


async def process_apple_type(message: Message, bot: Bot, state: FSMContext):
    # Save the type the user provides
    type = message.text
    await state.update_data(type=type)

    # Ask for the apple's description
    await message.answer("Please provide the description of the apple.")
    await state.set_state(AppleForm.waiting_for_description)  # Move to the next state


async def process_apple_description(message: Message, bot: Bot, state: FSMContext):
    # Save the description the user provides
    description = message.text
    await state.update_data(description=description)

    # Ask for the apple's image URL
    await message.answer("Please provide the image URL for the apple.")
    await state.set_state(AppleForm.waiting_for_image_url)  # Move to the next state


async def process_apple_image_url(message: Message, bot: Bot, state: FSMContext):
    # Save the image URL the user provides
    image_url = message.text
    await state.update_data(image_url=image_url)

    # Now that all data is collected, you can save the apple to the database or perform other actions
    user_data = await state.get_data()  # Retrieve all data stored in the FSMContext
    name = user_data.get("name")
    type = user_data.get("type")
    description = user_data.get("description")
    image_url = user_data.get("image_url")

    new_apple = await create_apple(name, type, description, image_url)  # api call

    await message.answer(f"Apple added: {name}, {type}, {description}, {image_url}")
    await state.clear()


async def get_apple_command(message: Message, bot: Bot):
    try:
        apple_id = int(message.text.split(" ")[1])  # Extract the apple ID
        apple = await get_apple(apple_id)
        if apple:
            await message.answer(f"Apple details: {apple}")
        else:
            await message.answer("Apple not found.")
    except (ValueError, IndexError):
        await message.answer("Invalid apple ID. Please provide a valid number.")


async def list_apples_command(message: Message, bot: Bot):
    apples = await list_apples()
    if apples:
        await message.answer(f"Apples: {apples}")
    else:
        await message.answer("No apples found.")


# Update Apple Handlers
async def update_apple_command(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(AppleUpdateForm.waiting_for_apple_id)
    await message.answer("Please provide the ID of the apple you want to update.")


async def process_apple_id(message: Message, bot: Bot, state: FSMContext):
    try:
        apple_id = int(message.text)
        apple = await get_apple(apple_id)
        if apple:
            await state.update_data(apple_id=apple_id)
            await state.set_state(AppleUpdateForm.waiting_for_name)
            await message.answer(
                f"Found apple: {apple['name']}. You can update the name. Please provide the new name."
            )
        else:
            await message.answer("Apple not found. Please provide a valid apple ID.")
            await state.finish()
    except ValueError:
        await message.answer("Invalid apple ID. Please provide a valid number.")
        await state.finish()


async def process_name(message: Message, bot: Bot, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(AppleUpdateForm.waiting_for_type)
    await message.answer("Please provide the new type for the apple.")


async def process_type(message: Message, bot: Bot, state: FSMContext):
    apple_type = message.text
    await state.update_data(type=apple_type)
    await state.set_state(AppleUpdateForm.waiting_for_description)
    await message.answer("Please provide the new description for the apple.")


async def process_description(message: Message, bot: Bot, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await state.set_state(AppleUpdateForm.waiting_for_image_url)
    await message.answer("Please provide the new image URL for the apple.")


async def process_image_url(message: Message, bot: Bot, state: FSMContext):
    image_url = message.text
    user_data = await state.get_data()

    apple_id = user_data["apple_id"]
    name = user_data["name"]
    apple_type = user_data["type"]
    description = user_data["description"]

    updated_apple = await update_apple(
        apple_id, name, apple_type, description, image_url
    )

    if updated_apple:
        await message.answer(f"Apple updated successfully: {updated_apple}")
    else:
        await message.answer("Failed to update the apple.")

    await state.clear()


async def delete_apple_command(message: Message, bot: Bot):
    try:
        apple_id = int(message.text.split(" ")[1])  # Extract the apple ID
        if await delete_apple(apple_id):
            await message.answer(f"Apple with ID {apple_id} has been deleted.")
        else:
            await message.answer("Failed to delete the apple.")
    except (ValueError, IndexError):
        await message.answer("Invalid apple ID. Please provide a valid number.")
