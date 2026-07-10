import factory

from domain.entities.customer import Customers
from domain.entities.user import Users
from infrastructure.security.password import hash_password


class UserFactory(factory.Factory):  # type: ignore
    class Meta:
        model = Users

    class Params:
        password = 'hashed_password'  # type: ignore

    name = factory.Faker('name')  # type: ignore
    email = factory.Faker('email')  # type: ignore
    hashed_password = factory.LazyAttribute(  # type: ignore
        lambda p: hash_password(p.password)
    )  # type: ignore
    role = factory.Faker(  # type: ignore
        'random_element',
        elements=['admin', 'seller', 'purchaser', 'stock_clerk'],
    )


class CustomerFactory(factory.Factory):  # type: ignore
    class Meta:
        model = Customers

    name = factory.Faker('name')  # type: ignore
    email = factory.Faker('email')  # type: ignore
    phone = factory.Sequence(lambda n: f'119{n:08d}')  # type: ignore
