from aiogram import Router, F
from aiogram.types import CallbackQuery, InaccessibleMessage
from aiogram.fsm.context import FSMContext
from keyboards.start import start_keyboard
from .utils import ServiceCallback

router = Router()


@router.callback_query(F.data == "cancel")
async def ca_cancel(callback: CallbackQuery, state: FSMContext):
    if isinstance(callback.message, InaccessibleMessage
                  ) or callback.message is None:
        await callback.answer("Сообщение недоступно", show_alert=True)
        return
    service = ServiceCallback(callback, state)
    if await service.go_back():
        return
    await callback.message.edit_text("Главное меню",
                                     reply_markup=start_keyboard())
    await state.clear()
