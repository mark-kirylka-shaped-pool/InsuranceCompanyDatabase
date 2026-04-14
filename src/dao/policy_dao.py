from db.schema.db_connection import get_connection


class Policy:
    def __init__(self, customer_id, monthly_payment, start_date, coverage, policy_id=None):
        self.policy_id = policy_id
        self.customer_id = customer_id
        self.monthly_payment = monthly_payment
        self.start_date = start_date
        self.coverage = coverage

    @staticmethod
    def from_row(row):
        """Build a Policy from a DB row tuple."""
        return Policy(
            policy_id=row[0],
            customer_id=row[1],
            monthly_payment=row[2],
            start_date=row[3],
            coverage=row[4]
        )

    def __repr__(self):
        return f"Policy({self.policy_id}: customer={self.customer_id}, coverage={self.coverage})"


class PolicyDAO:
    def add(self, policy: Policy):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO policy (customer_id, monthly_payment, start_date, coverage)
                    VALUES (:1, :2, :3, :4)
                """, (policy.customer_id, policy.monthly_payment, policy.start_date, policy.coverage))
                conn.commit()

    def get_all(self) -> list[Policy]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM policy")
                return [Policy.from_row(row) for row in cur.fetchall()]

    def find_by_id(self, policy_id: int) -> Policy | None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM policy WHERE policy_id = :1", (policy_id,))
                row = cur.fetchone()
                return Policy.from_row(row) if row else None

    def get_by_customer(self, customer_id: int) -> list[Policy]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM policy WHERE customer_id = :1", (customer_id,))
                return [Policy.from_row(row) for row in cur.fetchall()]

    def update(self, policy: Policy):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE policy
                    SET customer_id=:1, monthly_payment=:2, start_date=:3, coverage=:4
                    WHERE policy_id=:5
                """, (policy.customer_id, policy.monthly_payment,
                      policy.start_date, policy.coverage, policy.policy_id))
                conn.commit()

    def remove(self, policy_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM policy WHERE policy_id = :1", (policy_id,))
                conn.commit()
