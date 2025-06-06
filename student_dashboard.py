import streamlit as st
import gspread
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# ------------------ GOOGLE SHEETS SETUP ------------------
SHEET_ID = "139CNrS1bGnjdbkZAZzEzwuMWjOzIm-LlX4XALiNWVd8"
SHEET_NAME_MAIN = "Sheet1"
SHEET_NAME_INTERVIEWS = "Interview_Records"

# Google Sheets Authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("disco-basis-453119-t1-24a839d4c451.json", scope)
client = gspread.authorize(creds)

# Load main student data
sheet_main = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME_MAIN)
data_main = sheet_main.get_all_records()
df_main = pd.DataFrame(data_main)

st.title("🎓 Student Dashboard & Full Record Entry")

# ------------------ EXISTING STUDENT SELECTION ------------------
student_ids = df_main["Student_ID"].tolist()
selected_id = st.selectbox("Select Student ID", student_ids)

student_df = df_main[df_main["Student_ID"] == selected_id].reset_index(drop=True)

if not student_df.empty:
    st.subheader(f"📌 Student Details: {student_df.at[0, 'Name']}")
    st.write("### 🧾 Student Information")
    st.dataframe(student_df.T.rename(columns={0: "Details"}))

    st.write("### 📊 Current Student Performance")
    metrics = ["Attendance (%)", "Mock_Interview"]
    values = [student_df.at[0, metric] for metric in metrics]

    fig, ax = plt.subplots()
    ax.bar(metrics, values, color=["blue", "green"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score / Percentage")
    ax.set_title(f"{student_df.at[0, 'Name']}'s Performance")
    for i, v in enumerate(values):
        ax.text(i, v + 2, str(v), ha='center', fontweight='bold')
    st.pyplot(fig)

# ------------------ NEW MEMBER / RECORD ENTRY ------------------
st.write("### 🆕 Add New Student / Member Entry")

# Extract all columns from sheet
columns = df_main.columns.tolist()

# Handle "Attendance (%)" and "Date" as auto-filled fields
form_data = {}
auto_fields = ["Attendance (%)", "Date"]

for col in columns:
    if col in auto_fields:
        continue
    form_data[col] = st.text_input(f"Enter {col}")

# Optional logic: you can customize how attendance is calculated
present_days = st.number_input("Enter number of Present Days", min_value=0, step=1)
total_days = st.number_input("Enter Total Working Days", min_value=1, step=1)

# Automatically calculate attendance percentage
if total_days > 0:
    attendance_percentage = round((present_days / total_days) * 100, 2)
else:
    attendance_percentage = 0

current_date = datetime.now().strftime("%d/%m/%Y")

# Submit button to add the new entry
if st.button("Submit New Member Record"):
    if any(v.strip() == "" for v in form_data.values()):
        st.warning("⚠️ Please fill all required fields.")
    else:
        new_row = [form_data.get(col, "") for col in columns if col not in auto_fields]
        new_row.append(attendance_percentage)
        new_row.append(current_date)
        sheet_main.append_row(new_row)
        st.success("✅ New member data added successfully!")

# ------------------ INTERVIEW PERFORMANCE VISUALIZATION ------------------
try:
    sheet_interviews = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME_INTERVIEWS)
    data_interviews = sheet_interviews.get_all_records()
    df_interviews = pd.DataFrame(data_interviews)

    student_scores = df_interviews[df_interviews["Student_ID"] == selected_id]

    if not student_scores.empty:
        st.write("### 📈 Interview Score Over Time")
        student_scores["Date"] = pd.to_datetime(student_scores["Date"], format="%d/%m/%Y")
        student_scores = student_scores.sort_values("Date")

        fig2, ax2 = plt.subplots()
        ax2.plot(student_scores["Date"], student_scores["Score"], marker='o', color='purple')
        ax2.set_title(f"{student_df.at[0, 'Name']}'s Interview Progress")
        ax2.set_ylabel("Score")
        ax2.set_xlabel("Date")
        ax2.grid(True)
        st.pyplot(fig2)
except Exception as e:
    st.warning("ℹ️ Could not fetch Interview Records (optional sheet).")
