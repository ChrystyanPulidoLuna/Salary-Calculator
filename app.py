import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import os

# Define a relative path to the folder where the file should be located
file_path = 'Salary_Data.csv'

# Check if the file exists
if not os.path.isfile(file_path):
    messagebox.showerror("Error", f"{file_path} not found in the current directory.")
    exit()

# Load the dataset
try:
    df = pd.read_csv(file_path)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load CSV: {e}")
    exit()

# Extract unique values for dropdowns
job_titles = sorted(df['Job Title'].dropna().unique().tolist())
education_levels = ["Bachelor's", "Master's", "PhD"]
ages = list(range(18, 81))  # Age range from 18 to 80

# Convert categorical education levels to numerical for analysis
education_mapping = {"Bachelor's": 1, "Master's": 2, "PhD": 3}
df['Education Level'] = df['Education Level'].map(education_mapping)

# Function to show top professions
def show_top_professions():
    top_professions = df.groupby("Job Title")["Salary"].mean().sort_values(ascending=False).head(5)
    plt.figure(figsize=(6, 4))
    plt.bar(top_professions.index, top_professions.values, color="#2196F3")
    plt.xlabel("Professions", fontsize=12)
    plt.ylabel("Average Salary ($)", fontsize=12)
    plt.title("Top 5 Highest Paying Professions", fontsize=14)
    plt.xticks(rotation=45)
    plt.show()

# Function to analyze salary by age
def analyze_by_age():
    age_salaries = df.groupby("Age")["Salary"].mean()
    plt.figure(figsize=(6, 4))
    plt.plot(age_salaries.index, age_salaries.values, marker="o", linestyle="-", color="#E91E63")
    plt.xlabel("Age", fontsize=12)
    plt.ylabel("Average Salary ($)", fontsize=12)
    plt.title("Salary Trend by Age", fontsize=14)
    plt.show()

# Function to analyze salary by gender
def analyze_by_gender():
    gender_salaries = df.groupby("Gender")["Salary"].mean()
    plt.figure(figsize=(6, 4))
    plt.bar(gender_salaries.index, gender_salaries.values, color=["#FF4081", "#03A9F4"])
    plt.xlabel("Gender", fontsize=12)
    plt.ylabel("Average Salary ($)", fontsize=12)
    plt.title("Salary Differences by Gender", fontsize=14)
    plt.show()

# Function to analyze salary by education
def analyze_by_education():
    education_salaries = df.groupby("Education Level")["Salary"].mean()
    plt.figure(figsize=(6, 4))
    plt.bar(["Bachelor's", "Master's", "PhD"], education_salaries.values, color=["#FFEB3B", "#FF9800", "#4CAF50"])
    plt.xlabel("Education Level", fontsize=12)
    plt.ylabel("Average Salary ($)", fontsize=12)
    plt.title("Salary Trends by Education Level", fontsize=14)
    plt.show()

# Function to analyze salary by experience
def analyze_by_experience():
    experience_salaries = df.groupby("Years of Experience")["Salary"].mean()
    plt.figure(figsize=(6, 4))
    plt.plot(experience_salaries.index, experience_salaries.values, marker="s", linestyle="-", color="#673AB7")
    plt.xlabel("Years of Experience", fontsize=12)
    plt.ylabel("Average Salary ($)", fontsize=12)
    plt.title("Salary Growth by Experience", fontsize=14)
    plt.show()

# Function to estimate salary
def estimate_salary():
    """Estimates salary and generates a comparison graph."""
    job = job_title_var.get()
    education = education_mapping.get(education_level_var.get(), 0)
    age = int(age_var.get()) if age_var.get().isdigit() else None

    if not job or not age:
        messagebox.showerror("Error", "Please select a job title, education level, and age.")
        return

    # Filter data based on the job title
    filtered_data = df[df["Job Title"] == job]

    if filtered_data.empty:
        estimated_salary = df["Salary"].mean()  # Fallback to overall average if no data found
        avg_salary_by_job = estimated_salary
    else:
        # Calculate the average salary based on job title
        avg_salary_by_job = filtered_data["Salary"].mean()

        # Calculate the average salary by education level
        avg_salary_by_education = df[df["Education Level"] == education]["Salary"].mean()

        # Calculate the average salary by age
        avg_salary_by_age = df[df["Age"] == age]["Salary"].mean()

        # Apply weighted adjustment with a reasonable distribution of the weights
        salary_values = [s for s in [avg_salary_by_job, avg_salary_by_education, avg_salary_by_age] if not pd.isna(s)]
        estimated_salary = (
            (avg_salary_by_job * 0.8) +  # Moderate weight to job title
            (avg_salary_by_education * 0.1 if not pd.isna(avg_salary_by_education) else 0) +  # Moderate weight for education
            (avg_salary_by_age * 0.1 if not pd.isna(avg_salary_by_age) else 0)  # Lesser weight for age
        )

    # Ensure the estimated salary is within a reasonable range of the job title's average salary
    estimated_salary = max(min(estimated_salary, avg_salary_by_job * 1.5), avg_salary_by_job * 0.5)

    # Display salary estimate
    messagebox.showinfo("Estimated Salary", f"Estimated Salary: ${estimated_salary:,.2f}")

    # Generate Salary Comparison Graph
    plt.figure(figsize=(6, 4))
    plt.bar(["Average Salary", "Estimated Salary"], [avg_salary_by_job, estimated_salary], color=["#2196F3", "#FF9800"])
    plt.ylabel("Salary ($)")
    plt.title(f"Salary Comparison for {job}")
    plt.show()

