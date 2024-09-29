# Bus Ticket Reservation System

## Overview

The **Bus Ticket Reservation System** is a web-based application built using Django and Django REST framework. It allows users to search for buses based on source, destination, and travel date, and reserve seats on the available buses. The application comes with pre-loaded bus data and a simple API-based interface for interacting with the system.

## Setup and Run

### Setup Instructions:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/aniket-24/bus-ticket-reservation-system.git
   cd bus-ticket-reservation-system
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Load bus data from fixture**:

   ```bash
   python manage.py loaddata initial_buses.json
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## How It Works

- Users can search for buses based on **source**, **destination**, and **date**.
- The system checks the bus frequency (i.e., days when the bus is active) and returns available buses.
- Users can then **reserve seats** on a particular bus, and the system ensures that the required number of seats is available before confirming the reservation.
- The application keeps track of all reservations, which users can view later based on their **user ID**.

### Core Features:

- **Search Buses**: Search buses based on source, destination, and date.
- **Reserve Seats**: Reserve a certain number of seats on a selected bus, ensuring that seat availability is taken into account.
- **View Reservations**: List all past and upcoming reservations for a user.

## Model Schema

### Bus

- **company_name**: The name of the bus company.
- **bus_number**: Unique identifier for each bus.
- **source**: The starting location of the bus.
- **destination**: The ending location of the bus.
- **start_time**: The time at which the bus departs.
- **end_time**: The time at which the bus arrives at the destination.
- **frequency**: The days on which the bus operates (e.g., "Monday, Wednesday, Friday").
- **total_seats**: The total number of seats available on the bus.

### Reservation

- **user_id**: Simple identification for the user (without authentication).
- **bus**: The bus on which seats are reserved (foreign key to Bus model).
- **reserved_seats**: The number of seats reserved by the user.
- **reservation_date**: The date on which the reservation is made.

## API Endpoints

### 1. Search for Buses

- **Endpoint**: `/buses/search/`
- **Method**: `GET`
- **Request**:
  ```http
  GET /buses/search/?source=<source_city>&destination=<destination_city>&date=<YYYY-MM-DD>
  ```
- **Response**:
  ```json
  [
    {
      "id": 1,
      "company_name": "ABC Travels",
      "bus_number": "DL1234",
      "source": "Delhi",
      "destination": "Mumbai",
      "start_time": "09:00:00",
      "end_time": "22:00:00",
      "frequency": "Monday,Wednesday,Friday",
      "total_seats": 40
    },
    ...
  ]
  ```

### 2. Reserve Seats

- **Endpoint**: `/reservations/reserve/`
- **Method**: `POST`
- **Request**:
  ```json
  {
    "user_id": 1,
    "bus": 1,
    "reserved_seats": 3,
    "reservation_date": "2024-09-30"
  }
  ```
- **Response (Success)**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "bus": 1,
    "reserved_seats": 3,
    "reservation_date": "2024-09-30"
  }
  ```
- **Response (Failure)**:
  ```json
  {
    "error": "Not enough seats available"
  }
  ```

### 3. View Reservations for a User

- **Endpoint**: `/reservations/user/<user_id>/`
- **Method**: `GET`
- **Request**:
  ```http
  GET /reservations/user/1/
  ```
- **Response**:
  ```json
  [
    {
      "id": 1,
      "user_id": 1,
      "bus": {
        "id": 1,
        "company_name": "ABC Travels",
        "bus_number": "DL1234",
        "source": "Delhi",
        "destination": "Mumbai",
        "start_time": "09:00:00",
        "end_time": "22:00:00"
      },
      "reserved_seats": 3,
      "reservation_date": "2024-09-30"
    },
    ...
  ]
  ```
