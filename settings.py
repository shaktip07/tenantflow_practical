from decouple import config

# To decode JWT token
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-xhvmvna*#b!1^877=wne(i*8jmwcw&(tcskrl3pi=x91+a!81q",
)
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=60
)

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="*",
)

# DB_INSTANCE_HOST = config("DB_INSTANCE_HOST", default="localhost")
# DB_NAME = config("DB_NAME", default="organization_management_temp")
# DB_USER = config("DB_USER", default="postgres")
# DB_PASSWORD = config("DB_PASSWORD", default="Patel@1234")
# DB_PORT = config("DB_PORT", default="5432")

DB_INSTANCE_HOST = "localhost"
DB_NAME = "organization_management_temp"
DB_USER = "postgres"
DB_PASSWORD = "Patel1234"
DB_PORT = "5432"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_INSTANCE_HOST}:{DB_PORT}/{DB_NAME}"

TIME_ZONE = "Asia/Kolkata"