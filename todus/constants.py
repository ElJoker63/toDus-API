"""Constantes del protocolo ToDus."""

# XMPP
XMPP_HOST = "im.todus.cu"
XMPP_PORT = 1756
MUCLIGHT_HOST = "muclight.im.todus.cu"
CHANNEL_HOST = "ch.im.todus.cu"

# Auth / Versión
AUTH_VERSION_NAME = "2.1.2"
AUTH_VERSION_CODE = "30102"

# HTTP Base URLs
AUTH_URL = "https://auth.todus.cu"
CHAT_URL = "https://chat.todus.cu"
CLIENT_URL = "https://client.todus.cu"
S3_URL = "https://s3.todus.cu"
STICKERS_URL = "https://stickers.todus.cu"
CATALOGUE_URL = "https://todus.cu/catalog"

# Configuración
BUFFER_SIZE = 1024 * 1024
KEEPALIVE_INTERVAL = 25
DEFAULT_TIMEOUT = 15
MAX_MSG_TEXT_SIZE = 8192
MAX_MESSAGE_LENGTH = 65536
COUNTER_VISIBLE_THRESHOLD = 200

# Namespaces
STATUS_NAMESPACE = "status"
REACTION_NAMESPACE = "reaction"
STATUS_RECEPTOR = "status@status.im.todus.cu"
STICKERS_OFFICIAL = "stickers.todus.cu"