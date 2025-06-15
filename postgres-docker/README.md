# PostgreSQL Docker Setup

This project provides a simple setup to run a PostgreSQL database using Docker Compose.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed

## Project Structure

```
postgres-docker
├── docker-compose.yml
└── README.md
```

## Getting Started

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd postgres-docker
   ```

2. **Build and run the containers**:
   ```bash
   docker-compose up -d
   ```

3. **Accessing the PostgreSQL database**:
   - The PostgreSQL database will be available on port `5444` of your host machine.
   - You can connect to the database using any PostgreSQL client with the following credentials:
     - **Username**: `searchuser`
     - **Password**: `searchpass`
     - **Database Name**: `searchdb`

4. **Stopping the containers**:
   ```bash
   docker-compose down
   ```

## Notes

- The database will be initialized with the specified environment variables.
- Make sure to check the `docker-compose.yml` file for any additional configurations or changes.