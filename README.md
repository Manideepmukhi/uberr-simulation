# 🚗 Uberr - Ride-Hailing Backend Simulation

This is a backend simulation of a ride-hailing platform (like Uber/Ola), built using **Django** with a clean and modular architecture.

It models the **full ride lifecycle**, **driver allocation**, and **fare computation** using background scripts and Django's ORM.

---

## 🧱 Tech Stack

| Component        | Tech            |
|------------------|-----------------|
| Backend Framework | Django (Python) |
| Database         | SQLite (Dev) / PostgreSQL (Prod ready) |
| ORM              | Django ORM |
| Background Tasks | Django `management commands` |
| Admin Interface  | Django Admin Panel |

---

## 🧪 Features Implemented

### ✅ Ride Lifecycle

Each ride follows the full journey:

1. `create_ride` – Rider requests a ride  
2. `driver_assigned` – System assigns an available nearby driver  
3. `driver_at_location` – Driver reaches pickup point  
4. `start_ride` – Ride starts  
5. `end_ride` – Ride ends, fare is computed  

Timestamps are tracked for all key transitions.

---

### ✅ Driver Matching Rules

- Searches for nearby drivers within expanding radius (2km every 10s)
- Driver must be available
- Cannot be assigned to multiple rides at once
- Excludes:
  - Drivers who completed a ride with the same rider in last 30 minutes
  - Drivers who cancelled their last 2 rides

---

### ✅ Fare Computation Formula

Fare = Base Fare + (Distance × Rate per KM) + (Duration × Rate per Minute) + Waiting Charges

yaml
Copy
Edit

Rates are configurable via key-value pairs (`FareConfig` model):

| Config Key              | Example Value |
|-------------------------|---------------|
| `base_fare`             | ₹50.0         |
| `per_km`                | ₹10.0         |
| `per_minute`           | ₹2.0          |
| `waiting_charge_per_min` | ₹1.0        |

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/<your-username>/uberr-simulation.git
cd uberr-simulation

2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Migrate DB
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
4. Create Superuser
bash
Copy
Edit
python manage.py createsuperuser
5. Set Up Fare Config
bash
Copy
Edit
python manage.py setup_fare_config
6. Simulate Data (drivers, riders, rides)
bash
Copy
Edit
python manage.py simulate_data
7. Run Ride Lifecycle Simulation
bash
Copy
Edit
python manage.py simulate_ride_flow
