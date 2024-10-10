from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client.MilkTracking
milk_entries = db.milk_entries

# Function to get data for a specific month and year
def get_monthly_data(month, year):
    """Retrieve milk data for a specific month and year."""
    results = milk_entries.find({
        "month": month,
        "year": year
    })
    return list(results)

# Function to add a new milk entry
def add_milk_entry(date, quantity):
    """Add a new milk entry to the database."""
    entry = {
        "date": date.strftime("%Y-%m-%d"),
        "quantity": float(quantity),
        "cost": quantity * 60,  # 60 Rs per liter
        "month": date.strftime("%B"),
        "year": date.year
    }
    milk_entries.insert_one(entry)