
# 🌟Exercise 1: Introduction to Data Analysis (Easy)


# Objective: Understand the basic overview and significance of data analysis.
# Task:
# Write a short essay or report on the following topics:

# What is data analysis?
# Why is data analysis important in modern contexts?
# List and describe three areas where data analysis is applied today.
# Hint/Tip:

# Research current trends in data analysis and real-world examples to provide depth to your essay.


# 🌟Exercise 2: Dataset Loading and Initial Analysis


# Objective: Practice dataset loading from Kaggle and initial analysis.
# Task:
# for the following dataset : How Much Sleep Do Americans Really Get?, Global Trends in Mental Health Disorder and Credit Card Approvals.

# Load the dataset into Jupyter or Google Colab.
# Display the first few rows.
# Provide a brief dataset description.


# 🌟Exercise 3: Identifying Data Types


# Objective: Learn to identify different data types.
# Task:
# For the datasets from the previous exercise, categorize each column of it as either quantitative or qualitative and explain your reasoning.



# 🌟Exercise 4: Exploring Data Types


# Objective: Learn about different types of data in data analysis.
# Task:
# Load the Iris dataset using Kaggle into a Jupyter Notebook or Google Colaboratory Notebook.
# Identify and list which columns in your dataset are qualitative and which are quantitative.
# Write a brief description of why each column is classified as qualitative or quantitative.
# Tools: Jupyter Notebook, Python with Pandas library.



# 🌟Exercise 5: Basic Observation Skills in Data Analysis


# Objective: Develop observation skills for data analysis.
# Task:
# Load the How Much Sleep Do Americans Really Get? dataset into Jupyter or Google Colab.
# Identify columns that could be interesting for a specific type of analysis (e.g., trend analysis, group comparison) and explain your choice.
# Tools: Jupyter Notebook, Python with Pandas library.


# 🌟 Exercise 6: Identifying Data Types
# Below are various data sources. Identify whether each one is an example of structured or unstructured data.

# A company’s financial reports stored in an Excel file.
# Photographs uploaded to a social media platform.
# A collection of news articles on a website.
# Inventory data in a relational database.
# Recorded interviews from a market research study.


# 🌟 Exercise 7: Transformation Exercise
# For each of the following unstructured data sources, propose a method to convert it into structured data. Explain your reasoning.

# A series of blog posts about travel experiences.
# Audio recordings of customer service calls.
# Handwritten notes from a brainstorming session.
# A video tutorial on cooking.


# 🌟 Exercise 8 : Import a file from Kaggle
# Note: This dataset was originally sourced from Kaggle, but for easier access, it has been made available on GitHub.

# 👉 Please download the dataset directly from the GitHub repository to use it in this project.

# Import the train dataset. Use the train.csv file.
# Print the first few rows of the DataFrame.


# 🌟 Exercise 9 : Export a dataframe to excel format and JSON format.
# Create a simple dataframe.
# Export the dataframe to an excel file.
# Export the dataframe to a JSON file.


# 🌟 Exercise 10: Reading JSON Data
# Use a sample JSON dataset

# Import the JSON data from the provided URL.
# Use Pandas to read the JSON data.
# Display the first five entries of the data.


# Do this for me. Keep it simple. Exercise 1:
# Research current trends in data analysis and real-world examples to provide depth to your essay.

# For this one, take the examples of cars. Use data to understand the life of principal car components & their trending sells

# ============================================
# 🌟 Exercise 1: Introduction to Data Analysis
# ============================================

print("\n===== Exercise 1 =====\n")

essay = """
What is Data Analysis?
----------------------
Data analysis is the process of collecting, organizing, cleaning,
and interpreting data in order to discover useful information and
support decision-making.

Data analysis helps businesses and organizations understand patterns,
trends, and relationships within data.

Why is Data Analysis Important?
-------------------------------
Data analysis is important because modern companies generate huge
amounts of data every day. By analyzing this data, businesses can
make better decisions, improve performance, reduce costs, and predict
future trends.

Example in the Automobile Industry
----------------------------------
Car companies use data analysis to study:
- Car sales trends
- Battery life
- Engine performance
- Tire durability
- Maintenance history

For example:
- Electric vehicle companies analyze battery data to improve battery life.
- Car dealerships analyze trending car sales to understand customer demand.
- Maintenance companies use data to predict when components may fail.

Areas Where Data Analysis is Applied
------------------------------------
1. Healthcare
   - Disease tracking
   - Patient monitoring
   - Medical research

2. Finance and Banking
   - Fraud detection
   - Credit scoring
   - Risk management

3. Automobile Industry
   - Predictive maintenance
   - Vehicle performance analysis
   - Sales trend analysis
"""

print(essay)

# ============================================
# Import Libraries
# ============================================

import pandas as pd
import numpy as np
from pathlib import Path


# Small helper to try several likely filenames and return the first found DataFrame
def try_load_csv(candidates):
    """Try to load a CSV from a list of candidate paths. Return DataFrame or None."""
    for candidate in candidates:
        p = Path(candidate)
        if p.exists():
            try:
                df = pd.read_csv(p)
                print(f"Loaded: {p} (rows={len(df):,}, cols={len(df.columns):,})")
                print(df.head())
                print("\nInfo:")
                df.info()
                return df
            except Exception as e:
                print(f"Found file {p} but failed to read as CSV: {e}")
    print(f"None of the candidate files were found: {candidates}\n")
    return None


# ============================================
# 🌟 Exercise 2: Dataset Loading and Initial Analysis
# ============================================

print("\n===== Exercise 2 =====\n")

