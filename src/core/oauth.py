from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from core.config import settings
from core.constants import SERVER_METADATA_URL

config = Config(".env")

oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url=SERVER_METADATA_URL,
    client_kwargs={"scope": "openid email profile"},
)