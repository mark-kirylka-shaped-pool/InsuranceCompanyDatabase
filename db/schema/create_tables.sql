CREATE TABLE customer (
    customer_id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name       VARCHAR2(50)  NOT NULL,
    last_name        VARCHAR2(50)  NOT NULL,
    date_of_birth    DATE,
    phone_number     VARCHAR2(20),
    email            VARCHAR2(100),
    street           VARCHAR2(100),
    city             VARCHAR2(50),
    state            VARCHAR2(2),
    apartment_number VARCHAR2(10),
    zipcode          VARCHAR2(10)
);

CREATE TABLE policy (
    policy_id        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id      NUMBER NOT NULL REFERENCES customer(customer_id),
    monthly_payment  NUMBER(10,2),
    start_date       DATE,
    coverage         NUMBER(12,2)
);

CREATE TABLE car_insurance (
    car_id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    policy_id       NUMBER NOT NULL,
    end_date        DATE,
    make            VARCHAR2(50),
    model           VARCHAR2(50),
    vin             VARCHAR2(50) UNIQUE,
    yearly_mileage  NUMBER,

    CONSTRAINT fk_car_policy
        FOREIGN KEY (policy_id)
        REFERENCES policy(policy_id)
        ON DELETE CASCADE
);

CREATE TABLE life_insurance (
    life_id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    policy_id            NUMBER NOT NULL,
    existing_conditions  CLOB,
    beneficiary          VARCHAR2(100),

    CONSTRAINT fk_life_policy
        FOREIGN KEY (policy_id)
        REFERENCES policy(policy_id)
        ON DELETE CASCADE
);

CREATE TABLE home_insurance (
    house_id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    policy_id         NUMBER NOT NULL,
    end_date          DATE,
    house_price       NUMBER(12,2),
    house_area        NUMBER,
    bedroom_number    NUMBER,
    bathroom_number   NUMBER,
    street            VARCHAR2(100),
    city              VARCHAR2(50),
    state             VARCHAR2(2),
    apartment_number  VARCHAR2(10),
    zip_code          VARCHAR2(10),

    CONSTRAINT fk_home_policy
        FOREIGN KEY (policy_id)
        REFERENCES policy(policy_id)
        ON DELETE CASCADE
);