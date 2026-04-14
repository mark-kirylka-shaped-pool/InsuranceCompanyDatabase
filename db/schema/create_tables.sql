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