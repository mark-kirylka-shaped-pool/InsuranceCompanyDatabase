from db.schema.db_connection import get_connection


class CarInsurance:
    def __init__(self, policy_id, end_date=None, make=None, model=None,
                 vin=None, yearly_mileage=None, car_id=None):
        self.car_id = car_id
        self.policy_id = policy_id
        self.end_date = end_date
        self.make = make
        self.model = model
        self.vin = vin
        self.yearly_mileage = yearly_mileage

    @staticmethod
    def from_row(row):
        return CarInsurance(
            car_id=row[0],
            policy_id=row[1],
            end_date=row[2],
            make=row[3],
            model=row[4],
            vin=row[5],
            yearly_mileage=row[6]
        )

    def __repr__(self):
        return f"CarInsurance({self.car_id}: policy={self.policy_id}, {self.make} {self.model})"


class CarInsuranceDAO:

    def add(self, car: CarInsurance):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO car_insurance
                    (policy_id, end_date, make, model, vin, yearly_mileage)
                    VALUES (:1, :2, :3, :4, :5, :6)
                """, (
                    car.policy_id,
                    car.end_date,
                    car.make,
                    car.model,
                    car.vin,
                    car.yearly_mileage
                ))
                conn.commit()

    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM car_insurance")
                return [CarInsurance.from_row(row) for row in cur.fetchall()]

    def find_by_id(self, car_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM car_insurance WHERE car_id = :1", (car_id,))
                row = cur.fetchone()
                return CarInsurance.from_row(row) if row else None

    def get_by_policy(self, policy_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM car_insurance WHERE policy_id = :1", (policy_id,))
                return [CarInsurance.from_row(row) for row in cur.fetchall()]

    def update(self, car: CarInsurance):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE car_insurance
                    SET policy_id=:1,
                        end_date=:2,
                        make=:3,
                        model=:4,
                        vin=:5,
                        yearly_mileage=:6
                    WHERE car_id=:7
                """, (
                    car.policy_id,
                    car.end_date,
                    car.make,
                    car.model,
                    car.vin,
                    car.yearly_mileage,
                    car.car_id
                ))
                conn.commit()

    def remove(self, car_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM car_insurance WHERE car_id = :1", (car_id,))
                conn.commit()