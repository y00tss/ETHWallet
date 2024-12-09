import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import async_session_maker
from routers.user import router as router_auth
from routers.wallet import router as router_wallet
from routers.transactions import router as router_transactions
from services.autostart.initial_data import InitializationData

app = FastAPI(
    title="Kauri API",
    description="Test task for Kauri",
)

current_dir = os.path.join(os.path.dirname(__file__))

# Authorizations
app.include_router(
    router_auth,
    prefix="/auth",
    tags=["Auth"],
)

# Wallets
app.include_router(
    router_wallet,
    prefix="/wallet",
    tags=["Wallet"],
)
# Transactions
app.include_router(
    router_transactions,
    prefix="/transactions",
    tags=["Transactions"],
)


@app.on_event("startup")
async def startup_event():
    async with async_session_maker() as session:
        init_data = InitializationData(session)
        await init_data.start_app()


origins = ["*"]

# Настройки CORS и конфигурации
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)
