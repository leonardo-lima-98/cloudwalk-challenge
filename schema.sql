-- schema.sql

WITH per_minute AS (
  SELECT
    ts,
    SUM(CASE WHEN status='approved' THEN count ELSE 0 END) AS approved,
    SUM(CASE WHEN status='failed' THEN count ELSE 0 END) AS failed,
    SUM(CASE WHEN status='denied' THEN count ELSE 0 END) AS denied,
    SUM(CASE WHEN status='reversed' THEN count ELSE 0 END) AS reversed
  FROM transactions
  GROUP BY ts
),
with_rate AS (
  SELECT
    ts,
    approved,
    failed,
    denied,
    reversed,
    (failed * 1.0) / NULLIF(approved + failed + denied + reversed, 0) AS failure_rate
  FROM per_minute
)
SELECT * FROM with_rate ORDER BY ts;