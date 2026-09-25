import json
import urllib
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from core.db import get_async_session
from models.user import User
from schemas.user import UserInfo
from models.subscription import Subscription

USER_FIELDS_TO_LOAD = [
    User.id,
    User.username,
    User.uuid,
    User.email,
    User.tg_id,
    User.role,
    User.created_at,
    User.updated_at,
]


async def get_current_user(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserInfo:
    """Возвращает текущего пользователя по сессии."""
    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
        )

    query = (
        select(User)
        .where(User.id == user_id)
        .options(load_only(*USER_FIELDS_TO_LOAD))
    )
    result = await session.execute(query)
    user = result.scalars().first()

    if user is None:
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return UserInfo.model_validate(user)


async def get_list_inbound_id(data: str) -> list[int]:
    '''Получаем id инбаундов панели.'''
    data_js = json.loads(data)
    obj = data_js['obj']
    result = []
    for inbound in obj:
        if inbound['subSortIndex'] > 8000:
            continue
        inbound_id = inbound['id']
        result.append(int(inbound_id))
    return result


async def data_user_config(
        inbound_id: int, user: User, sub: Subscription,
        transport: str
        ) -> dict:
    '''Формируем data для запроса на добавления пользователя в inbound.'''
    if transport == 'xhttp':
        flow = ''
    if transport == 'tcp':
        flow = 'xtls-rprx-vision'
    end_date = sub.end_date
    expiry_time = int(end_date.timestamp() * 1000)
    settings_data = {
        'clients': [
            {
                'id': user.uuid,
                'flow': flow,
                'email': user.email,
                'limitIp': 0,
                'totalGB': 0,
                'expiryTime': expiry_time,
                'enable': True,
                'tgId': user.tg_id,
                'subId': sub.code,
                'comment': user.username,
                'reset': 0
            }
        ]
    }
    data = {
        'id': inbound_id,
        'settings': json.dumps(settings_data)
    }
    return data


async def get_inbound_transport(
        response_text: str
) -> str:
    '''Получаем транспорт инбаунда.'''
    obj_response = json.loads(response_text)
    obj = json.loads(obj_response['obj']['streamSettings'])
    return obj['network']
