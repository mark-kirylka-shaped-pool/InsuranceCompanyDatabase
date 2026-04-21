import pytest
from datetime import date

from src.dao.customer_dao import Customer, CustomerDAO
from src.dao.policy_dao import Policy, PolicyDAO
from src.dao.car_insurance_dao import CarInsurance, CarInsuranceDAO

customer_dao = CustomerDAO()
policy_dao = PolicyDAO()
car_dao = CarInsuranceDAO()

SAMPLE_CUSTOMER = Customer(
    first_name="Car",
    last_name="Tester",
    date_of_birth=date(1992, 6, 10),
    phone_number="555-1111",
    email="car.insurance@test.com",
    street="1 Test St",
    city="Testville",
    state="PA",
    apartment_number=None,
    zipcode="17000"
)


@pytest.fixture(scope="module")
def policy_id():
    _cleanup()

    customer_dao.add(SAMPLE_CUSTOMER)
    cid = customer_dao.search(SAMPLE_CUSTOMER.email)[0].customer_id

    policy = Policy(
        customer_id=cid,
        monthly_payment=120.00,
        start_date=date(2024, 1, 1),
        coverage=25000.00
    )

    policy_dao.add(policy)
    pid = policy_dao.get_by_customer(cid)[0].policy_id

    yield pid

    # cleanup
    for c in car_dao.get_by_policy(pid):
        car_dao.remove(c.car_id)
    policy_dao.remove(pid)
    customer_dao.remove(cid)


def _cleanup():
    for c in customer_dao.search(SAMPLE_CUSTOMER.email):
        for p in policy_dao.get_by_customer(c.customer_id):
            for car in car_dao.get_by_policy(p.policy_id):
                car_dao.remove(car.car_id)
            policy_dao.remove(p.policy_id)
        customer_dao.remove(c.customer_id)


def _make_car(policy_id):
    return CarInsurance(
        policy_id=policy_id,
        end_date=date(2026, 1, 1),
        make="Toyota",
        model="Camry",
        vin="VIN123456TEST",
        yearly_mileage=12000
    )


def test_add_and_get_by_policy(policy_id):
    car = _make_car(policy_id)
    car_dao.add(car)

    results = car_dao.get_by_policy(policy_id)
    assert len(results) >= 1
    assert any(r.vin == "VIN123456TEST" for r in results)


def test_find_by_id(policy_id):
    car = _make_car(policy_id)
    car_dao.add(car)

    record = car_dao.get_by_policy(policy_id)[0]
    found = car_dao.find_by_id(record.car_id)

    assert found is not None
    assert found.car_id == record.car_id
    assert found.make == "Toyota"


def test_update(policy_id):
    car = _make_car(policy_id)
    car_dao.add(car)

    record = car_dao.get_by_policy(policy_id)[0]
    record.model = "Corolla"
    record.yearly_mileage = 15000

    car_dao.update(record)

    updated = car_dao.find_by_id(record.car_id)
    assert updated.model == "Corolla"
    assert updated.yearly_mileage == 15000


def test_remove(policy_id):
    car = _make_car(policy_id)
    car_dao.add(car)

    record = car_dao.get_by_policy(policy_id)[0]
    car_dao.remove(record.car_id)

    assert car_dao.find_by_id(record.car_id) is None