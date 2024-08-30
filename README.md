
# Application Rating Project

This repository contains a Python project that focuses on data cleaning and application rating calculation based on predefined criteria. The project demonstrates skills in data manipulation, cleansing, and analysis using the Pandas library. The tasks were structured to meet specific acceptance criteria, ensuring a systematic approach to data handling and the generation of meaningful insights.

## Project Overview

The project aims to process application data, clean it, and calculate ratings for each application based on several criteria. The final output includes a filtered dataset of accepted applications and a visual representation of the average application ratings per week.

### Data Sources

The project utilizes two main data files:

1. **applications.csv** - Contains application details, including applicant information, education level, and external ratings.
2. **industries.csv** - Provides industry-related scores that contribute to the overall application rating.

### Workflow and Steps

The project follows a step-by-step approach:

1. **Data Loading and Initial Cleaning**:
    - Load the `applications.csv` file into a Pandas DataFrame.
    - Remove duplicate entries based on `applicant_id`.
    - Fill missing values in the `External Rating` column with zeros.
    - Fill missing values in the `Education level` column with the text "Średnie".

2. **Data Merging**:
    - Load the `industries.csv` file and merge it with the existing DataFrame based on the industry-related data, particularly the score.

3. **Application Rating Calculation**:
    - Ratings are calculated on a scale of 0 to 100 based on six criteria:
        - Add 20 points if the applicant's age is between 35 and 55.
        - Add 20 points if the application was submitted during the week (excluding weekends).
        - Add 20 points if the applicant is married.
        - Add 10 points if the applicant resides in Warsaw or the Masovian Voivodeship.
        - Add the score from `industries.csv` (ranging from 0 to 20 points).
        - Add or subtract points based on the `External Rating`:
            - Add 20 points if `External Rating` ≥ 7.
            - Subtract 20 points if `External Rating` ≤ 2.
    - Applications with an `Amount` value of zero or an `External Rating` of zero receive a rating of zero.

4. **Filtering and Grouping**:
    - Remove applications with a rating of zero or less from the dataset.
    - Group the remaining data by the week of submission and calculate the average rating for each week.

5. **Visualization**:
    - Create a plot representing the average rating of accepted applications for each week.

### Results and Visualizations

The project outputs a cleaned and filtered DataFrame with only the accepted applications. Additionally, it generates a plot that visualizes the average ratings of these applications grouped by week, providing insights into trends over time.

### Python Code

Below is the complete Python code used in this project:

```python
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
```

### Installation and Usage

To run this project on your local machine:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/application-rating-project.git
    cd application-rating-project
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Execute the Jupyter Notebook or Python script:

    ```bash
    jupyter notebook application_rating.ipynb
    ```

### Files in the Repository

- `application_rating.ipynb` - The Jupyter Notebook containing the full implementation of the project.
- `applications.csv` - The dataset containing application information.
- `industries.csv` - The dataset containing industry-related scores.
- `README.md` - This file, explaining the project and providing instructions for usage.

### Conclusion

This project demonstrates a comprehensive approach to data cleaning and application rating. It is a great example of how to use Python and Pandas to handle real-world data processing tasks and generate insightful visualizations.
