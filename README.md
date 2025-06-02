# 🌍 Travel Itinerary Planner CLI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![SQLAlchemy ORM](https://img.shields.io/badge/SQLAlchemy-ORM-green.svg)](https://www.sqlalchemy.org/)
[![Alembic Migrations](https://img.shields.io/badge/Alembic-Migrations-lightgrey.svg)](https://alembic.sqlalchemy.org/)
[![Click CLI](https://img.shields.io/badge/CLI-Click-yellow.svg)](https://click.palletsprojects.com/)
[![SQLite Database](https://img.shields.io/badge/Database-SQLite-brightgreen.svg)](https://sqlite.org/)

A feature-rich command-line application for managing complete travel itineraries with flights, accommodations, and activities.

## Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Database Schema](#-database-schema)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## ✨ Features

### Trip Management
- Create and organize travel itineraries
- Set destinations and travel dates
- View all trips at a glance

### Booking Tracking
- Store flight details (airline, flight number)
- Save hotel/reservation information
- Manage multiple bookings per trip

### Activity Planning
- Schedule activities with specific times
- View daily agendas chronologically
- Flexible activity management

### Data Management
- SQLite database persistence
- Alembic schema migrations
- Sample data seeding

## 🛠 Installation

### Prerequisites
- Python 3.8 or later
- pipenv (recommended)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BrianSila/Travel-Itinerary-planner
   cd Travel-Itinerary-planner
   ```

2. **Setup the environment**
    ```bash
    pipenv install
    pipenv shell
    ```

3. **Install additional requirements**
   ```bash
   pip installfaker
   pip install click
   ```

4. **Initialize the database**
   ```bash
   alembic upgrade head
   ```

## 🚀 Usage

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list-trips` | Show all trips | `python -m lib.cli list-trips` |
| `add-trip` | Create new trip | `python -m lib.cli add-trip` |
| `trip-details` | View trip details | `python -m lib.cli trip-details 1` |
| `add-activity` | Schedule activity | `python -m lib.cli add-activity 1` |
| `add-booking` | Add booking info | `python -m lib.cli add-booking 1` |


### 🗄 Database Schema (Verified Working)

### Entity Relationship Diagram
```mermaid
erDiagram
    TRIP ||--o{ BOOKING : "has"
    TRIP ||--o{ ACTIVITY : "has"
    TRIP {
        integer id PK
        string destination
        date start_date
        date end_date
    }
    BOOKING {
        integer id PK
        string flight
        string hotel
        integer trip_id FK
    }
    ACTIVITY {
        integer id PK
        string name
        time time
        date date
        integer trip_id FK
    }

### Example workflow

1. **Create a new trip:**
   ```bash
   python -m lib.cli add-trip
   ```
Follow prompts to enter destination and dates

2. **Add bookings:**
   ```bash
   python -m lib.cli add-booking 1
   ```
Enter flight and hotel details

3. **Plan activities:**
   ```bash
   python -m lib.cli add-activity 1
   ```
Specify activity name, date, and time

4. **View your itinerary:**
   ```bash
   python -m lib.cli trip-details 1
   ```

## 📂 Project Structure

travel-planner-cli/
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── alembic.ini
├── README.md
└── lib/
    ├── cli.py                # CLI command definitions
    ├── db/
    │   ├── __init__.py
    │   ├── config.py         # Database configuration
    │   ├── models.py         # SQLAlchemy ORM models
    │   ├── seed.py           # Database seeding
    │   └── migrations/       # Alembic migration scripts
    ├── helpers.py            # Utility functions
    └── debug.py              # Debugging utilities

## 🔧 Development

### Creating Migrations

1. **After modifying models:**
   ```bash
   alembic revision --autogenerate -m "description of changes"
   ```