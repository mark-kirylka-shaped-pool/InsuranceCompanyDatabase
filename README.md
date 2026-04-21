

# Insurance Company Management System
CMPSC 430 – Spring 2026, Project A

A staff-facing application to manage insurance policies backed by an Oracle database.

## Database Tables

- **Customer** – stores customer personal information
- **Policy** – base policy record linked to a customer
- **HomeInsurance** – home policy details linked to a policy
- **CarInsurance** – car policy details linked to a policy
- **LifeInsurance** – life policy details linked to a policy

## ER Diagram

![Alt text](https://github.com/mark-kirylka-shaped-pool/InsuranceCompanyDatabase/img/erdiagram.jpg?raw=true "ER Diagram")

## Features

Staff can perform the following operations through the UI:

- Add / edit / remove / search customers
- Browse the full customer list
- Add / edit / remove home, car, or life insurance policies for a customer
- Browse and search insurance policies
- View all policies belonging to a specific customer

## Project Structure

```
insurance-management-system/
├── src/
│   ├── domain/          # Entity classes (Customer, HomeInsurance, CarInsurance, LifeInsurance)
│   ├── dao/             # Data access objects + Oracle DB connection
│   ├── service/         # Business logic
│   └── ui/              # Frontend (CLI or GUI)
├── db/
│   ├── er_diagram/      # ER diagram files
│   ├── schema/          # DDL scripts (CREATE TABLE)
│   └── seed/            # Sample INSERT scripts
├── docs/                # Project documentation
└── tests/               # Unit and integration tests
```

## Tech Stack

- Language: Java or Python
- Database: Oracle
- UI: CLI or optional GUI (JavaFX / Tkinter)

## DAO Documentation

The repository includes data access objects in `src/dao/` for interacting with the Oracle database.

### `src/dao/customer_dao.py`

- `Customer`
  - Entity representing a customer record.
  - Fields: `customer_id`, `first_name`, `last_name`, `date_of_birth`, `phone_number`, `email`, `street`, `city`, `state`, `apartment_number`, `zipcode`.
- `CustomerDAO`
  - `add(customer)` - insert a new customer record.
  - `get_all()` - return all customers as `Customer` objects.
  - `find_by_id(customer_id)` - return a `Customer` by primary key or `None`.
  - `update(customer)` - update an existing customer record.
  - `remove(customer_id)` - delete a customer by ID.
  - `search(query)` - search customers by first name, last name, or email (case-insensitive substring match).

### `src/dao/policy_dao.py`

- `Policy`
  - Entity representing an insurance policy.
  - Fields: `policy_id`, `customer_id`, `monthly_payment`, `start_date`, `coverage`.
- `PolicyDAO`
  - `add(policy)` - insert a new policy record.
  - `get_all()` - return all policies as `Policy` objects.
  - `find_by_id(policy_id)` - return a `Policy` by primary key or `None`.
  - `get_by_customer(customer_id)` - return all policies for a specific customer.
  - `update(policy)` - update an existing policy record.
  - `remove(policy_id)` - delete a policy by ID.

### Insurance type DAO placeholders

The repository also includes conceptual placeholders for the three insurance-specific DAO types.

#### `src/dao/home_insurance_dao.py  NOT IMPLIMENTED`

- `HomeInsurance`
  - Entity representing a home insurance policy record.
- `HomeInsuranceDAO`
  - `add(home_insurance)` - insert a new home insurance record.
  - `get_all()` - return all home insurance records.
  - `find_by_id(home_insurance_id)` - return a home insurance record by ID.
  - `get_by_policy(policy_id)` - return home insurance details for a specific policy.
  - `update(home_insurance)` - update an existing home insurance record.
  - `remove(home_insurance_id)` - delete a home insurance record by ID.

#### `src/dao/car_insurance_dao.py  NOT IMPLIMENTED`

- `CarInsurance`
  - Entity representing a car insurance policy record.
- `CarInsuranceDAO`
  - `add(car_insurance)` - insert a new car insurance record.
  - `get_all()` - return all car insurance records.
  - `find_by_id(car_insurance_id)` - return a car insurance record by ID.
  - `get_by_policy(policy_id)` - return car insurance details for a specific policy.
  - `update(car_insurance)` - update an existing car insurance record.
  - `remove(car_insurance_id)` - delete a car insurance record by ID.

#### `src/dao/life_insurance_dao.py  NOT IMPLIMENTED`

- `LifeInsurance`
  - Entity representing a life insurance policy record.
- `LifeInsuranceDAO`
  - `add(life_insurance)` - insert a new life insurance record.
  - `get_all()` - return all life insurance records.
  - `find_by_id(life_insurance_id)` - return a life insurance record by ID.
  - `get_by_policy(policy_id)` - return life insurance details for a specific policy.
  - `update(life_insurance)` - update an existing life insurance record.
  - `remove(life_insurance_id)` - delete a life insurance record by ID.

Both DAOs use `db.schema.db_connection.get_connection()` to establish a connection to Oracle.
