# import gspread
# import pandas as pd
# import streamlit as st
# import seaborn as sns
# import matplotlib.pyplot as plt
# from oauth2client.service_account import ServiceAccountCredentials

# # Function to Fetch Live Data from Google Sheets
# def load_live_data():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
#              "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
#     creds = ServiceAccountCredentials.from_json_keyfile_name("disco-basis-453119-t1-24a839d4c451.json", scope)
#     client = gspread.authorize(creds)

#     # Open Google Sheet
#     sheet = client.open("Student Dashboard Data").sheet1

#     # Fetch Data
#     data = sheet.get_all_records()
    
#     # Convert to DataFrame
#     df = pd.DataFrame(data)
#     return df

# # Load Live Data
# df = load_live_data()

# # Streamlit App Title
# st.title("📊 Real-Time Student Dashboard")

# # Refresh Button
# if st.button("Refresh Data"):
#     df = load_live_data()
#     st.success("Data Updated Successfully!")

# # Show Data
# st.write("### Student Data Overview")
# st.dataframe(df)

# # Attendance Distribution
# st.write("### Attendance Distribution")
# fig, ax = plt.subplots()
# sns.histplot(df["Attendance (%)"], bins=10, kde=True, ax=ax)
# st.pyplot(fig)

# # Mock Interview Score Distribution
# st.write("### Mock Interview Score Distribution")
# fig, ax = plt.subplots()
# sns.boxplot(x=df["Mock_Interview_Score"], ax=ax)
# st.pyplot(fig)

# # Scatter Plot of Attendance vs Performance
# st.write("### Attendance vs Mock Interview Score")
# fig, ax = plt.subplots()
# sns.scatterplot(x=df["Attendance (%)"], y=df["Mock_Interview_Score"], ax=ax)
# st.pyplot(fig)

# # Identify students with low attendance
# low_attendance = df[df["Attendance (%)"] < 75]
# st.write("### 🚨 Students with Low Attendance (< 75%)")
# st.dataframe(low_attendance)





# import streamlit as st
# import gspread
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from oauth2client.service_account import ServiceAccountCredentials

# # ------------------ GOOGLE SHEETS SETUP ------------------
# SHEET_ID = "139CNrS1bGnjdbkZAZzEzwuMWjOzIm-LlX4XALiNWVd8"  # Replace with your Google Sheet ID
# SHEET_NAME = "Student Dashboard Data"  # Replace with your sheet name

# # Authenticate Google Sheets API
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("disco-basis-453119-t1-24a839d4c451.json", scope)
# client = gspread.authorize(creds)

# # Open Google Sheet
# sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# # Load data from Google Sheets into a DataFrame
# data = sheet.get_all_records()
# df = pd.DataFrame(data)

# # ------------------ STREAMLIT UI ------------------

# st.title("📊 Student Dashboard")

# # Sidebar - Select Student
# student_ids = df["Student_ID"].tolist()
# selected_student = st.sidebar.selectbox("Select a Student", student_ids)

# # Fetch student details
# student_data = df[df["Student_ID"] == selected_student].iloc[0]

# st.write(f"### Student Name: {student_data['Name']}")
# st.write(f"📅 Last Updated: {student_data['Last_Updated']}")

# # Attendance Update
# attendance = st.number_input("Update Attendance (%)", min_value=0, max_value=100, value=student_data["Attendance (%)"])

# # Mock Interview Score Update
# mock_score = st.number_input("Update Mock Interview Score", min_value=0, max_value=10, value=student_data["Mock_Interview"])

# # Feedback Update
# feedback = st.text_area("Interview Feedback", student_data["Interview_Feedback"])

# # Update Button
# if st.button("Update Student Data"):
#     for i, row in df.iterrows():
#         if row["Student_ID"] == selected_student:
#             df.at[i, "Attendance (%)"] = attendance
#             df.at[i, "Mock_Interview"] = mock_score
#             df.at[i, "Interview_Feedback"] = feedback
#             df.at[i, "Last_Updated"] = pd.Timestamp.now().strftime("%d-%m-%Y %H:%M")
#             break

#     # Update Google Sheets
#     sheet.update([df.columns.values.tolist()] + df.values.tolist())
#     st.success("✅ Data updated successfully!")

# # ------------------ DATA VISUALIZATION ------------------

# st.write("## 📊 Performance Analysis")

# fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# # Attendance Visualization
# sns.barplot(x=df["Name"], y=df["Attendance (%)"], ax=axes[0], palette="Blues_r")
# axes[0].set_title("Attendance Percentage")
# axes[0].tick_params(axis="x", rotation=45)

# # Mock Interview Performance Visualization
# sns.barplot(x=df["Name"], y=df["Mock_Interview"], ax=axes[1], palette="Greens_r")
# axes[1].set_title("Mock Interview Scores")
# axes[1].tick_params(axis="x", rotation=45)

# st.pyplot(fig)




# import streamlit as st
# import gspread
# import pandas as pd
# import matplotlib.pyplot as plt
# from oauth2client.service_account import ServiceAccountCredentials

# # ------------------ GOOGLE SHEETS SETUP ------------------
# SHEET_ID = "139CNrS1bGnjdbkZAZzEzwuMWjOzIm-LlX4XALiNWVd8"  # Your Google Sheet ID
# SHEET_NAME = "Sheet1"  # Sheet name as shown in the bottom tab

# # Google Sheets Authentication
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("disco-basis-453119-t1-24a839d4c451.json", scope)
# client = gspread.authorize(creds)

# # Open Sheet
# sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
# data = sheet.get_all_records()
# df = pd.DataFrame(data)

# # ------------------ STREAMLIT DASHBOARD ------------------

# st.title("🎓 Student Individual Dashboard")

# # Select student by ID
# student_ids = df["Student_ID"].tolist()
# selected_id = st.selectbox("Select Student ID", student_ids)

# # Filter for selected student
# student_df = df[df["Student_ID"] == selected_id].reset_index(drop=True)

# if not student_df.empty:
#     st.subheader(f"📌 Student Details: {student_df.at[0, 'Name']}")
    
#     # Display individual data
#     st.write("### 🧾 Student Information")
#     st.dataframe(student_df.T.rename(columns={0: "Details"}))
    
#     # Plot student values
#     st.write("### 📊 Student Performance Visualization")
    
#     # Choose which metrics to display
#     metrics = ["Attendance (%)", "Mock_Interview"]
#     values = [student_df.at[0, metric] for metric in metrics]
    
#     fig, ax = plt.subplots()
#     ax.bar(metrics, values, color=["blue", "green"])
#     ax.set_ylim(0, 100)
#     ax.set_ylabel("Score / Percentage")
#     ax.set_title(f"{student_df.at[0, 'Name']}'s Performance")
    
#     for i, v in enumerate(values):
#         ax.text(i, v + 2, str(v), ha='center', fontweight='bold')
    
#     st.pyplot(fig)
# else:
#     st.warning("⚠️ Student not found.")


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
