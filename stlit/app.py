import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Google Sheets authentication setup
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",  # Full access to Google Sheets
    "https://www.googleapis.com/auth/drive.file"    # File-specific access to Drive
]
SERVICE_ACCOUNT_FILE = "/Users/ashwinnishad/Downloads/UW/neuropy/neuropy-442419-fabb35ce8ed2.json"  # Replace with your JSON file path 

# Authenticate and connect to Google Sheets
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)

# Open your Google Sheet
SHEET_NAME = "https://docs.google.com/spreadsheets/d/1T0LHecKs28qilZZl5ddA5SIp361li7l8-02YCt5jW0U/edit#gid=0"  # Replace with your sheet name
sheet = client.open_by_key("1T0LHecKs28qilZZl5ddA5SIp361li7l8-02YCt5jW0U").sheet1  # Access the first worksheet

# Streamlit app UI
st.title("Mood Tracker")
st.write("Track your mood by entering your name, selecting how you feel, and submitting the data!")

# Predefined names for the dropdown
names = ["Ashwin", "Gwen", "Margaret", "Lily"]

# Input fields
name = st.selectbox("Select your name:", names, help="Choose your name from the list.")


mood = st.selectbox(
    "How are you emotionally today?",
    ["Happy", "Sad", "Angry", "Fear", "Surprise", "Calm", "Excited", "Relief", "Frustrated", "Anxious"],
    help="Select the mood that best describes how you're feeling."
)

note = st.text_area(
    "Write a self-reported mood assessment (optional):",
    placeholder="Describe how you're feeling or anything you'd like to share.",
    help="You can leave this blank if you don't want to add a note."
)

date = datetime.now().strftime("%Y-%m-%d")  # Auto-populated date

# Submit button logic
if st.button("Submit"):
    if name.strip():  # Ensure name is not empty or just whitespace
        try:
            # Append data to Google Sheet
            sheet.append_row([name.strip(), mood, note, date])
            st.success(f"Thanks, {name}! Your mood has been recorded as '{mood}' on {date}.")
        except Exception as e:
            st.error(f"An error occurred while submitting your data: {e}")
    else:
        st.error("Please enter a valid name before submitting.")

# # Display current data in the Google Sheet (optional)
# if st.checkbox("Show submitted data"):
#     try:
#         # Fetch all rows from the sheet and display them as a table
#         records = sheet.get_all_records()
#         if records:
#             st.write("Here is the data submitted so far:")
#             st.dataframe(records)
#         else:
#             st.info("No data has been submitted yet.")
#     except Exception as e:
#         st.error(f"An error occurred while fetching data: {e}")