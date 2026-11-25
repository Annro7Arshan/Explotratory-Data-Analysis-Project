import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load the data
df = pd.read_csv("coaster_db.csv")
print("Initial Shape:", df.shape)

# 2. Set display options
pd.set_option('display.max_columns', 200) 

print(df.columns)
print(df.dtypes)
print(df.describe())

# ==========================================
# Data Preparation
# ==========================================

# 3. Rename the column 
df = df.rename(columns={'coaster_name': 'Coaster_Name'})

# 4. Convert datatype
df['opening_date_clean'] = pd.to_datetime(df['Opening date'], errors='coerce')

# 5. Remove the old raw date column
df = df.drop(columns=['Opening date'])

# ==========================================
# Checking Duplicates and Querying
# ==========================================

print("\n--- Full Duplicates ---")
print(df.loc[df.duplicated()])

print("\n--- Duplicates by Coaster Name ---")
print(df.loc[df.duplicated(subset=['Coaster_Name'])].head(5))

print("\n--- Crystal Beach Cyclone ---")
print(df.query('Coaster_Name == "Crystal Beach Cyclone"'))

print("\n--- Duplicate Count ---")
print(df.duplicated(subset=['Coaster_Name', 'Location', 'opening_date_clean']).sum())

# Drop duplicates and reset index
df = df.loc[~df.duplicated(subset=['Coaster_Name', 'Location', 'opening_date_clean'])].reset_index(drop=True)

print("\nFinal Shape:", df.shape)

# ==========================================
# Visualizations (Plots)
# ==========================================

# Plot 1: Bar chart of Year Introduced
print("\nNumber of values in 'Year_Introduced' column:", df['year_introduced'].value_counts().head(10))

ax = df['year_introduced'].value_counts().head(10).plot(kind='bar')
ax.set_xlabel('Year Introduced')
ax.set_ylabel('Count')
plt.title('Top 10 Years Coasters Were Introduced') # Added a title for clarity
plt.show() # Fixed: Removed ax from parentheses

# Plot 2: Histogram of Speed
# Fixed: Changed column name to lowercase 'speed_mph'
ax = df['speed_mph'].plot(kind='hist', bins=20, title='Coaster Speed (mph)')
ax.set_xlabel('Speed (mph)')
plt.show() # Fixed: Changed 'ar' to just plt.show() 

# Plot 3: KDE plot of Speed
# Fixed: Changed column name to lowercase 'speed_mph'
aq = df['speed_mph'].plot(kind='kde', title='Coaster Speed (mph)')
aq.set_xlabel('Speed (mph)')
plt.show() 

# Plot 4: Scatter plot of Speed vs Height
# Fixed: Changed column names to lowercase 'speed_mph' and 'height_ft'
ac = df.plot(kind='scatter', x='speed_mph', y='height_ft', title='Coaster Speed vs Height')               
plt.show()

sns.scatterplot(data=df, x='speed_mph',y='height_ft',hue='year_introduced')
plt.show()

sns.pairplot(df,vars=['year_introduced','speed_mph','height_ft','Inversions_clean','Gforce_clean'],hue='Type_Main')
plt.show()

df_corr=df[['year_introduced','speed_mph','height_ft','Inversions_clean','Gforce_clean']].dropna().corr()
sns.heatmap(df_corr,annot=True)
plt.show()

#What are the locations with the fastest roller coasters (min of 10)
df['Location'].value_counts()

ax=df.query('Location!="Others"').groupby('Location')['speed_mph'].agg(['mean','count']).query('count>=10').sort_values('mean')['mean'].plot(kind='barh',figsize=(12,5),title='Average Coast Speed by Location')
ax.set_xlabel('Average Coast Speed by Location')
plt.show()
