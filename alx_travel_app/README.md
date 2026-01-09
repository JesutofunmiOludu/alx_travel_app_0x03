 ALX Travel App 0x00 — Database Models, Serializers & Seeder

This project is a duplicated version of the original **alx_travel_app**, extended with database models, API serializers, and a custom management command for seeding sample data into the database.  
It is part of the ALX Backend specialization tasks.

---

## 📌 Objective

- Define database models for **Listing**, **Booking**, and **Review**.
- Create serializers for converting model instances into API-friendly JSON.
- Implement a Django management command to seed the database with sample listings.
- Confirm that the seeder populates the database correctly.

---

## 📁 Project Structure

alx_travel_app_0x00/
│
├── alx_travel_app/
│ ├── listings/
│ │ ├── models.py
│ │ ├── serializers.py
│ │ ├── management/
│ │ │ └── commands/
│ │ │ └── seed.py
│ │ └── ...
│ └── ...
└── README.md

yaml
Copy code

---

## 🧩 Tasks Completed

### 1. Project Duplication

The original project was duplicated into:

alx_travel_app_0x00

yaml
Copy code

This serves as the working directory for this task.

---

## 2. Database Models Setup

All models were defined in:

listings/models.py

markdown
Copy code

### ### 📍 Models Included

### 🔹 **Listing**
Represents a travel property or location.

Fields include:
- `title`
- `description`
- `location`
- `price`
- `created_at`
- `updated_at`

---

### 🔹 **Booking**
Represents a reservation made by a user.

Relationships:
- `listing` → ForeignKey to Listing  
- `user` → ForeignKey (if user model is available)

Key fields:
- `check_in_date`
- `check_out_date`
- `guest_count`
- `created_at`

---

### 🔹 **Review**
Represents user feedback on a listing.

Relationships:
- `listing` → ForeignKey  
- `user` → ForeignKey  

Fields:
- `rating`
- `comment`
- `created_at`

---

## 3. API Serializers

Serializers were added to:

listings/serializers.py

yaml
Copy code

### 🔹 **ListingSerializer**
Handles converting Listing model instances into JSON format.

### 🔹 **BookingSerializer**
Handles Booking model data for API input/output.

---

## 4. Seeder Management Command

A custom Django management command was created here:

listings/management/commands/seed.py

markdown
Copy code

### 🌱 Purpose of Seeder

- Populate the database with sample Listing data.
- Useful for testing and development.

### 📌 Run Seeder

```bash
python manage.py seed
This will insert predefined listings and print a success message.

5. Testing the Seeder
After running migrations, seed the database:

bash
Copy code
python manage.py migrate
python manage.py seed
Verify:

bash
Copy code
python manage.py shell

>>> from listings.models import Listing
>>> Listing.objects.all()
🔗 Repository Details
GitHub Repository: alx_travel_app_0x00

Main Directory: alx_travel_app

Key Files:

listings/models.py

listings/serializers.py

listings/management/commands/seed.py

README.md