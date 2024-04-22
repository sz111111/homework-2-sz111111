# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 20:32:01 2024

@author: ChelseySSS
"""

# PPHA 30537
# Spring 2024
# Homework 2

# SHIHAN ZHAO
# sz111111

# Due date: Sunday April 21st before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.  Using functions for organization will be rewarded.

##################

# To answer these questions, you will use the csv document included in
# your repo.  In nst-est2022-alldata.csv: SUMLEV is the level of aggregation,
# where 10 is the whole US, and other values represent smaller geographies. 
# REGION is the fips code for the US region. STATE is the fips code for the 
# US state.  The other values are as per the data dictionary at:
# https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2020-2022/NST-EST2022-ALLDATA.pdf
# Note that each question will build on the modified dataframe from the
# question before.  Make sure the SettingWithCopyWarning is not raised.

# PART 1: Macro Data Exploration

# Question 1.1: Load the population estimates file into a dataframe. Specify
# an absolute path using the Python os library to join filenames, so that
# anyone who clones your homework repo only needs to update one for all
# loading to work.

import os
import pandas as pd

# Define the base directory where the files are located
base_dir = r'C:\Users\ChelseySSS\Desktop'

# Define the filename of the population estimates data
filename = 'NST-EST2022-ALLDATA.csv'

# Join the base directory and filename to create a full path
file_path = os.path.join(base_dir, filename)

# Load the population estimates CSV into a DataFrame
population_data = pd.read_csv(file_path)

# Display the first few rows of the DataFrame
print(population_data.head())



# Question 1.2: Your data only includes fips codes for states (STATE).  Use 
# the us library to crosswalk fips codes to state abbreviations.  Drop the
# fips codes.

import us

# Define a function to convert FIPS to state abbreviations
def fips_to_abbreviation(fips_code):
    state = us.states.lookup(str(fips_code).zfill(2))
    return state.abbr if state else None

# Apply the function to the STATE column to create a new column for state abbreviations
population_data['State_Abbreviation'] = population_data['STATE'].apply(fips_to_abbreviation)

# Drop the original STATE column
population_data.drop(columns='STATE', inplace=True)

# Display the first few rows to confirm the changes
print(population_data.head())



# Question 1.3: Then show code doing some basic exploration of the
# dataframe; imagine you are an intern and are handed a dataset that your
# boss isn't familiar with, and asks you to summarize for them.  Do not 
# create plots or use groupby; we will do that in future homeworks.  
# Show the relevant exploration output with print() statements.

# Load the dataset as previously 
base_directory = "C:/Users/ChelseySSS/Desktop"
filename = "NST-EST2022-ALLDATA.csv"
file_path = os.path.join(base_directory, filename)
population_data = pd.read_csv(file_path)

# Show the first few rows of the dataset
print("First few rows of the dataset:")
print(population_data.head())

# Display the structure of the DataFrame
print("\nData types and non-null counts of each column:")
print(population_data.info())

# Summarize the number of non-null entries and check for missing values
print("\nSummary of missing values per column:")
print(population_data.isnull().sum())

# Display summary statistics of numeric columns
print("\nSummary statistics of numeric columns:")
print(population_data.describe())

# Count the number of unique values in each column to understand variability
print("\nNumber of unique values per column:")
print(population_data.nunique())



# Question 1.4: Subset the data so that only observations for individual
# US states remain, and only state abbreviations and data for the population
# estimates in 2020-2022 remain.  The dataframe should now have 4 columns.

# Convert FIPS codes to state abbreviations using the 'us' library
population_data['STATE'] = population_data['STATE'].apply(lambda x: us.states.lookup(str(x).zfill(2)).abbr if us.states.lookup(str(x).zfill(2)) else None)

# Filter out rows that are not individual US states
# Assuming that STATE has values for states only now after conversion; adjust filtering based on actual data inspection
population_data = population_data[population_data['STATE'].notna()]

# Select only the columns for state abbreviations and the years 2020-2022
columns_needed = ['STATE', 'POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022']
population_data = population_data[columns_needed]

# Drop rows with missing values
population_data.dropna(inplace=True)

# Filter out rows with state abbreviations that are not exactly 2 characters long
population_data = population_data[population_data['STATE'].apply(lambda x: len(x) == 2)]

# Rename 'STATE' to 'State_Abbreviation' for clarity
population_data.rename(columns={'STATE': 'State_Abbreviation'}, inplace=True)

# Display the first few rows of the modified DataFrame
print(population_data.head())



# Question 1.5: Show only the 10 largest states by 2021 population estimates,
# in decending order.

# Check if 'STATE' column exists and then convert FIPS codes to state abbreviations using the 'us' library
if 'STATE' in population_data.columns:
    population_data['State_Abbreviation'] = population_data['STATE'].apply(lambda x: us.states.lookup(str(x).zfill(2)).abbr if us.states.lookup(str(x).zfill(2)) else None)
    # Drop the 'STATE' column after conversion to avoid confusion
    population_data.drop(columns='STATE', inplace=True)

# Ensure that the DataFrame contains 'State_Abbreviation' before proceeding
if 'State_Abbreviation' in population_data.columns:
    # Select only the columns for state abbreviations and the years 2020-2022
    columns_needed = ['State_Abbreviation', 'POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022']
    population_data = population_data[columns_needed]

    # Drop rows with missing values
    population_data.dropna(inplace=True)

    # Filter out rows with state abbreviations that are not exactly 2 characters long
    population_data = population_data[population_data['State_Abbreviation'].apply(lambda x: len(x) == 2)]

    # Sorting the DataFrame by 2021 population estimates in descending order
    population_data_sorted = population_data.sort_values('POPESTIMATE2021', ascending=False)

    # Displaying the top 10 states
    top_10_states = population_data_sorted.head(10)
    print(top_10_states)



# Question 1.6: Create a new column, POPCHANGE, that is equal to the change in
# population from 2020 to 2022.  How many states gained and how many lost
# population between these estimates?

# Convert FIPS codes to state abbreviations using the 'us' library
if 'STATE' in population_data.columns:
    population_data['State_Abbreviation'] = population_data['STATE'].apply(lambda x: us.states.lookup(str(x).zfill(2)).abbr if us.states.lookup(str(x).zfill(2)) else None)
    population_data.drop(columns='STATE', inplace=True)

# Filter for only valid state abbreviations
population_data = population_data[population_data['State_Abbreviation'].notna() & population_data['State_Abbreviation'].apply(lambda x: len(x) == 2)]

# Select the necessary columns
columns_needed = ['State_Abbreviation', 'POPESTIMATE2020', 'POPESTIMATE2022']
population_data = population_data[columns_needed]

# Create the POPCHANGE column
population_data['POPCHANGE'] = population_data['POPESTIMATE2022'] - population_data['POPESTIMATE2020']

# Count how many states gained population (POPCHANGE > 0)
states_gained = population_data[population_data['POPCHANGE'] > 0].shape[0]

# Count how many states lost population (POPCHANGE < 0)
states_lost = population_data[population_data['POPCHANGE'] < 0].shape[0]

# Display the counts
print(f"Number of states that gained population: {states_gained}")
print(f"Number of states that lost population: {states_lost}")

# Display the states with their population change
print(population_data[['State_Abbreviation', 'POPCHANGE']])



# Question 1.7: Show all the states that had an estimated change in either
# direction of smaller than 1000 people. 

# Filter for only valid state abbreviations
population_data = population_data[population_data['State_Abbreviation'].notna() & population_data['State_Abbreviation'].apply(lambda x: len(x) == 2)]

# Select the necessary columns
columns_needed = ['State_Abbreviation', 'POPESTIMATE2020', 'POPESTIMATE2022']
population_data = population_data[columns_needed]

# Create the POPCHANGE column
population_data['POPCHANGE'] = population_data['POPESTIMATE2022'] - population_data['POPESTIMATE2020']

# Filter to find states with a population change less than 1000 in absolute value
small_change_states = population_data[population_data['POPCHANGE'].abs() < 1000]

# Display the states and their population changes
print(small_change_states[['State_Abbreviation', 'POPCHANGE']])



# Question 1.8: Show the states that had a population growth or loss of 
# greater than one standard deviation.  Do not create a new column in your
# dataframe.  Sort the result by decending order of the magnitude of 
# POPCHANGE.

# Calculate the population change and determine its standard deviation
population_change = population_data['POPESTIMATE2022'] - population_data['POPESTIMATE2020']
std_dev = population_change.std()

# Identify states with changes greater than one standard deviation
significant_changes = population_data[(population_change.abs() > std_dev)]

# Sort these states by the magnitude of the population change in descending order
significant_changes = significant_changes.assign(POPCHANGE=population_change)
significant_changes = significant_changes.sort_values('POPCHANGE', ascending=False)

# Display the filtered and sorted list
print(significant_changes[['State_Abbreviation', 'POPCHANGE']])



#PART 2: Data manipulation

# Question 2.1: Reshape the data from wide to long, using the wide_to_long function,
# making sure you reset the index to the default values if any of your data is located 
# in the index.  What happened to the POPCHANGE column, and why should it be dropped?
# Explain in a brief (1-2 line) comment.

# Make sure the DataFrame has a suitable index
population_data.reset_index(drop=True, inplace=True)

# Reshape the data from wide to long
long_format = pd.wide_to_long(population_data, stubnames='POPESTIMATE', i='State_Abbreviation', j='Year', sep='')

# Reset the index to make 'State_Abbreviation' and 'Year' into columns
long_format.reset_index(inplace=True)

# Display the first few rows of the reshaped DataFrame
print(long_format.head())

## The POPCHANGE column represents the difference in population estimates between two different years, but when we reshape the data to long format, each row should represent only one point in time. 
## This derived column (POPCHANGE) does not fit into the long format where each row is supposed to capture a single, undivided metric at a specific time. It should be dropped prior to reshaping because it doesn't correspond to a single year. 



# Question 2.2: Repeat the reshaping using the melt method.  Clean up the result so
# that it is the same as the result from 2.1 (without the POPCHANGE column).

# Make sure the DataFrame has a suitable index
population_data.reset_index(drop=True, inplace=True)

# Use melt to reshape the data, assuming POPESTIMATE2020, POPESTIMATE2022 columns exist
long_format = pd.melt(population_data, id_vars=['State_Abbreviation'], 
                      value_vars=['POPESTIMATE2020', 'POPESTIMATE2022'],
                      var_name='Year', value_name='POPESTIMATE')

# Clean up the 'Year' column to show just the year
long_format['Year'] = long_format['Year'].str.extract('(\d+)$')

# Display the first few rows of the reshaped DataFrame
print(long_format.head())



# Question 2.3: Open the state-visits.xlsx file in Excel, and fill in the VISITED
# column with a dummy variable for whether you've visited a state or not.  If you
# haven't been to many states, then filling in a random selection of them
# is fine too.  Save your changes.  Then load the xlsx file as a dataframe in
# Python, and merge the VISITED column into your original wide-form population 
# dataframe, only keeping values that appear in both dataframes.  Are any 
# observations dropped from this?  Show code where you investigate your merge, 
# and display any observations that weren't in both dataframes.

# Load the population data
base_directory = "C:/Users/ChelseySSS/Desktop"
population_filename = "NST-EST2022-ALLDATA.csv"
population_file_path = os.path.join(base_directory, population_filename)
population_data = pd.read_csv(population_file_path)

# Convert FIPS codes to state abbreviations using the 'us' library
population_data['State_Abbreviation'] = population_data['STATE'].apply(lambda x: us.states.lookup(str(x).zfill(2)).abbr if us.states.lookup(str(x).zfill(2)) else None)

# Drop the original 'STATE' column
population_data.drop(columns='STATE', inplace=True)

# Load the state visits data
visits_filename = "state-visits.xlsx"
visits_file_path = os.path.join(base_directory, visits_filename)
visits_data = pd.read_excel(visits_file_path)

# Merge the VISITED column into the population dataframe using an inner join
merged_data = population_data.merge(visits_data[['STATE', 'VISITED']], 
                                    left_on='State_Abbreviation', 
                                    right_on='STATE', 
                                    how='inner')

# Drop the duplicate 'STATE' column from the visits data 
merged_data.drop(columns=['STATE'], inplace=True)

# Check for states that were in the original population data but not in the visits data
unmatched_states = population_data[~population_data['State_Abbreviation'].isin(visits_data['STATE'])]
print("States in population data but not in visits data:")
print(unmatched_states['State_Abbreviation'])

# Check for states that were in the visits data but not in the original population data
unmatched_visits = visits_data[~visits_data['STATE'].isin(population_data['State_Abbreviation'])]
print("\nStates in visits data but not in population data:")
print(unmatched_visits['STATE'])

# Display the first few rows of the merged DataFrame
print("\nMerged DataFrame:")
print(merged_data.head())



# Question 2.4: The file policy_uncertainty.xlsx contains monthly measures of 
# economic policy uncertainty for each state, beginning in different years for
# each state but ending in 2022 for all states.  The EPU_National column esimates
# uncertainty from national sources, EPU_State from state, and EPU_Composite 
# from both (EPU-N, EPU-S, EPU-C).  Load it as a dataframe, then calculate 
# the mean EPU-C value for each state/year, leaving only columns for state, 
# year, and EPU_Composite, with each row being a unique state-year combination.

# Load the policy uncertainty data
base_directory = "C:/Users/ChelseySSS/Desktop"
policy_uncertainty_filename = "policy_uncertainty.xlsx"
policy_uncertainty_file_path = os.path.join(base_directory, policy_uncertainty_filename)
policy_uncertainty_data = pd.read_excel(policy_uncertainty_file_path)

# Calculate the mean EPU_Composite value for each state/year
# Since the data contains a 'year' column, there's no need to extract the year from a date column
epu_composite_mean = (policy_uncertainty_data
                      .groupby(['state', 'year'])['EPU_Composite']
                      .mean()
                      .reset_index())

# Rename the columns for consistency 
epu_composite_mean.columns = ['State', 'Year', 'EPU_Composite']

# Display the first few rows of the resulting DataFrame
print(epu_composite_mean.head())



# Question 2.5) Reshape the EPU data into wide format so that each row is unique 
# by state, and the columns represent the EPU-C values for the years 2022, 
# 2021, and 2020. 

# Policy_uncertainty_data is loaded 
base_directory = "C:/Users/ChelseySSS/Desktop"
policy_uncertainty_filename = "policy_uncertainty.xlsx"
policy_uncertainty_file_path = os.path.join(base_directory, policy_uncertainty_filename)
policy_uncertainty_data = pd.read_excel(policy_uncertainty_file_path)

# Filter for the years 2020, 2021, and 2022
epu_recent_years = policy_uncertainty_data[policy_uncertainty_data['year'].isin([2020, 2021, 2022])]

# Group by state and year to calculate the mean EPU_C value
epu_composite_mean = (epu_recent_years
                      .groupby(['state', 'year'])['EPU_Composite']
                      .mean()
                      .reset_index())

# Pivot the data
epu_wide_format = epu_composite_mean.pivot(index='state', columns='year', values='EPU_Composite')

# Rename the index and columns to match the requirements
epu_wide_format.index.name = 'State'
epu_wide_format.columns = [f'EPU_C_{year}' for year in epu_wide_format.columns]

# Reset index to make 'State' a column
epu_wide_format.reset_index(inplace=True)

# Display the first few rows of the reshaped DataFrame
print(epu_wide_format.head())



# Question 2.6) Finally, merge this data into your merged data from question 2.3, 
# making sure the merge does what you expect.

# Load the population data
base_directory = "C:/Users/ChelseySSS/Desktop"
population_filename = "NST-EST2022-ALLDATA.csv"
population_file_path = os.path.join(base_directory, population_filename)
population_data = pd.read_csv(population_file_path)

# Convert FIPS codes to state abbreviations and check the unique values
population_data['State_Abbreviation'] = population_data['STATE'].apply(lambda x: us.states.lookup(str(x).zfill(2)).abbr if us.states.lookup(str(x).zfill(2)) else None)
print("Unique state abbreviations in population data:", population_data['State_Abbreviation'].unique())

# Load the visits data and check the unique state values
visits_filename = "state-visits.xlsx"
visits_file_path = os.path.join(base_directory, visits_filename)
visits_data = pd.read_excel(visits_file_path)
print("Unique state identifiers in visits data:", visits_data['STATE'].unique())

# Load the EPU data
policy_uncertainty_filename = "policy_uncertainty.xlsx"
policy_uncertainty_file_path = os.path.join(base_directory, policy_uncertainty_filename)
policy_uncertainty_data = pd.read_excel(policy_uncertainty_file_path)
epu_composite_mean = (policy_uncertainty_data
                      .groupby(['state', 'year'])['EPU_Composite']
                      .mean()
                      .reset_index())
epu_wide_format = epu_composite_mean.pivot(index='state', columns='year', values='EPU_Composite')
epu_wide_format.index.name = 'State'
epu_wide_format.columns = [f'EPU_C_{year}' for year in epu_wide_format.columns]
epu_wide_format.reset_index(inplace=True)
print("Unique state identifiers in EPU data:", epu_wide_format['State'].unique())

# Merge the visits data with the population data
merged_data = population_data.merge(visits_data[['STATE', 'VISITED']],
                                    left_on='State_Abbreviation',
                                    right_on='STATE',
                                    how='inner')

# Remove 'STATE' if it exists after merging
if 'STATE' in merged_data.columns:
    merged_data.drop(columns='STATE', inplace=True)
print("Result of first merge (Population and Visits):", merged_data.head())

# Merge the EPU data with the previously merged population and visits data
final_merged_data = merged_data.merge(epu_wide_format,
                                      left_on='State_Abbreviation',
                                      right_on='State',
                                      how='inner')

# Remove 'State' if it exists after merging
if 'State' in final_merged_data.columns:
    final_merged_data.drop(columns='State', inplace=True)

# Final check
print("Final Merged DataFrame:", final_merged_data.head())
print("Number of rows in final merged DataFrame:", len(final_merged_data))



# Question 2.7: Using groupby on the VISITED column in the dataframe resulting 
# from the previous question, answer the following questions and show how you  
# calculated them: a) what is the single smallest state by 2022 population  
# that you have visited, and not visited?  b) what are the three largest states  
# by 2022 population you have visited, and the three largest states by 2022 
# population you have not visited? c) do states you have visited or states you  
# have not visited have a higher average EPU-C value in 2022?

# a) Smallest state by 2022 population that we have visited, and not visited
smallest_visited = final_merged_data[final_merged_data['VISITED'] == 1].nsmallest(1, 'POPESTIMATE2022')
smallest_not_visited = final_merged_data[final_merged_data['VISITED'] == 0].nsmallest(1, 'POPESTIMATE2022')

print("Smallest state by 2022 population visited:")
print(smallest_visited[['State_Abbreviation', 'POPESTIMATE2022']])

print("Smallest state by 2022 population not visited:")
print(smallest_not_visited[['State_Abbreviation', 'POPESTIMATE2022']])

# b) Three largest states by 2022 population we have visited, and not visited
largest_visited = final_merged_data[final_merged_data['VISITED'] == 1].nlargest(3, 'POPESTIMATE2022')
largest_not_visited = final_merged_data[final_merged_data['VISITED'] == 0].nlargest(3, 'POPESTIMATE2022')

print("Three largest states by 2022 population visited:")
print(largest_visited[['State_Abbreviation', 'POPESTIMATE2022']])

print("Three largest states by 2022 population not visited:")
print(largest_not_visited[['State_Abbreviation', 'POPESTIMATE2022']])

# c) Compare average EPU-C value in 2022 for visited vs. not visited states
average_epu_visited = final_merged_data[final_merged_data['VISITED'] == 1]['EPU_C_2022'].mean()
average_epu_not_visited = final_merged_data[final_merged_data['VISITED'] == 0]['EPU_C_2022'].mean()

print("Average EPU-C value in 2022 for states visited:", average_epu_visited)
print("Average EPU-C value in 2022 for states not visited:", average_epu_not_visited)

# Determine which group has a higher average EPU-C value
if average_epu_visited > average_epu_not_visited:
    print("States visited have a higher average EPU-C value in 2022.")
else:
    print("States not visited have a higher average EPU-C value in 2022.")



# Question 2.8: Transforming data to have mean zero and unit standard deviation
# is often called "standardization", or a "zscore".  The basic formula to 
# apply to any given value is: (value - mean) / std
# Return to the long-form EPU data you created in step 2.4 and then, using groupby
# and a function you write, transform the data so that the values for EPU-C
# have mean zero and unit standard deviation for each state.  Add these values
# to a new column named EPU_C_zscore.

# Load the policy uncertainty data
base_directory = "C:/Users/ChelseySSS/Desktop"
policy_uncertainty_filename = "policy_uncertainty.xlsx"
policy_uncertainty_file_path = os.path.join(base_directory, policy_uncertainty_filename)
policy_uncertainty_data = pd.read_excel(policy_uncertainty_file_path)

# Calculate the mean EPU_Composite value for each state/year
epu_composite_mean = (policy_uncertainty_data
                      .groupby(['state', 'year'])['EPU_Composite']
                      .mean()
                      .reset_index())

# Rename the columns for consistency 
epu_composite_mean.columns = ['State', 'Year', 'EPU_Composite']

# Define a function to standardize data to have mean zero and unit standard deviation
def standardize(data):
    return (data - data.mean()) / data.std()

# Apply the standardize function to the EPU_Composite values grouped by State
epu_composite_mean['EPU_C_zscore'] = epu_composite_mean.groupby('State')['EPU_Composite'].transform(standardize)

# Display the first few rows of the resulting DataFrame with the new column
print(epu_composite_mean.head())






