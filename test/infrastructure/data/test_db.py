import uuid

from domain.entities.customer import Customers


def test_insert_data_into_db(session):
    id = uuid.uuid4()

    costumer = Customers(
        id=id,
        name='John Doe',
        email='john.doe@example.com',
        phone='1234567890',
    )

    session.add(costumer)
    session.commit()

    new_data = session.get(Customers, id)

    assert new_data is not None
    assert new_data.id == id
    assert new_data.name == 'John Doe'
    assert new_data.email == 'john.doe@example.com'
    assert new_data.phone == '1234567890'
