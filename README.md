# E-commerce OLTP Data Generator

A high-performance, modular synthetic data generation pipeline designed for E-commerce OLTP systems. This tool generates realistic, relationally consistent data using Python and loads it into PostgreSQL.

---
## Overview
Generate synthetic data for an e-commerce transactional database with:
* **Modular Structure**:
   * **Generators**: Pure data generation logic (Faker)
   * **Tasks**: Execution units
   * **Stages**: Logical grouping (Master, Reference, Transaction)
   * **Pipelines**: Overall flow
* **Realistic Data**: Implements some simple weighted sampling and business constraints.
* **High Performance**: Optimized for write throughput using `psycopg2.extras.execute_values`.
* **Idempotency**: Supports database cleanup and regeneration.

### Tech Stack
* **Language**: Python 3.12+
* **Database**: PostgreSQL
* **Core Libs**: `Faker`, `psycopg2-binary`, `python-dotenv`
* **Package Manager**: Poetry

### ER Diagram
![](docs/images/erd.png)

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/plat102/py-ecommerce-synth-oltp
cd py-ecommerce-synth-oltp
```

### 2. Install dependencies
```bash
poetry install
```

### 3. Configure environment

Create a `.env` file from the example:
```bash
cp .env.example .env
```

Update your PostgreSQL credentials in `.env`.

### 4. Initialize database

Create the target database (if not exists):
```bash
python src/scripts/init_db.py
```

## Usage

Run the pipeline using the CLI entry point.

### 1. Full run

Cleans the database (`TRUNCATE CASCADE`) and regenerates all data from scratch.
```bash
python src/main.py --clean
```

### 2. Append

Generates and adds more data without deleting existing records.
```bash
python src/main.py
```

### 3. Run Specific Stage
Run specific parts of the pipeline independently.

* **Options**: `setup`, `master`, `catalog`, `transaction`
```bash
# Example: Only generate new orders
python src/main.py --stage transaction
```

### Data Volume Configuration

Data volumes are managed in `src/mock_ecommerce/config.py`.

* **DEV Profile**: Hardcoded volumes (20 Brands, 2000 Products, 50 Orders)

Change the environment by setting `APP_ENV=PROD` in `.env`.

