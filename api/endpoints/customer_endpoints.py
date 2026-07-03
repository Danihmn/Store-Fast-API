import uuid
from http import HTTPStatus
from typing import Annotated

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
from dependencies import (
    get_customer_by_id_handler,
    get_customer_create_handler,
    get_customer_delete_handler,
    get_customer_get_all_handler,
    get_customer_update_handler,
)
from infrastructure.security.token import get_current_user

router = APIRouter(
    prefix='/customer',
)


@router.get(
    '/', response_model=list[GetAllResponse], response_class=JSONResponse
)
def get_customers(
    command: Annotated[GetAllCommand, Query()],
    handler: Annotated[GetAllHandler, Depends(get_customer_get_all_handler)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    return handler.handle(command)


@router.get(
    '/{customer_id}',
    response_model=GetByIdResponse,
    response_class=JSONResponse,
)
def get_customer_by_id(
    command: Annotated[GetByIdCommand, Path()],
    handler: Annotated[GetByIdHandler, Depends(get_customer_by_id_handler)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    return handler.handle(command)


@router.post(
    '/create',
    response_model=CreateResponse,
    response_class=JSONResponse,
    status_code=HTTPStatus.CREATED,
)
def create_customer(
    command: CreateCommand,
    handler: Annotated[CreateHandler, Depends(get_customer_create_handler)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    return handler.handle(command)


@router.put(
    '/{customer_id}',
    response_model=UpdateResponse,
    response_class=JSONResponse,
)
def update_customer(
    customer_id: Annotated[uuid.UUID, Path()],
    command: Annotated[UpdateCommand, Body()],
    handler: Annotated[UpdateHandler, Depends(get_customer_update_handler)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    return handler.handle(customer_id, command)


@router.delete(
    '/{customer_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_customer(
    command: Annotated[DeleteCommand, Path()],
    handler: Annotated[DeleteHandler, Depends(get_customer_delete_handler)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource',
        )

    handler.handle(command)
