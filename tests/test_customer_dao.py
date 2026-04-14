import pytest
from datetime import date
from src.dao.customer_dao import Customer, CustomerDAO

dao = CustomerDAO()

# sample customer used across tests
SAMPLE = Customer(
    first_name="Jane",
    last_name="Doe",
    date_of_birth=date(1990, 5, 15),
    phone_number="555-1234",
    email="jane.doe@test.com",
    street="123 Main St",
    city="State College",
    state="PA",
    apartment_number="4B",
    zipcode="16801"
)

@pytest.fixture(autouse=True)
def cleanup():
    """Remove test customer by email before and after each test."""
    _delete_by_email(SAMPLE.email)
    yield
    _delete_by_email(SAMPLE.email)

def _delete_by_email(email):
    results = dao.search(email)
    for c in results:
        dao.remove(c.customer_id)


def test_add_and_find():
    dao.add(SAMPLE)
    results = dao.search(SAMPLE.email)
    assert len(results) == 1
    c = results[0]
    assert c.first_name == "Jane"
    assert c.last_name == "Doe"
    assert c.email == "jane.doe@test.com"


def test_get_all_contains_added():
    dao.add(SAMPLE)
    all_customers = dao.get_all()
    emails = [c.email for c in all_customers]
    assert SAMPLE.email in emails


def test_find_by_id():
    dao.add(SAMPLE)
    results = dao.search(SAMPLE.email)
    cid = results[0].customer_id
    found = dao.find_by_id(cid)
    assert found is not None
    assert found.customer_id == cid
    assert found.first_name == "Jane"


def test_find_by_id_not_found():
    result = dao.find_by_id(-1)
    assert result is None


def test_update():
    dao.add(SAMPLE)
    results = dao.search(SAMPLE.email)
    c = results[0]
    c.first_name = "Janet"
    c.phone_number = "555-9999"
    dao.update(c)
    updated = dao.find_by_id(c.customer_id)
    assert updated.first_name == "Janet"
    assert updated.phone_number == "555-9999"


def test_remove():
    dao.add(SAMPLE)
    results = dao.search(SAMPLE.email)
    cid = results[0].customer_id
    dao.remove(cid)
    assert dao.find_by_id(cid) is None


def test_search_by_first_name():
    dao.add(SAMPLE)
    results = dao.search("jane")
    assert any(c.email == SAMPLE.email for c in results)


def test_search_no_results():
    results = dao.search("zzznomatch999")
    assert results == []
