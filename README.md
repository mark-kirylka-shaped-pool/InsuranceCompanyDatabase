# Insurance Company Management System
CMPSC 430 – Spring 2026, Project A

A staff-facing application to manage insurance policies backed by an Oracle database.

## Database Tables

- **Customer** – stores customer personal information
- **Policy** – base policy record linked to a customer
- **HomeInsurance** – home policy details linked to a policy
- **CarInsurance** – car policy details linked to a policy
- **LifeInsurance** – life policy details linked to a policy

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
