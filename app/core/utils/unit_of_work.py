from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING

import fakeredis
from database.redis import RedisSingleton
from database.session import get_db
from fakeredis import TcpFakeServer
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.utils import SQLAlchemyRepository
from core.utils.cache import RedisCache
from core.utils.repository import AbstractRepository

if TYPE_CHECKING:
    from repositories.contest import ContestRepository
    from repositories.problem import ProblemRepository
    from repositories.test_case import TestCaseRepository
    from repositories.submission import SubmissionRepository


class AbstractUnitOfWork(ABC):
    batches: AbstractRepository

    @abstractmethod
    def __init__(self, session_factory):
        raise NotImplementedError

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class CachedSQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        session_factory=Depends(get_db),
    ):
        self.session_factory = session_factory
        self.redis = fakeredis.FakeAsyncRedis()

    def get_repository(self, repo_class):
        return repo_class(
            repository=SQLAlchemyRepository(self.session), cache=RedisCache(self.redis)
        )

    async def __aenter__(self):
        self.session: AsyncSession = await anext(self.session_factory())

        # Import repository classes only when needed
        from blog_service.app.repositories.post import PostRepository
        from blog_service.app.repositories.comment import CommentRepository
        from blog_service.app.repositories.tag import TagRepository
        from blog_service.app.repositories.post_tag import PostTagRepository
        from blog_service.app.repositories.category import CategoryRepository
        from blog_service.app.repositories.post_category import PostCategoryRepository

        # Initialize repositories
        self.posts = self.get_repository(PostRepository)
        self.comments = self.get_repository(CommentRepository)
        self.tags = self.get_repository(TagRepository)
        self.post_tags = self.get_repository(PostTagRepository)
        self.categories = self.get_repository(CategoryRepository)
        self.post_categories = self.get_repository(PostCategoryRepository)

        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self.session:
                await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
