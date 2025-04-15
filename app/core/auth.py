from fastapi import Depends, HTTPException
from jwt import DecodeError, decode
from starlette import status

from core.config import settings
from core.security import oauth2_scheme
from core.utils.unit_of_work import CachedSQLAlchemyUnitOfWork


# from app.services.user import UserService


async def get_current_user(
        uow=Depends(CachedSQLAlchemyUnitOfWork), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.security.secret_key, algorithms=[settings.security.algorithm]
        )
        email = payload.get("sub")

        if email is None:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = await UserService().get_user_by_email(uow, email)

    if user is None:
        raise credentials_exception

    return user


async def get_admin_user(
        uow=Depends(CachedSQLAlchemyUnitOfWork), token: str = Depends(oauth2_scheme)
):
    user = await get_current_user(uow, token)

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted",
        )

    return user