# Create the main application window
root = tk.Tk()
root.title("Salary Data Estimator")
root.geometry("1000x600")
root.configure(bg="#121212")  # Dark background

# Intro Screen
intro_frame = tk.Frame(root, bg="#121212")
intro_frame.pack(fill="both", expand=True)

intro_label = tk.Label(intro_frame, text="Salary Data provided by Kaggle", font=("Arial", 24, "bold"), fg="white", bg="#121212")
intro_label.pack(expand=True)

small_text = tk.Label(intro_frame, text="Press any key to begin", font=("Arial", 12), fg="gray", bg="#121212")
small_text.pack(side="bottom", pady=20)

# Function to start the main interface and prevent multiple activations
def start_application(event):
    root.unbind("<KeyPress>")  # Unbind event to prevent multiple starts
    intro_frame.destroy()  # Remove intro screen
    build_ui()  # Call function to build the UI properly
    root.update()  # Force refresh

# Bind keypress to start the app (and unbind after first press)
root.bind("<KeyPress>", start_application)

# Function to build the main UI correctly
def build_ui():
    global content_frame, job_title_var, education_level_var, age_var

    # Initialize Tkinter variables after root is created
    job_title_var = tk.StringVar()
    education_level_var = tk.StringVar()
    age_var = tk.StringVar()

    main_frame = tk.Frame(root, bg="#121212")
    main_frame.pack(fill="both", expand=True)

    # Sidebar
    sidebar = tk.Frame(main_frame, width=220, bg="#1E1E2F")
    sidebar.pack(fill="y", side="left")

    sidebar_label = tk.Label(sidebar, text="Sort Data", font=("Arial", 14, "bold"), fg="white", bg="#1E1E2F")
    sidebar_label.pack(pady=10)

    # Sidebar Buttons (Linked to Real Functions)
    options = [
        ("🏆 Top Professions", show_top_professions),
        ("📊 Analyze by Age", analyze_by_age),
        ("👤 Analyze by Gender", analyze_by_gender),
        ("🎓 Analyze by Education", analyze_by_education),
        ("📅 Analyze by Experience", analyze_by_experience),
    ]

    for text, command in options:
        btn = tk.Button(sidebar, text=text, command=command, font=("Arial", 12), bg="#30304B", fg="white", width=25, height=2, bd=0)
        btn.pack(pady=5)

    # Main Content Area
    content_frame = tk.Frame(main_frame, bg="#121212")
    content_frame.pack(fill="both", expand=True)
    content_frame.pack_propagate(False)  # Ensures proper sizing

    # Title Label
    title_label = tk.Label(content_frame, text="Salary Estimation Calculator", font=("Arial", 20, "bold"), fg="white", bg="#121212")
    title_label.pack(pady=20)

    # Job Title Dropdown
    tk.Label(content_frame, text="Select Job Title:", fg="white", bg="#121212", font=("Arial", 12)).pack(pady=(10, 0))
    job_dropdown = ttk.Combobox(content_frame, textvariable=job_title_var, values=job_titles, state="readonly", width=30)
    job_dropdown.pack()

    # Education Level Dropdown
    tk.Label(content_frame, text="Select Education Level:", fg="white", bg="#121212", font=("Arial", 12)).pack(pady=(10, 0))
    education_dropdown = ttk.Combobox(content_frame, textvariable=education_level_var, values=education_levels, state="readonly", width=30)
    education_dropdown.pack()

    # Age Dropdown
    tk.Label(content_frame, text="Select Age:", fg="white", bg="#121212", font=("Arial", 12)).pack(pady=(10, 0))
    age_dropdown = ttk.Combobox(content_frame, textvariable=age_var, values=ages, state="readonly", width=30)
    age_dropdown.pack()

    # Calculate Button
    calc_button = tk.Button(content_frame, text="💰 Calculate Salary", command=estimate_salary,
                            font=("Arial", 14, "bold"), bg="#FF9800", fg="white", width=20, height=2, bd=0)
    calc_button.pack(pady=20)

    # Refresh UI
    root.update()

# Run the application
root.mainloop()
