import os
from models.user import User
from passlib.context import CryptContext
from sqlalchemy import select


class InitializationData:
    """For starting the project with initial"""

    def __init__(self, session):
        self.session = session

    async def start_app(self):
        await self._create_superuser()

    async def _create_superuser(self):
        """Creating a superuser if it does not exist yet."""

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        username = os.getenv("SUPERUSER_USERNAME", "admin")
        email = os.getenv("SUPERUSER_EMAIL", "admin@admin.com")
        password = os.getenv("SUPERUSER_PASSWORD", "admin")

        try:
            result = await self.session.execute(select(User).where(User.username == username))  # noqa
            user = result.scalars().first()

            if not user:
                hashed_password = pwd_context.hash(password)
                new_user = User(
                    username=username,
                    email=email,
                    hashed_password=hashed_password,
                    is_superuser=True
                )
                self.session.add(new_user)
                await self.session.commit()

        except Exception as e:
            return {"status": 500, "description": f"{e}"}
