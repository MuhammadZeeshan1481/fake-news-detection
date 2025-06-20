CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text TEXT,
    prediction TEXT,
    confidence REAL,
    suspicious_words TEXT
);
