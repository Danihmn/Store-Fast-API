import uuid
from http import HTTPStatus
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from fastapi.responses import JSONResponse

from application.usecases.customer import (
    CreateCommand,
    CreateHandler,
    CreateResponse,
    DeleteCommand,
    DeleteHandler,
    GetAllCommand,
    GetAllHandler,
    GetAllResponse,
    GetByIdCommand,
    GetByIdHandler,
    GetByIdResponse,
    UpdateCommand,
    UpdateHandler,
    UpdateResponse,
)
from infrastructure.dependency_injection.container import Container
from infrastructure.security.token import get_current_user

router = APIRouter(
    prefix='/customers',
)


@router.get(
    '/', response_model=list[GetAllResponse], response_class=JSONResponse
)
@inject
async def get_customers(
    command: Annotated[GetAllCommand, Query()],
    handler: Annotated[
        GetAllHandler, Depends(Provide[Container.customer_get_all_handler])
    ],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    return await handler.handle(command)


@router.get(
    '/{customer_id}',
    response_model=GetByIdResponse,
    response_class=JSONResponse,
)
@inject
async def get_customer_by_id(
    command: Annotated[GetByIdCommand, Path()],
    handler: Annotated[
        GetByIdHandler, Depends(Provide[Container.customer_get_by_id_handler])
    ],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    return await handler.handle(command)


@router.post(
    '/create',
    response_model=CreateResponse,
    response_class=JSONResponse,
    status_code=HTTPStatus.CREATED,
)
@inject
async def create_customer(
    command: CreateCommand,
    handler: Annotated[
        CreateHandler, Depends(Provide[Container.customer_create_handler])
    ],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    return await handler.handle(command)


@router.put(
    '/{customer_id}',
    response_model=UpdateResponse,
    response_class=JSONResponse,
)
@inject
async def update_customer(
    customer_id: Annotated[uuid.UUID, Path()],
    command: Annotated[UpdateCommand, Body()],
    handler: Annotated[
        UpdateHandler, Depends(Provide[Container.customer_update_handler])
    ],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    return await handler.handle(customer_id, command)


@router.delete(
    '/{customer_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
@inject
async def delete_customer(
    command: Annotated[DeleteCommand, Path()],
    handler: Annotated[
        DeleteHandler, Depends(Provide[Container.customer_delete_handler])
    ],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    await handler.handle(command)
