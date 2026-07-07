from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.help import help_keyboard, instructions_keyboard
from .utils import ServiceCallback

router = Router()


@router.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery, state: FSMContext) -> None:
    service_callback = ServiceCallback(callback, state)
    message = await service_callback.service_callback(
        ServiceCallback.help_menu)
    if message is None:
        return
    await message.edit_text(
        "С чем вам помочь?", reply_markup=help_keyboard())


@router.callback_query(F.data == "support_chat")
async def cb_support_chat(callback: CallbackQuery, state: FSMContext) -> None:
    service_callback = ServiceCallback(callback, state)
    message = await service_callback.service_callback(
        ServiceCallback.support_chat_menu)
    if message is None:
        return
    await message.edit_text(
        'Вы можете обратиться в наш чат поддержки:'
        'https://t.me/saul_goodman_vpn_support')


@router.callback_query(F.data == "instructions")
async def cb_instructions(callback: CallbackQuery, state: FSMContext) -> None:
    service_callback = ServiceCallback(callback, state)
    message = await service_callback.service_callback(
        ServiceCallback.instructions_menu)
    if message is None:
        return
    await message.edit_text(
        'Выберите инструкцию для вашей платформы:',
        reply_markup=instructions_keyboard())
