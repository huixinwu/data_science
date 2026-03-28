"""
module 1: capstone introduction and understading the dataset
Hands-on Lab: Data Wrangling
"""
import piplite, requests
await piplite.install(['numpy'])
await piplite.install(['pandas'])

# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

# Data Analysis
from js import fetch
import io

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv'
resp = await fetch(URL)
dataset_part_1_csv = io.BytesIO((await resp.arrayBuffer()).to_py())

#Load Space X dataset, from last section.
df=pd.read_csv(dataset_part_1_csv)
df.head(10)

# Identify and calculate the percentage of the missing values in each attribute

df.isnull().sum()/df.shape[0]*100

#
df.dtypes

# TASK 1: Calculate the number of launches on each site
# Apply value_counts() on column LaunchSite
df['LaunchSite'].value_counts()

#TASK 2: Calculate the number and occurrence of each orbit
# Apply value_counts on Orbit column
df['Orbit'].value_counts()

#TASK 3: Calculate the number and occurence of mission outcome of the orbits
# landing_outcomes = values on Outcome column
landing_outcomes = df['Outcome'].value_counts()
print(landing_outcomes)

# TASK 4: Create a landing outcome label from Outcome column
df['Class']=landing_class
df[['Class']].head(8)
print(df.head(5))
print(df["Class"].mean())




