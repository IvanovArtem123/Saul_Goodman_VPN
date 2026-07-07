from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Body

from api.services import get_current_user
from core.db import get_async_session


router = APIRouter(prefix='/promocodes', tags=['Промокоды'])


@router.post(
    '/create',
    response_model=PromocodeInfo,
    status_code=status.HTTP_200_OK,
    summary='Создание промокода'
)
async def create_promocode(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)],
    obj_in: PromocodeCreate
) -> PromocodeInfo:
    """Создание промокода для пользователя.
    Для конкретного пользователя или админа."""
    if not (await check_current_user_admin(user) or user.id == obj_in.user_id):
        obj_in.user_id = user.id
    new_promocode = await promo_crud.create_promocode(
        session=session, obj_in=obj_in)
    return new_promocode