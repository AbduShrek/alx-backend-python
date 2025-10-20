#!/usr/bin/env python3
"""
Memory-efficient average age using generators.

- stream_user_ages(): yields ages one by one from user_data.
- When run as a script, computes and prints:
  "Average age of users: <value>"

Constraints:
- No SQL AVG() usage.
- At most two loops total in this script:
  1) The generator's single loop over the cursor,
  2) The aggregation loop consuming the generator.
"""

from typing import Generator
import seed


def stream_user_ages() -> Generator[int, None, None]:
    """Yield user ages one by one from the database (single loop)."""
    conn = seed.connect_to_prodev()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT CAST(age AS UNSIGNED) AS age FROM user_data ORDER BY user_id"
        )
        for (age,) in cursor:  # loop #1
            yield int(age)
    finally:
        cursor.close()
        conn.close()


def _compute_average() -> float:
    """Consume the generator to compute the average age without loading all rows."""
    total = 0
    count = 0
    for age in stream_user_ages():  # loop #2
        total += age
        count += 1
    return (total / count) if count else 0.0


if __name__ == "__main__":
    avg = _compute_average()
    print(f"Average age of users: {avg}")
