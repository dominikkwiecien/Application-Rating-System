
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the applications data
applications = pd.read_csv('applications.csv')

# Data Cleaning
applications.drop_duplicates(subset='applicant_id', inplace=True)
applications['External Rating'].fillna(0, inplace=True)
applications['Education level'].fillna('Średnie', inplace=True)

# Load the industries data
industries = pd.read_csv('industries.csv')

# Merge the data
merged_data = pd.merge(applications, industries, on='Industry', how='left')

# Calculate the application rating
def calculate_rating(row):
    rating = 0
    if row['Age'] >= 35 and row['Age'] <= 55:
        rating += 20
    if row['Submission Day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        rating += 20
    if row['Marital Status'] == 'Married':
        rating += 20
    if row['City'] == 'Warsaw' or row['Region'] == 'Masovian Voivodeship':
        rating += 10
    rating += row['Score']
    if row['External Rating'] >= 7:
        rating += 20
    elif row['External Rating'] <= 2:
        rating -= 20
    if row['Amount'] == 0 or row['External Rating'] == 0:
        rating = 0
    return rating

merged_data['Rating'] = merged_data.apply(calculate_rating, axis=1)

# Filter applications with a rating greater than zero
accepted_applications = merged_data[merged_data['Rating'] > 0]

# Group by week and calculate average rating
accepted_applications['Week'] = pd.to_datetime(accepted_applications['Submission Date']).dt.isocalendar().week
weekly_average_ratings = accepted_applications.groupby('Week')['Rating'].mean()

# Plot the results
plt.figure(figsize=(10, 6))
weekly_average_ratings.plot(kind='bar', color='skyblue')
plt.title('Average Application Rating Per Week')
plt.xlabel('Week')
plt.ylabel('Average Rating')
plt.show()
