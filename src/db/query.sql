-- query.sql

WITH per_minute AS (
  SELECT
    timestamp,
    SUM(CASE WHEN status='approved' THEN count ELSE 0 END) AS approved,
    SUM(CASE WHEN status='denied' THEN count ELSE 0 END) AS denied,
    SUM(CASE WHEN status='reversed' THEN count ELSE 0 END) AS reversed,
    SUM(CASE WHEN status='backend_reversed' THEN count ELSE 0 END) AS backend_reversed,
    SUM(CASE WHEN status='failed' THEN count ELSE 0 END) AS failed,
    SUM(CASE WHEN status='refunded' THEN count ELSE 0 END) AS refunded
  FROM transactions
  GROUP BY timestamp
),
with_rate AS (
  SELECT
    timestamp,
    approved,
    denied,
    reversed,
    backend_reversed,
    failed,
    refunded,
    (failed * 1.0) / NULLIF(approved + denied + reversed + backend_reversed + failed + refunded, 0) AS failure_rate
  FROM per_minute
)
SELECT * FROM with_rate ORDER BY timestamp;