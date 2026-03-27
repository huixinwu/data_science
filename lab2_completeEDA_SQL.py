import pandas as pd
import sqlite3

# Step 1: Connect to SQLite database
con = sqlite3.connect("my_data1.db")

# Step 2: Load SpaceX CSV into a pandas DataFrame
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
df = pd.read_csv(url)

# Step 3: Save the original table into SQLite
df.to_sql("SPACEXTBL", con, if_exists="replace", index=False)

# Step 4: Remove rows where Date is null
df_clean = df[df["Date"].notna()]

# Step 5: Save the cleaned table into SQLite
df_clean.to_sql("SPACEXTABLE", con, if_exists="replace", index=False)

# Step 6: Optional - Check the first 5 rows
df_check = pd.read_sql_query("SELECT * FROM SPACEXTABLE LIMIT 5", con)
print(df_check)

# task 1: Display the names of the unique launch sites in the space mission
# Get unique launch sites
unique_sites = df_clean["Launch_Site"].unique()

# Display them
print("Unique Launch Sites:")
for site in unique_sites:
    print(site)

# task 2: Display 5 records where launch sites begin with the string 'KSC'
# Filter rows where Launch_Site starts with 'KSC' and take first 5 records
df_ksc = df_clean[df_clean["Launch_Site"].str.startswith("KSC")].head(5)

# Display the results
print(df_ksc)

# task 3:Display the total payload mass carried by boosters launched by NASA (CRS)
# Filter rows where Customer is 'NASA (CRS)'
df_nasa = df_clean[df_clean["Customer"] == "NASA (CRS)"]

# Calculate total payload mass
total_payload = df_nasa["PAYLOAD_MASS__KG_"].sum()

print("Total payload mass carried by boosters launched by NASA (CRS):", total_payload, "kg")

# task 4: Display average payload mass carried by booster version F9 v1.1
# Filter rows where Booster_Version is 'F9 v1.1'
df_f9v11 = df[df["Booster_Version"] == "F9 v1.1"]

# Calculate average payload mass
average_payload = df_f9v11["PAYLOAD_MASS__KG_"].mean()

print("Average payload mass carried by booster version F9 v1.1:", average_payload, "kg")

#task 5
# Filter rows where landing was successful and on a drone ship
# Assuming 'Landing_Outcome' contains 'Success' and 'Drone Ship'
df_success_drone = df[df["Landing_Outcome"].str.contains("Success") & df["Landing_Outcome"].str.contains("drone ship")]

# Get the earliest date
earliest_date = df_success_drone["Date"].min()

print(f"Earliest date with successful landing on a drone ship: {earliest_date}")

#task 6
# Filter rows where landing was successful on ground pad
df_ground_success = df[df["Landing_Outcome"].str.contains("Success") & df["Landing_Outcome"].str.contains("ground")]

# Further filter for payload mass between 4000 and 6000 kg
df_filtered = df_ground_success[(df_ground_success["PAYLOAD_MASS__KG_"] > 4000) & (df_ground_success["PAYLOAD_MASS__KG_"] < 6000)]

# Select unique booster names
boosters = df_filtered["Booster_Version"].unique()

# Display results
print("Boosters with successful ground pad landing and payload mass between 4000 and 6000 kg:")
for booster in boosters:
    print(booster)

# task 7
# Count the number of successful and failed missions
# Using 'Class' column if it exists (1 = success, 0 = failure)
print("TASK 7")
if "Class" in df.columns:
    mission_counts = df["Class"].value_counts()
    print("Mission outcomes (1=success, 0=failure):")
    print(mission_counts)
else:
    # Alternatively, use 'Mission_Outcome' or 'Landing_Outcome' if Class doesn't exist
    mission_counts = df["Mission_Outcome"].value_counts()
    print("Mission outcomes:")
    print(mission_counts)

# TASK 8
# Step 1: Find the maximum payload mass (like a subquery)
max_payload = df["PAYLOAD_MASS__KG_"].max()

# Step 2: Filter rows where payload mass equals the maximum
df_max_payload = df[df["PAYLOAD_MASS__KG_"] == max_payload]

# Step 3: Get unique booster versions
boosters_max_payload = df_max_payload["Booster_Version"].unique()

# Display results
print("Booster versions that carried the maximum payload mass ({} kg):".format(max_payload))
for booster in boosters_max_payload:
    print(booster)

# TASK 9
print("TASK 9")
# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Filter for year 2017
df_2017 = df[df["Date"].dt.year == 2017]

# Filter for successful landing outcomes on ground pad
df_success_ground = df_2017[df_2017["Landing_Outcome"].str.contains("Success") & df_2017["Landing_Outcome"].str.contains("ground")]

# Create a Month column with month names
df_success_ground["Month"] = df_success_ground["Date"].dt.month_name()

# Select desired columns
df_result = df_success_ground[["Month", "Landing_Outcome", "Booster_Version", "Launch_Site"]]

# Display results
print(df_result)

# TAKS 10
print("TASK 10")
# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Filter rows between 2010-06-04 and 2017-03-20
start_date = "2010-06-04"
end_date = "2017-03-20"
df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

# Count occurrences of each Landing_Outcome
landing_counts = df_filtered["Landing_Outcome"].value_counts()

# Convert to DataFrame for better display
df_landing_counts = landing_counts.reset_index()
df_landing_counts.columns = ["Landing_Outcome", "Count"]

# Display results in descending order
df_landing_counts = df_landing_counts.sort_values(by="Count", ascending=False)

print(df_landing_counts)

# Step 7: Close the database connection
con.close()