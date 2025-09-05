-- schema.sql

CREATE TABLE IF NOT EXISTS transactions (
    timestamp TEXT NOT NULL,
    status TEXT NOT NULL,
    count INTEGER NOT NULL
)
