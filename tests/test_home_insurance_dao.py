import pytest
from datetime import date

from src.dao.customer_dao import Customer, CustomerDAO
from src.dao.policy_dao import Policy, PolicyDAO
from src.dao.home_insurance_dao import HomeInsurance, HomeInsuranceDAO

customer_dao = CustomerDAO()
policy_dao = PolicyDAO()
home_dao = HomeInsuranceDAO()

SAMPLE_CUSTOMER = Customer(
    first_name="Home",
    last_name="Tester",
    date_of_birth=date(1990, 1, 1),
    phone_number="555-2222",
    email="home.insurance@test.com",
    street="10 House Rd",
    city="HomeCity",
    state="PA",
    apartment_number=None,
    zipcode="17001"
)


@pytest.fixture(scope="module")
def policy_id():
    _cleanup()

    customer_dao.add(SAMPLE_CUSTOMER)
    cid = customer_dao.search(SAMPLE_CUSTOMER.email)[0].customer_id

    policy = Policy(
        customer_id=cid,
        monthly_payment=200.00,
        start_date=date(2024, 1, 1),
        coverage=100000.00
    )

    policy_dao.add(policy)
    pid = policy_dao.get_by_customer(cid)[0].policy_id

    yield pid

    for h in home_dao.get_by_policy(pid):
        home_dao.remove(h.house_id)
    policy_dao.remove(pid)
    customer_dao.remove(cid)


def _cleanup():
    for c in customer_dao.search(SAMPLE_CUSTOMER.email):
        for p in policy_dao.get_by_customer(c.customer_id):
            for h in home_dao.get_by_policy(p.policy_id):
                home_dao.remove(h.house_id)
            policy_dao.remove(p.policy_id)
        customer_dao.remove(c.customer_id)


def _make_home(policy_id):
    return HomeInsurance(
        policy_id=policy_id,
        end_date=date(2026, 1, 1),
        house_price=350000,
        house_area=2000,
        bedroom_number=3,
        bathroom_number=2,
        street="10 House Rd",
        city="HomeCity",
        state="PA",
        apartment_number=None,
        zip_code="17001"
    )


def test_add_and_get(policy_id):
    home = _make_home(policy_id)
    home_dao.add(home)

    results = home_dao.get_by_policy(policy_id)
    assert len(results) >= 1
    assert results[0].city == "HomeCity"


def test_find_by_id(policy_id):
    home = _make_home(policy_id)
    home_dao.add(home)

    record = home_dao.get_by_policy(policy_id)[0]
    found = home_dao.find_by_id(record.house_id)

    assert found is not None
    assert found.house_id == record.house_id


def test_update(policy_id):
    home = _make_home(policy_id)
    home_dao.add(home)

    record = home_dao.get_by_policy(policy_id)[0]
    record.house_price = 400000
    record.bedroom_number = 4

    home_dao.update(record)

    updated = home_dao.find_by_id(record.house_id)
    assert updated.house_price == 400000
    assert updated.bedroom_number == 4


def test_remove(policy_id):
    home = _make_home(policy_id)
    home_dao.add(home)

    record = home_dao.get_by_policy(policy_id)[0]
    home_dao.remove(record.house_id)

    assert home_dao.find_by_id(record.house_id) is None