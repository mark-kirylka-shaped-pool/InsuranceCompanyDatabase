from db.schema.db_connection import get_connection


class HomeInsurance:
    def __init__(self, policy_id, end_date=None, house_price=None,
                 house_area=None, bedroom_number=None, bathroom_number=None,
                 street=None, city=None, state=None,
                 apartment_number=None, zip_code=None, house_id=None):

        self.house_id = house_id
        self.policy_id = policy_id
        self.end_date = end_date
        self.house_price = house_price
        self.house_area = house_area
        self.bedroom_number = bedroom_number
        self.bathroom_number = bathroom_number
        self.street = street
        self.city = city
        self.state = state
        self.apartment_number = apartment_number
        self.zip_code = zip_code

    @staticmethod
    def from_row(row):
        return HomeInsurance(
            house_id=row[0],
            policy_id=row[1],
            end_date=row[2],
            house_price=row[3],
            house_area=row[4],
            bedroom_number=row[5],
            bathroom_number=row[6],
            street=row[7],
            city=row[8],
            state=row[9],
            apartment_number=row[10],
            zip_code=row[11]
        )

    def __repr__(self):
        return f"HomeInsurance({self.house_id}: policy={self.policy_id}, {self.city})"


class HomeInsuranceDAO:

    def add(self, home: HomeInsurance):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO home_insurance
                    (policy_id, end_date, house_price, house_area,
                     bedroom_number, bathroom_number, street, city,
                     state, apartment_number, zip_code)
                    VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)
                """, (
                    home.policy_id,
                    home.end_date,
                    home.house_price,
                    home.house_area,
                    home.bedroom_number,
                    home.bathroom_number,
                    home.street,
                    home.city,
                    home.state,
                    home.apartment_number,
                    home.zip_code
                ))
                conn.commit()

    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM home_insurance")
                return [HomeInsurance.from_row(row) for row in cur.fetchall()]

    def find_by_id(self, house_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM home_insurance WHERE house_id = :1", (house_id,))
                row = cur.fetchone()
                return HomeInsurance.from_row(row) if row else None

    def get_by_policy(self, policy_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM home_insurance WHERE policy_id = :1", (policy_id,))
                return [HomeInsurance.from_row(row) for row in cur.fetchall()]

    def update(self, home: HomeInsurance):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE home_insurance
                    SET policy_id=:1,
                        end_date=:2,
                        house_price=:3,
                        house_area=:4,
                        bedroom_number=:5,
                        bathroom_number=:6,
                        street=:7,
                        city=:8,
                        state=:9,
                        apartment_number=:10,
                        zip_code=:11
                    WHERE house_id=:12
                """, (
                    home.policy_id,
                    home.end_date,
                    home.house_price,
                    home.house_area,
                    home.bedroom_number,
                    home.bathroom_number,
                    home.street,
                    home.city,
                    home.state,
                    home.apartment_number,
                    home.zip_code,
                    home.house_id
                ))
                conn.commit()

    def remove(self, house_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM home_insurance WHERE house_id = :1", (house_id,))
                conn.commit()