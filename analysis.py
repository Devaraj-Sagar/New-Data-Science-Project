import pandas as pd

#Loading files 
try:
    users = pd.read_csv('Users.csv')
    courses = pd.read_csv('Courses.csv')
    transactions = pd.read_csv('Transactions.csv')
    print("Files loaded successfully!")
except FileNotFoundError:
    print("Error: Files not found. Ensure the CSVs are in the same folder as this script.")
    exit()

# Joining the tables using UserID and CourseID
df = transactions.merge(users, on='UserID').merge(courses, on='CourseID')
print(f"Data Integration complete. Total records: {len(df)}")


#age bands: <18, 18-25, 26-35, 36-45, 45+
bins = [0, 18, 25, 35, 45, 100]
labels = ['<18', '18-25', '26-35', '36-45', '45+']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)

print("\n--- Age Distribution ---")
print(df['AgeGroup'].value_counts().sort_index())


# Count enrollments by Category and Level

print("\n--- Top 5 Course Categories ---")
print(df['CourseCategory'].value_counts().head(5))

print("\n--- Enrollment by Course Level ---")
print(df['CourseLevel'].value_counts())

# Average courses taken per learner

avg_courses = len(df) / df['UserID'].nunique()
print(f"\nAverage courses per learner: {avg_courses:.2f}")

# Saving the final integrated data for your Streamlit app
df.to_csv('integrated_edupro_data.csv', index=False)
print("\nProcessed data saved as 'integrated_edupro_data.csv'")