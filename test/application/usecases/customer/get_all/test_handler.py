from application.usecases.customer.get_all.command import Command
from application.usecases.customer.get_all.handler import Handler
from application.usecases.customer.get_all.response import Response
from test.configuration.fake_data import CustomerFactory


async def test_handler_get_all_customers_success(session, customer_repository):
    # arrange
    handler = Handler(customer_repository)
    baseline = await handler.handle(Command(skip=0, take=10_000))

    customers = CustomerFactory.create_batch(3)
    session.add_all(customers)
    await session.commit()

    # act
    result = await handler.handle(Command(skip=0, take=10_000))

    # assert
    assert len(result) == len(baseline) + 3
    assert all(isinstance(item, Response) for item in result)
    result_ids = {item.id for item in result}
    assert {customer.id for customer in customers} <= result_ids


async def test_handler_get_all_customers_respects_take_limit(
    session, customer_repository
):
    # arrange
    handler = Handler(customer_repository)

    # act
    result = await handler.handle(Command(skip=0, take=2))

    # assert
    assert len(result) == 2
