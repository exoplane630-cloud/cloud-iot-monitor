# Cloud IoT Environmental Monitoring System

A small cloud and networking project that simulates an IoT environmental monitoring pipeline using Python, MQTT, Docker, PostgreSQL, and AWS EC2.

The project was built to explore how sensor data can be transmitted, stored, recovered after network interruptions, and tested across both local and cloud environments.

## Architecture

```text
Sensor Simulator (Python)
        |
        | MQTT
        v
Mosquitto MQTT Broker
        |
        v
Python Subscriber
        |
        v
PostgreSQL Database
```

During MQTT connectivity failures:

```text
Sensor
  |
  X  MQTT unavailable
  |
  v
Local SQLite Cache
  |
  | connection restored
  v
MQTT Broker
```

## Features

- Simulates environmental sensor readings including temperature and humidity
- Publishes sensor data using the MQTT protocol
- Uses Mosquitto as the MQTT broker
- Subscribes to sensor messages with a Python MQTT client
- Stores received readings in PostgreSQL
- Uses SQLite as a local cache when MQTT is unavailable
- Automatically resends cached readings after connectivity is restored
- Runs infrastructure locally using Docker Compose
- Supports MQTT username/password authentication
- Loads credentials from environment variables
- Excludes secrets and local runtime data from version control

## Technologies

- Python
- MQTT
- Eclipse Mosquitto
- PostgreSQL
- SQLite
- Docker
- Docker Compose
- AWS EC2
- Git / GitHub

## Reliability Experiment

The sensor simulator was tested under temporary MQTT broker failure.

When the broker was unavailable, sensor readings were stored in a local SQLite cache instead of being lost.

After the broker became available again, the simulator reconnected and resent the cached readings through MQTT.

This experiment demonstrates a simple store-and-forward approach for handling intermittent network connectivity in IoT systems.

## Security

Basic security practices were added to the project:

- MQTT username/password authentication
- Credentials loaded through environment variables
- `.env` excluded from version control
- MQTT password files excluded from version control
- AWS access performed using SSH key authentication

The project intentionally keeps the security implementation small and focuses on demonstrating the underlying concepts.

## AWS EC2 Experiment

After validating the system locally, a small cloud networking experiment was performed using AWS EC2.

An Amazon Linux EC2 instance was created and Docker was installed on the instance. A Mosquitto MQTT broker was then run inside a Docker container.

The local computer successfully established a TCP connection to the EC2-hosted MQTT broker and published an MQTT message from a local Python client to the remote broker.

```text
Local Laptop
     |
     | Internet / MQTT
     | TCP 1883
     v
AWS EC2
     |
     v
Docker Container
     |
     v
Mosquitto MQTT Broker
```

This was a limited cloud experiment rather than a permanent production deployment.

## What I Learned

This project helped me understand the relationship between several technologies that are often discussed separately:

- how MQTT publishers, brokers, and subscribers communicate
- how containers can provide reproducible infrastructure
- how application data can be persisted in PostgreSQL
- how local caching can improve resilience during network failures
- how authentication and environment variables can improve basic security
- how a locally developed service can communicate with infrastructure running on a cloud VM
- how AWS security groups affect inbound network connectivity

## Future Improvements

Possible future improvements include:

- TLS encryption for MQTT
- restricting MQTT network access further
- SSH tunnelling for private database access
- automated testing
- monitoring and logging
- deploying the complete application stack to cloud infrastructure

## Project Status

Educational / experimental project.

The main system runs locally using Docker-based infrastructure, with an additional AWS EC2 experiment used to test remote MQTT communication.