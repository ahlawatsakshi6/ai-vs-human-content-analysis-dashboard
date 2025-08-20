import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Load dataset
df = pd.read_csv("C:\\Users\\Sakshi\\Desktop\\ai_vs_human_content_dataset.csv")

# Step 3: First look at data
print(df.head())      # First 5 rows
print(df.info())      # Data types & null values
print(df.describe())  # Summary statistics

# -----------------------------
# 🧹 DATA CLEANING
# -----------------------------

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')


# Check for missing values
print(df.isnull().sum())

# Drop duplicates if any
df.drop_duplicates(inplace=True)


# Standardize Author_Type values (AI/Human)
df['Author_Type'] = df['Author_Type'].str.strip().str.title()

# Recalculate Engagement_Score (in case needed)
df['Engagement_Score'] = df['Likes'] + df['Comments']*2 + df['Shares']*3



# -----------------------------
# 🔍 EXPLORATORY DATA ANALYSIS (EDA)
# -----------------------------

# 1. Average engagement by Author Type
avg_engagement = df.groupby("Author_Type")['Engagement_Score'].mean()
print(avg_engagement)

# 2. Total Likes, Comments, Shares by Author Type
totals = df.groupby("Author_Type")[['Likes','Comments','Shares']].sum()
print(totals)

# 3. Plot: Avg Engagement (AI vs Human)
sns.barplot(x=avg_engagement.index, y=avg_engagement.values)
plt.title("Average Engagement Score (AI vs Human)")
plt.ylabel("Engagement Score")
plt.show()

# 4. Trend over time
df.groupby(['Date','Author_Type'])['Engagement_Score'].mean().unstack().plot(kind='line')
plt.title("Engagement Trend Over Time")
plt.ylabel("Avg Engagement Score")
plt.show()

# 5. Content type analysis
sns.boxplot(data=df, x="Content_Type", y="Engagement_Score", hue="Author_Type")
plt.title("Engagement by Content Type (AI vs Human)")
plt.xticks(rotation=45)
plt.show()