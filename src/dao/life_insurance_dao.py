from db.schema.db_connection import get_connection


class LifeInsurance:
    def __init__(self, policy_id, existing_conditions=None,
                 beneficiary=None, life_id=None):
        self.life_id = life_id
        self.policy_id = policy_id
        self.existing_conditions = existing_conditions
        self.beneficiary = beneficiary

    @staticmethod
    def from_row(row):
        return LifeInsurance(
            life_id=row[0],
            policy_id=row[1],
            existing_conditions=row[2].read() if row[2] else None,
            beneficiary=row[3]
        )

    def __repr__(self):
        return f"LifeInsurance({self.life_id}: policy={self.policy_id}, {self.beneficiary})"


class LifeInsuranceDAO:

    def add(self, life: LifeInsurance):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO life_insurance
                    (policy_id, existing_conditions, beneficiary)
                    VALUES (:1, :2, :3)
                """, (
                    life.policy_id,
                    life.existing_conditions,
                    life.beneficiary
                ))
                conn.commit()

    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM life_insurance")
                return [LifeInsurance.from_row(row) for row in cur.fetchall()]

    def find_by_id(self, life_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM life_insurance WHERE life_id = :1", (life_id,))
                row = cur.fetchone()
                return LifeInsurance.from_row(row) if row else None

    def get_by_policy(self, policy_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM life_insurance WHERE policy_id = :1", (policy_id,))
                return [LifeInsurance.from_row(row) for row in cur.fetchall()]

    def update(self, life: LifeInsurance):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE life_insurance
                    SET policy_id=:1,
                        existing_conditions=:2,
                        beneficiary=:3
                    WHERE life_id=:4
                """, (
                    life.policy_id,
                    life.existing_conditions,
                    life.beneficiary,
                    life.life_id
                ))
                conn.commit()

    def remove(self, life_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM life_insurance WHERE life_id = :1", (life_id,))
                conn.commit()