from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship

from .base import BaseModel
from .many_to_many import subscription_panels


class Panel(BaseModel):
    """Модель панели."""

    path = Column(String(150), nullable=False)
    domain = Column(String(150), nullable=False)
    port = Column(String(10))
    login = Column(String(150), nullable=False)
    password = Column(String(255), nullable=False)
    country = Column(String(150), nullable=False)
    subscriptions = relationship(
        "Subscription",
        secondary=subscription_panels,
        back_populates="panels",
        lazy='selectin'
    )
    ip = Column(String(16), nullable=False)
    api_token = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
