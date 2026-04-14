import pytest
from datetime import date
from src.dao.customer_dao import Customer, CustomerDAO
from src.dao.policy_dao import Policy, PolicyDAO

customer_dao = CustomerDAO()
policy_dao = PolicyDAO()

SAMPLE_CUSTOMER = Customer(
    first_name="Test",
    last_name="User",
    date_of_birth=date(1985, 3, 20),
    phone_number="555-0000",
    email="test.policy.user@test.com",
    street="456 Elm St",
    city="State College",
    state="PA",
    apartment_number=None,
    zipcode="16802"
)


@pytest.fixture(scope="module")
def customer_id():
    """Create a customer once for all policy tests, remove after."""
    _delete_customer()
    customer_dao.add(SAMPLE_CUSTOMER)
    results = customer_dao.search(SAMPLE_CUSTOMER.email)
    cid = results[0].customer_id
    yield cid
    # cleanup: remove policies then customer
    for p in policy_dao.get_by_customer(cid):
        policy_dao.remove(p.policy_id)
    customer_dao.remove(cid)


def _delete_customer():
    results = customer_dao.search(SAMPLE_CUSTOMER.email)
    for c in results:
        for p in policy_dao.get_by_customer(c.customer_id):
            policy_dao.remove(p.policy_id)
        customer_dao.remove(c.customer_id)


def _make_policy(customer_id):
    return Policy(
        customer_id=customer_id,
        monthly_payment=150.00,
        start_date=date(2024, 1, 1),
        coverage=50000.00
    )


def test_add_and_get_by_customer(customer_id):
    p = _make_policy(customer_id)
    policy_dao.add(p)
    results = policy_dao.get_by_customer(customer_id)
    assert len(results) >= 1
    assert any(r.coverage == 50000.00 for r in results)


def test_get_all_contains_added(customer_id):
    p = _make_policy(customer_id)
    policy_dao.add(p)
    all_policies = policy_dao.get_all()
    customer_ids = [p.customer_id for p in all_policies]
    assert customer_id in customer_ids


def test_find_by_id(customer_id):
    p = _make_policy(customer_id)
    policy_dao.add(p)
    results = policy_dao.get_by_customer(customer_id)
    pid = results[0].policy_id
    found = policy_dao.find_by_id(pid)
    assert found is not None
    assert found.policy_id == pid
    assert found.customer_id == customer_id


def test_find_by_id_not_found():
    result = policy_dao.find_by_id(-1)
    assert result is None


def test_update(customer_id):
    p = _make_policy(customer_id)
    policy_dao.add(p)
    results = policy_dao.get_by_customer(customer_id)
    pol = results[0]
    pol.monthly_payment = 200.00
    pol.coverage = 75000.00
    policy_dao.update(pol)
    updated = policy_dao.find_by_id(pol.policy_id)
    assert updated.monthly_payment == 200.00
    assert updated.coverage == 75000.00


def test_remove(customer_id):
    p = _make_policy(customer_id)
    policy_dao.add(p)
    results = policy_dao.get_by_customer(customer_id)
    pid = results[0].policy_id
    policy_dao.remove(pid)
    assert policy_dao.find_by_id(pid) is None
