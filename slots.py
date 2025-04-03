# from pymongo import MongoClient
# from datetime import datetime, timedelta
# import pytz

# # MongoDB connection
# client = MongoClient("mongodb+srv://bnbdevs:feLC7m4jiT9zrmHh@cluster0.fjnp4qu.mongodb.net/?retryWrites=true&w=majority")
# db = client["conf_bookings_db"]

# # Function to generate the date format in "dd-mm-yyyy"
# def get_next_dates(num_days=7):
#     today = datetime.now(pytz.timezone("UTC")).date()
#     dates = [(today + timedelta(days=i)).strftime("%d-%m-%Y") for i in range(num_days)]
#     return dates

# # Function to create time slots for a given date
# def create_slots_for_date(date_str):
#     # Start and end times in 24-hour format
#     start_hour = 11  # 11:00 AM
#     end_hour = 16    # 4:00 PM
#     slot_duration = 30  # in minutes
    
#     slots = []
#     # Generate time slots for 11:00 AM to 4:00 PM with 30-minute intervals
#     for hour in range(start_hour, end_hour):
#         for minute in [0, 30]:
#             start_time = f"{hour:02d}{minute:02d}"
#             end_time = f"{hour:02d}{(minute + 30) % 60:02d}" if minute == 0 else f"{(hour + 1) % 24:02d}00"
            
#             # Format the slot
#             slot = {
#                 "start_time": start_time,
#                 "end_time": end_time,
#                 "status": "open"
#             }
#             slots.append(slot)
    
#     # Insert into the collection for the given date
#     collection = db[date_str]
#     collection.insert_many(slots)

# # Function to check and create collections and slots
# def check_and_create_slots():
#     # Get the next 7 days' dates
#     dates = get_next_dates(7)
    
#     for date_str in dates:
#         # Check if collection exists
#         if date_str not in db.list_collection_names():
#             # Create collection and insert slots
#             print(f"Collection for {date_str} not found. Creating new collection and inserting slots.")
#             create_slots_for_date(date_str)
#         else:
#             print(f"Collection for {date_str} already exists. No need to create.")

# # Run the function to check and create slots
# check_and_create_slots()


from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["hall_booking"]
collection = db["bookings"]

# Define hall timings
HALL_OPEN = 11  # 11:00 AM
HALL_CLOSE = 16  # 4:00 PM
TIME_INTERVAL = 30  # Minimum slot size in minutes

def get_booked_slots(date):
    """Fetch booked slots for a specific date."""
    bookings = collection.find({"date": date}, {"_id": 0, "start_time": 1, "end_time": 1})
    return [(entry["start_time"], entry["end_time"]) for entry in bookings]

def generate_available_slots(date, duration):
    """Generate available slots based on date and duration."""
    booked_slots = get_booked_slots(date)
    available_slots = []

    start_time = datetime.strptime(f"{HALL_OPEN}:00", "%H:%M")
    end_time = datetime.strptime(f"{HALL_CLOSE}:00", "%H:%M")

    while start_time + timedelta(minutes=duration) <= end_time:
        slot_start = start_time.strftime("%H:%M")
        slot_end = (start_time + timedelta(minutes=duration)).strftime("%H:%M")

        # Check if slot overlaps with booked slots
        if not any(
            (slot_start < end and slot_end > start) for start, end in booked_slots
        ):
            available_slots.append({"start": slot_start, "end": slot_end})

        start_time += timedelta(minutes=TIME_INTERVAL)  # Move by 30 mins

    return available_slots

@app.route("/available_slots", methods=["GET"])
def available_slots():
    """API to get available slots for a given date and duration."""
    try:
        date = request.args.get("date")  # Expected format: YYYY-MM-DD
        duration = int(request.args.get("duration"))  # Duration in minutes

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

        if duration < 30 or duration > 300:
            return jsonify({"error": "Duration must be between 30 and 300 minutes"}), 400

        slots = generate_available_slots(date, duration)
        return jsonify({"available_slots": slots})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/book_slot", methods=["POST"])
def book_slot():
    """API to book a slot for a specific date."""
    try:
        data = request.json
        date = data.get("date")  # YYYY-MM-DD
        start_time = data.get("start_time")  # e.g., "11:00"
        end_time = data.get("end_time")  # e.g., "12:00"

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

        # Validate time format
        try:
            start_time_obj = datetime.strptime(start_time, "%H:%M")
            end_time_obj = datetime.strptime(end_time, "%H:%M")
        except ValueError:
            return jsonify({"error": "Invalid time format, use HH:MM"}), 400

        if start_time_obj < datetime.strptime(f"{HALL_OPEN}:00", "%H:%M") or end_time_obj > datetime.strptime(f"{HALL_CLOSE}:00", "%H:%M"):
            return jsonify({"error": "Time slot out of allowed range"}), 400

        if (end_time_obj - start_time_obj).total_seconds() / 60 < 30:
            return jsonify({"error": "Minimum booking duration is 30 minutes"}), 400

        # Check if slot is available
        booked_slots = get_booked_slots(date)
        for booked_start, booked_end in booked_slots:
            if not (end_time <= booked_start or start_time >= booked_end):
                return jsonify({"error": "Slot already booked"}), 400

        # Book the slot
        collection.insert_one({"date": date, "start_time": start_time, "end_time": end_time, "status": "booked"})
        return jsonify({"message": "Slot booked successfully", "date": date, "start_time": start_time, "end_time": end_time})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
