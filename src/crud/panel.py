import json
import requests

from schemas.panel import PanelCreate, PanelUpdate
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from models.panel import Panel


class CRUDPanel(CRUDBase[Panel, PanelCreate, PanelUpdate]):
    """CRUD для панели управления."""

    async def create_be_hash_pass(
        self,
        obj_in: PanelCreate,
        session: AsyncSession
    ):
        """Создание панели управления с хешированием пароля."""
        obj_panel = Panel(
            path = obj_in.path,
            domain = obj_in.domain,
            login = obj_in.login,
            password_hash = obj_in.password,
            country = obj_in.country
        )
        session.add(obj_panel)
        await session.commit()
        await session.refresh(obj_panel)
        return obj_panel

    async def get_panel_by_id(
        self,
        panel_id: int,
        session: AsyncSession
    ) -> Panel | None:
        """Получить панель управления по ее id."""
        panel = await self.get(obj_id=panel_id, session=session)
        return panel

    async def update_panel_cookie(
        self,
        db_obj: Panel,
        cookie: str,
        session: AsyncSession
    ) -> Panel:
        """Обновить cookie панели управления."""
        db_obj.cookie = cookie
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_cookie_by_panel_id(
        self,
        panel_id: int,
        session: AsyncSession
    ) -> str | None:
        """Получить cookie панели управления по ее id."""
        panel = await self.get(obj_id=panel_id, session=session)
        if panel:
            cookies_dict = json.loads(panel.cookie)
            cookies_jar = requests.utils.cookiejar_from_dict(cookies_dict)
            return cookies_jar
        return None

panel_crud = CRUDPanel(Panel)
