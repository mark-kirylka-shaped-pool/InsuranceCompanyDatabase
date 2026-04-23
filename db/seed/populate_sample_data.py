#!/usr/bin/env python3
"""
Populate the insurance database with sample data for testing.
Run this script from the project root: python db/seed/populate_sample_data.py
"""

import sys
from pathlib import Path
from datetime import datetime, date, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.dao.customer_dao import Customer, CustomerDAO
from src.dao.policy_dao import Policy, PolicyDAO
from src.dao.car_insurance_dao import CarInsurance, CarInsuranceDAO
from src.dao.home_insurance_dao import HomeInsurance, HomeInsuranceDAO
from src.dao.life_insurance_dao import LifeInsurance, LifeInsuranceDAO


def main():
    print("🌱 Seeding database with sample data...\n")
    
    # Initialize DAOs
    customer_dao = CustomerDAO()
    policy_dao = PolicyDAO()
    car_dao = CarInsuranceDAO()
    home_dao = HomeInsuranceDAO()
    life_dao = LifeInsuranceDAO()
    
    # === SAMPLE CUSTOMERS ===
    print("📝 Creating sample customers...")
    
    customers = [
        Customer(
            first_name="John",
            last_name="Smith",
            date_of_birth=date(1985, 3, 15),
            phone_number="555-0101",
            email="john.smith@email.com",
            street="123 Main St",
            city="Springfield",
            state="IL",
            apartment_number=None,
            zipcode="62701"
        ),
        Customer(
            first_name="Sarah",
            last_name="Johnson",
            date_of_birth=date(1990, 7, 22),
            phone_number="555-0102",
            email="sarah.j@email.com",
            street="456 Oak Ave",
            city="Chicago",
            state="IL",
            apartment_number="201",
            zipcode="60601"
        ),
        Customer(
            first_name="Michael",
            last_name="Williams",
            date_of_birth=date(1978, 11, 8),
            phone_number="555-0103",
            email="m.williams@email.com",
            street="789 Elm Lane",
            city="Naperville",
            state="IL",
            apartment_number=None,
            zipcode="60540"
        ),
        Customer(
            first_name="Emily",
            last_name="Brown",
            date_of_birth=date(1995, 5, 30),
            phone_number="555-0104",
            email="emily.brown@email.com",
            street="321 Pine Road",
            city="Evanston",
            state="IL",
            apartment_number="105",
            zipcode="60201"
        ),
    ]
    
    customer_ids = []
    for customer in customers:
        customer_dao.add(customer)
        print(f"  ✓ Added {customer.first_name} {customer.last_name}")
    
    # Retrieve customer IDs
    all_customers = customer_dao.get_all()
    customer_ids = [c.customer_id for c in all_customers]
    print(f"  Total customers: {len(all_customers)}\n")
    
    # === SAMPLE POLICIES ===
    print("📋 Creating sample policies...")
    
    policy_data = [
        (customer_ids[0], 125.50, date(2023, 1, 15), 50000),      # John - Car insurance
        (customer_ids[0], 89.00, date(2023, 3, 20), 300000),      # John - Home insurance
        (customer_ids[1], 45.00, date(2023, 6, 10), 500000),      # Sarah - Life insurance
        (customer_ids[1], 150.00, date(2023, 8, 5), 35000),       # Sarah - Car insurance
        (customer_ids[2], 200.00, date(2022, 11, 1), 250000),     # Michael - Home insurance
        (customer_ids[2], 55.00, date(2023, 2, 14), 1000000),     # Michael - Life insurance
        (customer_ids[3], 120.00, date(2023, 9, 1), 40000),       # Emily - Car insurance
    ]
    
    policy_ids = []
    for customer_id, monthly_payment, start_date, coverage in policy_data:
        policy = Policy(
            customer_id=customer_id,
            monthly_payment=monthly_payment,
            start_date=start_date,
            coverage=coverage
        )
        policy_dao.add(policy)
        print(f"  ✓ Added policy for customer {customer_id}: ${monthly_payment}/month")
    
    all_policies = policy_dao.get_all()
    policy_ids = [p.policy_id for p in all_policies]
    print(f"  Total policies: {len(all_policies)}\n")
    
    # === SAMPLE CAR INSURANCE ===
    print("🚗 Creating sample car insurance records...")
    
    car_data = [
        (policy_ids[0], date(2026, 1, 15), "Honda", "Civic", "JH2RT5H49LM219186", 12000),
        (policy_ids[3], date(2025, 8, 5), "Toyota", "Camry", "4T1C1F1M5JU521447", 8500),
        (policy_ids[6], date(2026, 9, 1), "Ford", "F-150", "1FTFW1ET5DFC12345", 15000),
    ]
    
    for policy_id, end_date, make, model, vin, mileage in car_data:
        car = CarInsurance(
            policy_id=policy_id,
            end_date=end_date,
            make=make,
            model=model,
            vin=vin,
            yearly_mileage=mileage
        )
        car_dao.add(car)
        print(f"  ✓ Added {make} {model} ({vin})")
    
    print()
    
    # === SAMPLE HOME INSURANCE ===
    print("🏡 Creating sample home insurance records...")
    
    home_data = [
        (policy_ids[1], date(2026, 3, 20), 450000, 2500, 4, 2.5, "456 Oak Ave", "Chicago", "IL", "201", "60601"),
        (policy_ids[4], date(2025, 11, 1), 325000, 1800, 3, 2, "789 Elm Lane", "Naperville", "IL", None, "60540"),
    ]
    
    for policy_id, end_date, price, area, bedrooms, bathrooms, street, city, state, apt, zipcode in home_data:
        home = HomeInsurance(
            policy_id=policy_id,
            end_date=end_date,
            house_price=price,
            house_area=area,
            bedroom_number=bedrooms,
            bathroom_number=bathrooms,
            street=street,
            city=city,
            state=state,
            apartment_number=apt,
            zip_code=zipcode
        )
        home_dao.add(home)
        print(f"  ✓ Added home in {city}, ${price:,}")
    
    print()
    
    # === SAMPLE LIFE INSURANCE ===
    print("💚 Creating sample life insurance records...")
    
    life_data = [
        (policy_ids[2], "None", "Maria Johnson"),
        (policy_ids[5], "Diabetes, controlled with medication", "Robert Williams"),
    ]
    
    for policy_id, conditions, beneficiary in life_data:
        life = LifeInsurance(
            policy_id=policy_id,
            existing_conditions=conditions,
            beneficiary=beneficiary
        )
        life_dao.add(life)
        print(f"  ✓ Added life insurance for beneficiary: {beneficiary}")
    
    print()
    print("✅ Database seeding complete!")
    print(f"\n📊 Summary:")
    print(f"   • Customers: {len(all_customers)}")
    print(f"   • Policies: {len(all_policies)}")
    print(f"   • Car insurance records: {len(car_data)}")
    print(f"   • Home insurance records: {len(home_data)}")
    print(f"   • Life insurance records: {len(life_data)}")


if __name__ == "__main__":
    main()
