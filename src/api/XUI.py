import json
from typing import Dict, Any, List

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from crud.panel import panel_crud
from models.panel import Panel
from models.user import User
from models.subscription import Subscription
from api.services import (
    get_list_inbound_id, data_user_config,
    get_inbound_transport
)
from core.constants import TOKEN_PANEL


class XUIworker():
    """Класс добавления пользователя во все inbound всех панелей управления."""
    def __init__(
            self,
            user: User,
            sub: Subscription,
            session: AsyncSession,
            ):
        self.sub = sub
        self.user = user
        self.session = session
        self.client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=20)
        )

    async def add_client_to_panels(self, panels: List[Panel]) -> None:
        '''Добавление пользователя во все панели.'''
        for panel in panels:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
            headers = {'Authorization': f'Bearer {panel.api_token}'}
            all_ids_inbaunds = await self.get_inbaunds_ids(
                base_url_panel=base_url_panel,
                headers=headers)
            data = {
                "client": {
                    "email": self.user.email,
                    "totalGB": 0,
                    "expiryTime": int(self.sub.end_date.timestamp() * 1000),
                    "tgId": self.user.tg_id or 0,
                    "limitIp": 0,
                    "limitHwid": 0,
                    "enable": True,
                    'flow': 'xtls-rprx-vision'
                },
                "inboundIds": all_ids_inbaunds
                }
            await self.client.post(
                url=base_url_panel+'/panel/api/clients/add', headers=headers,
                json=data)

    async def get_inbaunds_ids(
            self, base_url_panel: str,
            headers: Dict[str, str]) -> List[int]:
        '''Получение всех id inbound панели управления.'''
        all_inbaunds = await self.client.get(
            url=base_url_panel + "/panel/api/inbounds/list",
            headers=headers)
        all_ids_inbaunds = await get_list_inbound_id(all_inbaunds.text)
        return all_ids_inbaunds

    async def get_sub_keys(self, panels: List[Panel]) -> List[str]:
        '''Возвращает список ключей юзера.'''
        keys_list = []
        for panel in panels:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
            headers = {'Authorization': f'Bearer {panel.api_token}'}
            response = await self.client.get(
                url=base_url_panel+f'/panel/api/clients/links/{self.user.email}',
                headers=headers)
            data = response.json()
            for key in data['obj']:
                keys_list.append(key)
        return keys_list
