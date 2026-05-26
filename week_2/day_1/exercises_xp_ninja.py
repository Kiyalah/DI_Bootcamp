# ============================================
# Exploratory Data Analysis (EDA) Project
# ============================================

# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Optional Libraries
# pip install seaborn textblob

import seaborn as sns
from textblob import TextBlob
import re

# ============================================
# Exercise 1 : General EDA Workflow
# ============================================

print("\n===== Exercise 1 : General EDA =====\n")

# Load dataset
# Replace with your dataset
df = pd.read_csv("your_dataset.csv")

# Display first rows
print(df.head())

# Dataset information
print("\nDataset Info:\n")
print(df.info())

# Statistical summary
print("\nDataset Description:\n")
print(df.describe())

# Missing values
print("\nMissing Values:\n")
print(df.isnull().sum())

# ============================================
# Exercise 2 : Titanic Dataset EDA
# ============================================

print("\n===== Exercise 2 : Titanic Dataset =====\n")

# Load Titanic dataset
titanic_df = pd.read_csv("Titanic.csv")

# First rows
print(titanic_df.head())

# Dataset info
print("\nInfo:\n")
print(titanic_df.info())

# Description
print("\nDescription:\n")
print(titanic_df.describe())

# Missing values
print("\nMissing Values:\n")
print(titanic_df.isnull().sum())

# ============================================
# Data Cleaning
# ============================================

# Fill missing Age values
titanic_df["Age"].fillna(
    titanic_df["Age"].median(),
    inplace=True
)

# Fill missing Embarked values
titanic_df["Embarked"].fillna(
    titanic_df["Embarked"].mode()[0],
    inplace=True
)

# Convert categorical variables
titanic_df["Sex"] = titanic_df["Sex"].map({
    "male": 0,
    "female": 1
})

# ============================================
# Univariate Analysis
# ============================================

plt.hist(titanic_df["Age"])
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

# ============================================
# Bivariate Analysis
# ============================================

sns.barplot(
    x="Pclass",
    y="Survived",
    data=titanic_df
)

plt.title("Survival Rate by Passenger Class")
plt.show()

# ============================================
# Correlation Heatmap
# ============================================

numeric_titanic = titanic_df.select_dtypes(
    include=["int64", "float64"]
)

sns.heatmap(
    numeric_titanic.corr(),
    annot=True
)

plt.title("Correlation Heatmap")
plt.show()

# ============================================
# Insights
# ============================================

print("""
Key Insights:
- Higher-class passengers had better survival rates.
- Females survived more than males.
- Younger passengers had slightly better survival chances.
""")

# ============================================
# Exercise 3 : Iris Dataset EDA
# ============================================

print("\n===== Exercise 3 : Iris Dataset =====\n")

# Load Iris dataset
iris_df = pd.read_csv("Iris.csv")

# Display rows
print(iris_df.head())

# Info
print("\nInfo:\n")
print(iris_df.info())

# Description
print("\nDescription:\n")
print(iris_df.describe())

# Species distribution
print("\nSpecies Distribution:\n")
print(iris_df["Species"].value_counts())

# ============================================
# Histograms
# ============================================

iris_df.hist(figsize=(10,8))
plt.show()

# ============================================
# Scatter Plot
# ============================================

sns.scatterplot(
    x="SepalLengthCm",
    y="PetalLengthCm",
    hue="Species",
    data=iris_df
)

plt.title("Sepal Length vs Petal Length")
plt.show()

# ============================================
# Boxplot
# ============================================

sns.boxplot(
    x="Species",
    y="PetalLengthCm",
    data=iris_df
)

plt.title("Petal Length by Species")
plt.show()

# ============================================
# Pairplot
# ============================================

sns.pairplot(
    iris_df,
    hue="Species"
)

plt.show()

# ============================================
# Heatmap
# ============================================

numeric_iris = iris_df.select_dtypes(
    include=["int64", "float64"]
)

sns.heatmap(
    numeric_iris.corr(),
    annot=True
)

plt.title("Iris Correlation Heatmap")
plt.show()

# ============================================
# Iris Insights
# ============================================

print("""
Iris Insights:
- Setosa flowers have smaller petals.
- Petal dimensions strongly differentiate species.
- Petal length and width are highly correlated.
""")

# ============================================
# Exercise 4 : Structured vs Unstructured Data
# ============================================

print("\n===== Exercise 4 =====\n")

# Structured Data
sales_df = pd.read_csv("sales.csv")

print("\nSales Dataset:\n")
print(sales_df.head())

# Unstructured Data
tickets_df = pd.read_csv("support_tickets.csv")

print("\nSupport Tickets Dataset:\n")
print(tickets_df.head())

# ============================================
# Sentiment Analysis
# ============================================

def get_sentiment(text):

    analysis = TextBlob(str(text))

    return analysis.sentiment.polarity

tickets_df["sentiment_score"] = tickets_df[
    "ticket_text"
].apply(get_sentiment)

print(tickets_df.head())

# ============================================
# Challenges
# ============================================

print("""
Challenges with Unstructured Data:
- Text cleaning is required
- Data is inconsistent
- Difficult to analyze directly

Structured Data Advantages:
- Easier to organize
- Easier to analyze
- Better for machine learning
""")

# ============================================
# Exercise 5 : Convert Tweets to Structured Data
# ============================================

print("\n===== Exercise 5 =====\n")

tweets_df = pd.read_csv("tweets.csv")

print(tweets_df.head())

# ============================================
# Extract Hashtags
# ============================================

def extract_hashtags(text):

    return re.findall(r"#(\w+)", str(text))

# Extract Mentions
def extract_mentions(text):

    return re.findall(r"@(\w+)", str(text))

tweets_df["hashtags"] = tweets_df["tweet"].apply(
    extract_hashtags
)

tweets_df["mentions"] = tweets_df["tweet"].apply(
    extract_mentions
)

# ============================================
# Structured Data
# ============================================

structured_tweets = tweets_df[
    ["tweet", "hashtags", "mentions", "sentiment"]
]

print("\nStructured Tweets:\n")
print(structured_tweets.head())

# ============================================
# Basic Analysis
# ============================================

print("\nSentiment Distribution:\n")
print(
    structured_tweets["sentiment"].value_counts()
)

print("""
Insights:
- Structured data is easier to analyze.
- Hashtags help identify trending topics.
- Mentions help identify interactions between users.
""")

print("\n===== END OF EDA PROJECT =====")