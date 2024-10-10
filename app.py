import streamlit as st
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from auth import admin_protect
from whatsapp import send_whatsapp_message
import os
from dotenv import load_dotenv
from streamlit_date_picker import date_picker, PickerType  # Import PickerType
import streamlit_shadcn_ui as ui
from database import get_monthly_data, add_milk_entry

load_dotenv()

# MongoDB conncection
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)  # Update with MongoDB Atlas connection string when hosted
db = client['MilkTracking']
milk_entries_collection = db['milk_entries']

# Get the current month and year
current_month = datetime.now().strftime("%B")
current_year = datetime.now().year
month_names = [datetime(2000, i, 1).strftime("%B") for i in range(1, 13)]

# display the dashboard
def display_dashboard():
    st.title("Milk Tracking Dashboard")

    # Dropdown to select the month, with the current month as default
    month = st.selectbox("Select Month", options=month_names, index=month_names.index(current_month))

    # Query to get milk entries for the selected month
    entries = list(milk_entries_collection.find({"month": month, "year": current_year}))

    # Calculate total milk and cost
    total_milk = sum(entry['quantity'] for entry in entries)
    total_cost = total_milk * 60  # Assuming cost is 60 Rs per liter

    # Create columns for side-by-side cards
    col1, col2 = st.columns(2)  # Create two columns

    # create cards for total milk quantity and total cost
    with col1:
        ui.card(title="Total Milk Quantity", content=f"{total_milk} L", key="quantity_card").render()
    with col2:
        ui.card(title="Total Cost", content=f"₹{total_cost:.2f}", key="cost_card").render()

    # Display the milk entries in a table
    if entries:
        data = [{"Date": entry['date'], "Quantity": f"{entry['quantity']} L", "Cost": f"₹{entry['cost']}"} for entry in entries]
        invoice_df = pd.DataFrame(data)
        ui.table(data=invoice_df, maxHeight=300)
    else:
        st.write("No entries found for the selected month.")

# Display the admin panel
def display_admin_panel():
    st.title("Admin Panel")

    # Date picker and number input fields
    dt_str = date_picker(picker_type=PickerType.date, value=datetime.now(), key="date_picker")  # Use PickerType.date
    quantity = st.number_input("Quantity (L)", min_value=0.0, format="%.2f")  # Allow floating point input

    if st.button("Add Entry"):
        if dt_str is not None:  
            dt = datetime.strptime(dt_str, "%Y-%m-%d")  
            add_milk_entry(dt, quantity)

            # Send WhatsApp messages
            send_whatsapp_message(quantity, dt.strftime("%Y-%m-%d"))

            st.success(f"Added {quantity:.2f} L of milk for {dt.strftime('%Y-%m-%d')}. Messages sent!")
        else:
            st.error("Please select a date.")

# Main function to display the app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Admin Panel"])

    if page == "Dashboard":
        display_dashboard()
    elif page == "Admin Panel":
        admin_protect()
        display_admin_panel()

if __name__ == "__main__":
    main()