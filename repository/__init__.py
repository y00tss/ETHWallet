from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Generic, TypeVar, List, Type
from fastapi import HTTPException

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self, user_id) -> List[T]:
        """Related to User"""
        result = await self.session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_id(self, id: int, user_id: int) -> T:
        result = await self.session.execute(
            select(self.model).where(
                self.model.id == id, self.model.user_id == user_id
            ))
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} with id {id} not found"
            )
        return obj

    async def create(self, obj_data: dict) -> T:
        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, values: dict) -> T:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} with id {id} not found"
            )
        for key, value in values.items():
            setattr(obj, key, value)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: int, user_id: int) -> None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id, self.model.user_id == user_id)
        )
        obj = result.scalars().first()
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} with id {id} not found"
            )
        await self.session.delete(obj)
        await self.session.commit()
