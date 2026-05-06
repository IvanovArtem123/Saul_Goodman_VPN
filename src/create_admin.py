import os
from dotenv import load_dotenv
import asyncio
from core.db import AsyncSessionLocal
from models.user import User
from core.security import hash_password


load_dotenv()


def get_required_env(var_name: str):
    """Получить переменную окружения или выдать ошибку"""
    value = os.getenv(var_name)
    if value:
        return value
    else:
        print(f"❌ Ошибка: Переменная окружения {var_name} не установлена!")


async def create_superuser():
    admin_email = get_required_env("ADMIN_EMAIL")
    admin_username = get_required_env("ADMIN_USERNAME")
    admin_password = get_required_env("ADMIN_PASSWORD")

    async with AsyncSessionLocal() as session:
        user = User(
            email=admin_email,
            username=admin_username,
            password_hash=await hash_password(admin_password),
            role=2
        )
        session.add(user)
        await session.commit()
        print("✅ Админ создан!")

if __name__ == "__main__":
    asyncio.run(create_superuser())
