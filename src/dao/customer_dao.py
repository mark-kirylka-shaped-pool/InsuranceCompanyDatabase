from db.schema.db_connection import get_connection


class Customer:
    def __init__(self, first_name, last_name, date_of_birth, phone_number,
                 email, street, city, state, apartment_number, zipcode, customer_id=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.email = email
        self.street = street
        self.city = city
        self.state = state
        self.apartment_number = apartment_number
        self.zipcode = zipcode

    @staticmethod
    def from_row(row):
        """Build a Customer from a DB row tuple."""
        return Customer(
            customer_id=row[0],
            first_name=row[1],
            last_name=row[2],
            date_of_birth=row[3],
            phone_number=row[4],
            email=row[5],
            street=row[6],
            city=row[7],
            state=row[8],
            apartment_number=row[9],
            zipcode=row[10]
        )

    def __repr__(self):
        return f"Customer({self.customer_id}: {self.first_name} {self.last_name})"


class CustomerDAO:
    def add(self, customer: Customer):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO customer (first_name, last_name, date_of_birth, phone_number,
                                         email, street, city, state, apartment_number, zipcode)
                    VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
                """, (customer.first_name, customer.last_name, customer.date_of_birth,
                      customer.phone_number, customer.email, customer.street,
                      customer.city, customer.state, customer.apartment_number, customer.zipcode))
                conn.commit()

    def get_all(self) -> list[Customer]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM customer")
                return [Customer.from_row(row) for row in cur.fetchall()]

    def find_by_id(self, customer_id: int) -> Customer | None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM customer WHERE customer_id = :1", (customer_id,))
                row = cur.fetchone()
                return Customer.from_row(row) if row else None

    def update(self, customer: Customer):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE customer
                    SET first_name=:1, last_name=:2, date_of_birth=:3, phone_number=:4,
                        email=:5, street=:6, city=:7, state=:8, apartment_number=:9, zipcode=:10
                    WHERE customer_id=:11
                """, (customer.first_name, customer.last_name, customer.date_of_birth,
                      customer.phone_number, customer.email, customer.street,
                      customer.city, customer.state, customer.apartment_number,
                      customer.zipcode, customer.customer_id))
                conn.commit()

    def remove(self, customer_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM customer WHERE customer_id = :1", (customer_id,))
                conn.commit()

    def search(self, query: str) -> list[Customer]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                q = f"%{query.lower()}%"
                cur.execute("""
                    SELECT * FROM customer
                    WHERE LOWER(first_name) LIKE :q1
                       OR LOWER(last_name)  LIKE :q2
                       OR LOWER(email)      LIKE :q3
                """, {"q1": q, "q2": q, "q3": q})
                return [Customer.from_row(row) for row in cur.fetchall()]
