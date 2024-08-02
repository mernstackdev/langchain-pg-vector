# README.md

## Setup PostgreSQL with pgvector Extension

### Using Docker

1. **Pull the Docker Image:**

   ```bash
   docker pull ankane/pgvector
   ```

2. **Start the Container:**

   ```bash
   docker run --name pgvector-demo -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d ankane/pgvector
   ```

   This command runs a container using the `ankane/pgvector` image, sets the container name to `pgvector-demo`, assigns a password for the PostgreSQL instance, and maps port 5432 between the container and host.

3. **Verify the Container is Running:**

   ```bash
   docker ps
   ```

4. **Connect to the Database:**

   You can use a GUI tool such as pgAdmin or the command-line tool `psql` to inspect the database. When connecting, use `localhost` as the host and the password `mysecretpassword`.

5. **Create Database and Enable pgvector Extension:**

   ```sql
   CREATE DATABASE vector_db;
   \c vector_db
   CREATE EXTENSION pgvector;
   ```

## Running the FastAPI Application

1. **Create a Virtual Environment:**

   ```bash
   python -m virtualenv venv
   ```

2. **Activate the Virtual Environment:**

   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the Application:**

   ```bash
   python main.py
   ```

5. **Test the Application:**

   Open your browser and navigate to:

   ```url
   http://localhost:5000/docs
   ```

## Summary

This README guides you through setting up a PostgreSQL database with the `pgvector` extension using Docker. It also provides steps to set up and run a FastAPI application in a virtual environment.
