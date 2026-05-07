from typing import Annotated, List

from fastapi.params import Body
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from schemas.user import UserCreate, UserShortInfo, UserUpdate, UserInfo
from crud.user import user_crud
from api.services import get_current_user
from api.validators.user import (
    check_unique_email_username_phone_tgid, check_current_user_admin_or_SU,
    get_user_or_404, check_permission_values
    )
from api.exceptions import bad_request, forbidden
from models.user import User

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get(
    '/me',
    response_model=UserInfo,
    status_code=status.HTTP_200_OK,
    summary='Информация о текущем пользователе'
)
async def get_current_user_info(
    user: Annotated[User, Depends(get_current_user)]
) -> UserInfo:
    """Получить информацию о текущем пользователе."""
    return user


@router.get(
    '/get_all',
    response_model=List[UserShortInfo],
    summary='Информация о всех пользователях',
)
async def get_all_users(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)]
) -> List[UserShortInfo]:
    if await check_current_user_admin_or_SU(user):
        return await user_crud.get_all(session)
    return forbidden('Недостаточно прав для получения списка пользователей')


@router.get(
    '/{user_id}',
    response_model=UserShortInfo,
    status_code=status.HTTP_200_OK,
    summary='Информация о пользователе'
)
async def get_user_info(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)],
    user_id: int,
) -> UserShortInfo:
    """Получить информацию о пользователе."""
    if await check_current_user_admin_or_SU(user):
        user = await get_user_or_404(user_id, session)
    return user


@router.post(
        '/create',
        response_model=UserShortInfo,
        status_code=status.HTTP_201_CREATED,
        summary='Новый пользователь',
    )
async def create_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_in: UserCreate = Body(
                openapi_examples={
                    'user1': {
                        'summary': 'Пример пользователя',
                        'value': {
                            'username': 'TestName1',
                            'password': 'TestPassword1',
                            'email': 'testmail@gmail.com',
                            'phone': '+79998887766',
                            'tg_id': '123456789'
                        }
                    }
                }
            ),
) -> UserShortInfo:
    """Создать нового пользователя."""
    await check_unique_email_username_phone_tgid(user_in, session)
    return await user_crud.create_user_with_hash_password(user_in, session)


@router.patch(
    '/update/{user_id}',
    response_model=UserShortInfo,
    status_code=status.HTTP_200_OK,
    summary='Обновление информации о пользователе',
)
async def update_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)],
    user_id: int,
    user_in: UserUpdate = Body(
                openapi_examples={
                    'user1_update': {
                        'summary': 'Пример обновления пользователя для user1',
                        'value': {
                            'username': 'TestName1_up',
                            'password': 'TestPassword1_up',
                            'email': 'testmail_up@gmail.com',
                            'phone': '+79998887765',
                            'tg_id': '123456785'
                        }
                    }
                }),
) -> UserShortInfo:
    """Обновить информацию о пользователе."""
    if ((not await check_current_user_admin_or_SU(user)) or
            (not (user.id == user_id))):
        return bad_request(
            'Недостаточно прав для обновления информации о пользователе.'
            )
    db_user = await get_user_or_404(user_id, session)
    await check_permission_values(
        user=db_user,
        user_in=user_in)
    if db_user:
        await check_unique_email_username_phone_tgid(
            session=session,
            user_obj=user_in
        )
        return await user_crud.update_user_with_hash_password(
            db_obj=db_user,
            obj_in=user_in,
            session=session
        )


@router.delete(
    '/delete/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалитль пользователя',
    )
async def delete_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)],
    user_id: int,
) -> None:
    """Удалить пользователя."""
    if not (await check_current_user_admin_or_SU(user) or
            (user.id == user_id)):
        return bad_request('Недостаточно прав для удаления пользователя.')
    user = await get_user_or_404(user_id, session)
    if user:
        await user_crud.delete(db_obj=user, session=session)
