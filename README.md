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
    ```
    pipenv install
    pipenv shell
    ```