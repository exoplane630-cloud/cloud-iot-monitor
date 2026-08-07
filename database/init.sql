CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    timestamp TIMESTAMP NOT NULL
)