# Candidate names (try common variants and the local data/ folder)
sleep_candidates = [
    "sleep.csv",
    "Time Americans Spend Sleeping.csv",
    "data/Time Americans Spend Sleeping.csv",
    "data/sleep.csv",
]

mental_candidates = [
    "mental_health.csv",
    "Mental health Depression disorder Data.csv",
    "data/Mental health Depression disorder Data.csv",
    "data/mental_health.csv",
]

credit_candidates = [
    "credit_card_approvals.csv",
    "crx.csv",
    "data/crx.csv",
    "data/train.csv",
]

sleep_df = try_load_csv(sleep_candidates)
mental_df = try_load_csv(mental_candidates)
credit_df = try_load_csv(credit_candidates)

# ============================================
# 🌟 Exercise 3: Identifying Data Types
# ============================================

print("\n===== Exercise 3 =====\n")

# Function to classify columns
def classify_columns(df, dataset_name):

    print(f"\nColumn Types for {dataset_name}:\n")

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):
            print(f"{column} -> Quantitative")
        else:
            print(f"{column} -> Qualitative")
            
if sleep_df is not None:
    classify_columns(sleep_df, "Sleep Dataset")

if mental_df is not None:
    classify_columns(mental_df, "Mental Health Dataset")

if credit_df is not None:
    classify_columns(credit_df, "Credit Card Dataset")
    
# print("""
# Quantitative Data:
# - Numerical values
# - Example: Age, Income, Sleep Hours

# Qualitative Data:
# - Categories or labels
# - Example: Gender, Occupation, Country
# """)

# ============================================
# 🌟 Exercise 4: Exploring Data Types with Iris Dataset
# ============================================

print("\n===== Exercise 4 =====\n")

iris_candidates = ["Iris.csv", "data/Iris.csv", "data/iris.csv", "iris.csv"]
iris_df = try_load_csv(iris_candidates)

if iris_df is not None:
    print("\nColumn Classification:\n")
    for column in iris_df.columns:
        dtype = iris_df[column].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            print(f"{column} -> Quantitative")
        else:
            print(f"{column} -> Qualitative")
else:
    print("Iris.csv file not found.\n")

# ============================================
# 🌟 Exercise 5: Basic Observation Skills
# ============================================

print("\n===== Exercise 5 =====\n")

print("""
Interesting Columns for Analysis:
---------------------------------
1. Sleep Duration
    - Useful for trend analysis

2. Age Group
    - Useful for group comparison

3. Work Schedule
    - Helps analyze work impact on sleep

4. Stress Level
    - Helps study relationship between stress and sleep
""")

if sleep_df is not None:
     print("Sleep Dataset Columns:\n")
     print(list(sleep_df.columns))

     print("\nStatistical Summary:\n")
     print(sleep_df.describe(include='all'))
else:
     print("Sleep dataset not available.\n")

# ============================================
# 🌟 Exercise 6: Structured vs Unstructured Data
# ============================================

print("\n===== Exercise 6 =====\n")

data_types = {
    "Financial reports in Excel": "Structured",
    "Photographs on social media": "Unstructured",
    "News articles on websites": "Unstructured",
    "Inventory database": "Structured",
    "Recorded interviews": "Unstructured"
}

for item, dtype in data_types.items():
    print(f"{item} -> {dtype}")

# ============================================
# 🌟 Exercise 7: Transformation Exercise
# ============================================

print("\n===== Exercise 7 =====\n")

transformations = {
    "Blog posts": "Text extraction and keyword analysis",
    "Audio recordings": "Speech-to-text transcription",
    "Handwritten notes": "OCR (Optical Character Recognition)",
    "Cooking videos": "Video transcription and tagging"
}

for source, method in transformations.items():
    print(f"{source} -> {method}")

# ============================================
# 🌟 Exercise 8: Import a File from GitHub
# ============================================

print("\n===== Exercise 8 =====\n")

# Replace with your GitHub raw CSV link (example)
# github_url = "YOUR_GITHUB_RAW_FILE_URL"

# if "YOUR_GITHUB_RAW_FILE_URL" in github_url:
#     print("No GitHub URL provided. Replace the placeholder with the raw GitHub CSV URL to load it.")
# else:
#     try:
#         train_df = pd.read_csv(github_url)
#         print("GitHub Dataset Loaded Successfully\n")
#         print(train_df.head())
#     except Exception as e:
#         print(f"Could not load GitHub dataset: {e}\n")


train_df = pd.read_csv("data/train.csv")

print(train_df.head())

# ============================================
# 🌟 Exercise 9: Export DataFrame
# ============================================

print("\n===== Exercise 9 =====\n")

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 22]
}

df = pd.DataFrame(data)

print("Simple DataFrame:\n")
print(df)

# Export to Excel (with fallback to CSV if Excel writer not available)
try:
    df.to_excel("data.xlsx", index=False)
    print("\nExcel file exported successfully.")
except Exception as e:
    print(f"Could not export to Excel (to_excel failed): {e}\nFalling back to CSV.")
    df.to_csv("data.csv", index=False)
    print("CSV file exported successfully as fallback.")

# Export to JSON
try:
    df.to_json("data.json", orient="records")
    print("JSON file exported successfully.")
except Exception as e:
    print(f"Could not export to JSON: {e}")

# ============================================
# 🌟 Exercise 10: Reading JSON Data
# ============================================

print("\n===== Exercise 10 =====\n")

json_url = "data/posts.json"

try:
    json_df = pd.read_json(json_url)

    print("JSON Data Loaded Successfully\n")
    print(json_df.head())

except Exception as e:
    print(f"Could not load JSON data: {e}\n")

print("\n===== END OF EXERCISES =====")