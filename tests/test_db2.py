import pytest
import sqlglot


def _transpile(sql: str, read: str | None = None, write: str | None = None) -> str:
    kwargs = {}
    if read:
        kwargs["read"] = read
    if write:
        kwargs["write"] = write
    return sqlglot.transpile(sql, **kwargs)[0]


@pytest.mark.parametrize("dialect", ["ibmdb2", "db2"])
def test_plugin_dialect_is_registered(dialect: str):
    assert _transpile("SELECT TRUE", write=dialect) == "SELECT 1"


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT FROM table1",
        "SELECT a, b, c FROM table1",
        "CREATE TABLE t (a SMALLINT, b INT, c BIGINT)",
        "CREATE TABLE t (a CHAR(10), b VARCHAR(100))",
        "CREATE TABLE t (a DECIMAL(10, 2))",
        "CREATE TABLE t (a TIMESTAMP)",
        "SELECT * FROM t FETCH FIRST 10 ROWS ONLY",
        "SELECT * FROM t FETCH FIRST ROW ONLY",
        "SELECT * FROM t OFFSET 5 ROWS",
        "SELECT * FROM t OFFSET 5 ROWS FETCH FIRST 10 ROWS ONLY",
        "SELECT a || b FROM t",
        "SELECT a || b || c FROM t",
        "SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.id",
        "SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.id",
        "SELECT * FROM t1 RIGHT JOIN t2 ON t1.id = t2.id",
        "SELECT * FROM (SELECT a, b FROM t1) AS subq",
        "SELECT COUNT(*) FROM t",
        "SELECT SUM(amount) FROM t",
        "SELECT AVG(amount) FROM t",
        "SELECT MIN(amount), MAX(amount) FROM t",
        "SELECT category, COUNT(*) FROM t GROUP BY category",
        "SELECT category, COUNT(*) FROM t GROUP BY category HAVING COUNT(*) > 5",
        "SELECT * FROM t ORDER BY a",
        "SELECT * FROM t ORDER BY a DESC",
        "SELECT * FROM t ORDER BY a, b DESC",
        "SELECT CASE WHEN a > 0 THEN 'positive' ELSE 'negative' END FROM t",
        "SELECT CASE a WHEN 1 THEN 'one' WHEN 2 THEN 'two' ELSE 'other' END FROM t",
        "SELECT * FROM t WHERE a IN (1, 2, 3)",
        "SELECT * FROM t WHERE a BETWEEN 1 AND 10",
        "SELECT * FROM t WHERE name LIKE 'John%'",
        "SELECT * FROM t WHERE a IS NULL",
        "SELECT COALESCE(a, b, c) FROM t",
        "SELECT a FROM t1 UNION SELECT a FROM t2",
        "SELECT a FROM t1 UNION ALL SELECT a FROM t2",
        "WITH cte AS (SELECT * FROM t1) SELECT * FROM cte",
        "INSERT INTO t (a, b) VALUES (1, 2)",
        "UPDATE t SET a = 1 WHERE b = 2",
        "DELETE FROM t WHERE a = 1",
        "CREATE TABLE t (id INT, name VARCHAR(100))",
        "DROP TABLE t",
    ],
)
def test_identity_cases(sql: str):
    assert _transpile(sql, read="ibmdb2", write="ibmdb2") == sql


@pytest.mark.parametrize(
    ("sql", "expected"),
    [
        ("SELECT CURRENT_DATE", "SELECT CURRENT DATE"),
        ("SELECT CURRENT_TIMESTAMP", "SELECT CURRENT TIMESTAMP"),
        ("SELECT STRPOS(haystack, needle)", "SELECT POSSTR(haystack, needle)"),
        ("SELECT TRUE, FALSE", "SELECT 1, 0"),
        ("CAST(value AS CHAR)", "CHAR(value)"),
        ("SELECT EXTRACT(DAYOFWEEK FROM date_col)", "SELECT DAYOFWEEK(date_col)"),
        ("SELECT EXTRACT(DAYOFYEAR FROM date_col)", "SELECT DAYOFYEAR(date_col)"),
        ("SELECT TIME_TO_STR(timestamp_col, 'YYYY-MM-DD')", "SELECT VARCHAR_FORMAT(timestamp_col, 'YYYY-MM-DD')"),
        ("SELECT DATEDIFF(date1, date2)", "SELECT DAYS(date1) - DAYS(date2)"),
        ("SELECT * FROM t WHERE a NOT IN (1, 2, 3)", "SELECT * FROM t WHERE NOT a IN (1, 2, 3)"),
        ("SELECT * FROM t WHERE a IS NOT NULL", "SELECT * FROM t WHERE NOT a IS NULL"),
        ("SELECT MAX(a, b, c)", "SELECT GREATEST(a, b, c)"),
        ("SELECT MIN(a, b, c)", "SELECT LEAST(a, b, c)"),
        ("SELECT * FROM t OFFSET 5", "SELECT * FROM t OFFSET 5 ROWS"),
        ("SELECT * FROM t LIMIT 10", "SELECT * FROM t FETCH FIRST 10 ROWS ONLY"),
    ],
)
def test_generation_cases(sql: str, expected: str):
    assert _transpile(sql, write="ibmdb2") == expected
