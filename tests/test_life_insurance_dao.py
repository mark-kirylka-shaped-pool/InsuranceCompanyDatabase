import pytest
from datetime import date

from src.dao.customer_dao import Customer, CustomerDAO
from src.dao.policy_dao import Policy, PolicyDAO
from src.dao.life_insurance_dao import LifeInsurance, LifeInsuranceDAO

customer_dao = CustomerDAO()
policy_dao = PolicyDAO()
life_dao = LifeInsuranceDAO()

SAMPLE_CUSTOMER = Customer(
    first_name="Life",
    last_name="Tester",
    date_of_birth=date(1980, 1, 1),
    phone_number="555-3333",
    email="life.insurance@test.com",
    street="99 Life St",
    city="LifeCity",
    state="PA",
    apartment_number=None,
    zipcode="17002"
)


@pytest.fixture(scope="module")
def policy_id():
    _cleanup()

    customer_dao.add(SAMPLE_CUSTOMER)
    cid = customer_dao.search(SAMPLE_CUSTOMER.email)[0].customer_id

    policy = Policy(
        customer_id=cid,
        monthly_payment=300.00,
        start_date=date(2024, 1, 1),
        coverage=500000.00
    )

    policy_dao.add(policy)
    pid = policy_dao.get_by_customer(cid)[0].policy_id

    yield pid

    for l in life_dao.get_by_policy(pid):
        life_dao.remove(l.life_id)
    policy_dao.remove(pid)
    customer_dao.remove(cid)


def _cleanup():
    for c in customer_dao.search(SAMPLE_CUSTOMER.email):
        for p in policy_dao.get_by_customer(c.customer_id):
            for l in life_dao.get_by_policy(p.policy_id):
                life_dao.remove(l.life_id)
            policy_dao.remove(p.policy_id)
        customer_dao.remove(c.customer_id)


def _make_life(policy_id):
    return LifeInsurance(
        policy_id=policy_id,
        existing_conditions="None",
        beneficiary="John Doe"
    )


def test_add_and_get(policy_id):
    life = _make_life(policy_id)
    life_dao.add(life)

    results = life_dao.get_by_policy(policy_id)
    assert len(results) >= 1
    assert results[0].beneficiary == "John Doe"


def test_find_by_id(policy_id):
    life = _make_life(policy_id)
    life_dao.add(life)

    record = life_dao.get_by_policy(policy_id)[0]
    found = life_dao.find_by_id(record.life_id)

    assert found is not None
    assert found.life_id == record.life_id


def test_update(policy_id):
    life = _make_life(policy_id)
    life_dao.add(life)

    record = life_dao.get_by_policy(policy_id)[0]
    record.beneficiary = "Jane Doe"

    life_dao.update(record)

    updated = life_dao.find_by_id(record.life_id)
    assert updated.beneficiary == "Jane Doe"


def test_remove(policy_id):
    life = _make_life(policy_id)
    life_dao.add(life)

    record = life_dao.get_by_policy(policy_id)[0]
    life_dao.remove(record.life_id)

    assert life_dao.find_by_id(record.life_id) is None