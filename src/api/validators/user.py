from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import bad_request, not_found
from sqlalchemy import select, or_

from schemas.user import UserCreate
from models.user import User, UserRole
from crud.user import user_crud


async def check_unique_email_username_phone_tgid(
        user_obj: UserCreate,
        session: AsyncSession
) -> None:
    """Проверка на уникальность полей модели пользователя:
    email
    username
    phone"""
    conditions = []
    if user_obj.username:
        conditions.append(User.username == user_obj.username)
    if user_obj.email:
        conditions.append(User.email == user_obj.email)
    if user_obj.phone:
        conditions.append(User.phone == user_obj.phone)
    if conditions:
        existing_users = await session.execute(
            select(User).where(or_(*conditions))
        )
        existing_obj_users = existing_users.scalars().all()
        if existing_obj_users:
            message = 'Поля уже заняты: '
            for existing in existing_obj_users:
                if (user_obj.username and
                        existing.username == user_obj.username):
                    message += 'username, '
                if user_obj.email and existing.email == user_obj.email:
                    message += 'email, '
                if user_obj.phone and existing.phone == user_obj.phone:
                    message += 'phone, '
            result = message[:-2] + '.'
            raise bad_request(result)
    return None


async def check_current_user_admin_or_SU(
        user: User
) -> bool:
    """Проверка является юзер админом или суперюзером."""
    if user.role == UserRole.ADMIN or user.role == UserRole.SUPER_USER:
        return True
    return False


async def get_user_or_404(
        user_id: int,
        session: AsyncSession
) -> User:
    """Получить пользователя по id или 404 ошибку."""
    result = await user_crud.get(session=session, obj_id=user_id)
    if not result:
        raise not_found('Пользователь не найден.')
    return result
