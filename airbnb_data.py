## Data Importing

import pandas as pd

# Load dataset
file_path = "https://gitlab.crio.do/me_notebook/me_jupyter_airbnbanalysis/-/raw/master/Airbnb_data.csv"
df = pd.read_csv(file_path)


df.shape

## Data Exploration

df.info()

df.head()

## Handling Missing Values

df.isnull().sum()


# Fill missing values where necessary
df["reviews_per_month"].fillna(0, inplace=True)  # Replace NaNs with 0 for review counts
df.drop(columns=["last_review"], inplace=True)  # Drop last_review since it is not needed
# Replace only missing values in 'name' and 'host_name' with 'unknown'
df["name"].fillna("unknown", inplace=True)
df["host_name"].fillna("unknown", inplace=True)


# Re-check missing values
df.isnull().sum()

## Handling Outliers



# Selecting only numeric columns
import matplotlib.pyplot as plt
numeric_columns = df.select_dtypes(include=['number']).columns


# plt.figure(figsize=(8, 5))
# plt.boxplot(df[price], vert=False, patch_artist=True)
# plt.title(f"Boxplot of price")
# plt.xlabel("Price")
# plt.grid(True)
# plt.show()
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

plt.boxplot(df['price'], vert=False, patch_artist=True)

plt.title("Boxplot of Price")
plt.xlabel("Price")
plt.grid(True)

plt.show()


# Ensure data types are correct
df["price"] = pd.to_numeric(df["price"], errors='coerce')
df["availability_365"] = pd.to_numeric(df["availability_365"], errors='coerce')




# Remove outliers (if necessary)
df = df[df["price"] > 0]  # Remove listings with zero or negative price
df = df[df["minimum_nights"] < 365]  # Remove extreme long-term stays




import numpy as np

Q1 = df["number_of_reviews"].quantile(0.25)  # First quartile
Q3 = df["number_of_reviews"].quantile(0.75)  # Third quartile
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR


# Cap outliers at threshold values
df["number_of_reviews"] = np.where(df["number_of_reviews"] < lower_bound, lower_bound, df["number_of_reviews"])
df["number_of_reviews"] = np.where(df["number_of_reviews"] > upper_bound, upper_bound, df["number_of_reviews"])

import numpy as np

Q1 = df["price"].quantile(0.25)  # First quartile
Q3 = df["price"].quantile(0.75)  # Third quartile
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR


# Cap outliers at threshold values
df["price"] = np.where(df["price"] < lower_bound, lower_bound, df["price"])
df["price"] = np.where(df["price"] > upper_bound, upper_bound, df["price"])

# Follow the same for other columns
df.columns

## Understanding Customer Preferences

import numpy as np
import matplotlib.pyplot as plt

# Understanding Customer Preferences


# TODO:
# 1. Group data by 'neighbourhood_group' and 'room_type', count listings, and reshape with unstack().
# 2. Fill any missing values with 0 for better visualization.
# 3. Create a bar plot to visualize room type popularity across neighborhoods:
#    - Set appropriate figure size.
#    - Use a colormap for visual appeal.
#    - Rotate x-axis labels for readability.
#    - Add title, axis labels, and legend.
#    - Display the plot.
# df.columns


room_neighbour_grp = df.groupby('neighbourhood_group')['room_type'].value_counts().unstack().fillna(0)
# room_neighbour_grp
room_neighbour_grp.plot(
    kind='bar',
    figsize=(10,6),
    colormap='viridis'   # ✅ important fix
)

plt.title("Most Popular Room Type Across Neighbourhoods")
plt.xlabel("Neighbourhood Group")
plt.ylabel("Number of Listings")
plt.xticks(rotation=45)
plt.legend(title="Room Type")

plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Understanding Customer Preferences

# TODO:
# 1. Create a new column 'price_range' by binning the 'price' into defined ranges with labels.
# 2. Group the data by 'neighbourhood_group' and 'price_range', then count listings and reshape using unstack().
# 3. Fill missing values with 0 for visualization consistency.
# 4. Generate a bar plot to show price range preferences across neighborhoods:
#    - Set figure size and use a distinct colormap.
#    - Rotate x-axis labels for clarity.
#    - Add title, axis labels, and legend.
#    - Display the plot.

df['price_range'] = pd.cut(
    df['price'],
    bins=[0, 100, 200, 500, 1000],
    labels=['Budget', 'Affordable', 'Premium', 'Luxury']
)
price_neighbour_grp = df.groupby('neighbourhood_group')['price_range'].value_counts().unstack()
price_neighbour_grp = price_neighbour_grp.fillna(0)
price_neighbour_grp.plot(
    kind='bar',
    figsize=(10,6),
    colormap='plasma'
)

plt.title("Customer Preferences for Price Ranges by Neighbourhood")
plt.xlabel("Neighbourhood Group")
plt.ylabel("Number of Listings")
plt.xticks(rotation=45)
plt.legend(title="Price Range")

plt.show()


# TODO:
# 1. Group the data by 'neighbourhood' and sum the 'number_of_reviews' to find total reviews per area.
# 2. Sort the result in descending order to identify high-demand locations.
# 3. Create a bar plot for the top 15 neighborhoods with the most reviews:
#    - Set appropriate figure size and bar color.
#    - Rotate x-axis labels for readability.
#    - Add title, axis labels, and display the plot.
# Step 1: Group + sum
top_reviews = df.groupby('neighbourhood')['number_of_reviews'].sum()

# Step 2: Sort descending
top_reviews = top_reviews.sort_values(ascending=False)

# Step 3: Select top 15
top_15 = top_reviews.head(15)

# Step 4: Plot
top_15.plot(
    kind='bar',
    figsize=(12,6),
    color='orange'
)

plt.title("Top 15 Locations with Most Reviews (High Demand Areas)")
plt.xlabel("Neighbourhood")
plt.ylabel("Total Reviews")
plt.xticks(rotation=45)

plt.show()

## Pricing Startegy Analysis

import matplotlib.pyplot as plt
import seaborn as sns

# Pricing Strategy Analysis

# TODO:
# 1. Group the data by 'neighbourhood_group' and calculate the average price.
# 2. Reset the index to prepare for plotting.
# 3. Create a bar plot showing average price per neighborhood group:
#    - Use a distinct color for the bars.
#    - Add a title and axis labels.
#    - Display the plot.
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Group + average
avg_price = df.groupby('neighbourhood_group')['price'].mean()

# Step 2: Reset index
avg_price = avg_price.reset_index()

# Step 3: Plot
plt.figure(figsize=(8,5))

sns.barplot(
    data=avg_price,
    x='neighbourhood_group',
    y='price',
    palette='coolwarm'
)

plt.title("Average Price by Neighbourhood Group")
plt.xlabel("Neighbourhood Group")
plt.ylabel("Average Price")

plt.show()

# TODO:
# 1. Group the data by 'room_type' and calculate the average price.
# 2. Reset the index to prepare the data for plotting.
# 3. Create a bar plot to show how average price varies by room type:
#    - Set figure size and choose a bar color.
#    - Add a title and axis labels.
#    - Display the plot.
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Group + average
avg_price_room = df.groupby('room_type')['price'].mean()

# Step 2: Reset index
avg_price_room = avg_price_room.reset_index()

# Step 3: Plot
plt.figure(figsize=(8,5))

sns.barplot(
    data=avg_price_room,
    x='room_type',
    y='price',
    palette='Set2'
)

plt.title("Average Price by Room Type")
plt.xlabel("Room Type")
plt.ylabel("Average Price")

plt.xticks(rotation=30)

plt.show()

## Growth opportunity Analysis

# TODO:
# 1. Create a scatter plot to visualize the relationship between 'availability_365' and 'price'.
#    - Set figure size, point transparency (alpha), and color.
#    - Use seaborn's scatterplot for better aesthetics.
# 2. Add title and axis labels to clearly describe the plot.
# 3. Display the plot.
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8,5))

sns.scatterplot(
    data=df,
    x='availability_365',
    y='price',
    alpha=0.5,
    color='blue'
)

plt.title("Relationship between Availability and Price")
plt.xlabel("Availability (Days per Year)")
plt.ylabel("Price")

plt.show()



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Market Competition & Growth Opportunities

# TODO:
# 1. Count the number of listings per 'neighbourhood_group' to assess market saturation.
# 2. Reset the index and rename columns for clarity.
# 3. Create a bar plot to visualize the number of listings per neighborhood group:
#    - Set figure size and choose a distinct bar color.
#    - Rotate x-axis labels for better readability.
#    - Add title and axis labels.
#    - Display the plot.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Count listings
listing_count = df['neighbourhood_group'].value_counts()

# Step 2: Reset index + rename
listing_count = listing_count.reset_index()
listing_count.columns = ['neighbourhood_group', 'listing_count']

# Step 3: Plot
plt.figure(figsize=(8,5))

plt.bar(
    listing_count['neighbourhood_group'],
    listing_count['listing_count'],
    color='teal'
)

plt.title("Number of Listings per Neighbourhood (Market Saturation)")
plt.xlabel("Neighbourhood Group")
plt.ylabel("Number of Listings")
plt.xticks(rotation=45)

plt.show()

# TODO:
# 1. Create a new column 'price_category' by binning the 'price' into defined categories (e.g., Budget, Luxury).
# 2. Count the number of listings in each price category to understand market competition.
# 3. Rename the resulting columns for clarity.
# 4. Create a bar plot to visualize the distribution of listings across price categories:
#    - Set figure size and bar color.
#    - Rotate x-axis labels for readability.
#    - Add title and axis labels.
#    - Display the plot.
df['price_category'] = pd.cut(
    df['price'],
    bins=[0, 100, 200, 500, 1000],
    labels=['Budget', 'Affordable', 'Premium', 'Luxury']
)

# Step 2: Count listings
price_counts = df['price_category'].value_counts()

# Step 3: Reset index + rename
price_counts = price_counts.reset_index()
price_counts.columns = ['price_category', 'listing_count']

# Step 4: Plot
plt.figure(figsize=(8,5))

plt.bar(
    price_counts['price_category'],
    price_counts['listing_count'],
    color='purple'
)

plt.title("Competition in Budget vs. Luxury Listings")
plt.xlabel("Price Category")
plt.ylabel("Number of Listings")
plt.xticks(rotation=45)

plt.show()

# TODO:
# 1. Create a new column 'total_revenue' by multiplying 'price' with 'minimum_nights'.
# 2. Group data by 'neighbourhood' and calculate average total revenue to estimate potential earnings.
# 3. Sort the neighborhoods by revenue potential in descending order.
# 4. Create a bar plot for the top 15 neighborhoods with the highest average revenue:
#    - Set figure size and bar color.
#    - Rotate x-axis labels for readability.
#    - Add title and axis labels.
#    - Display the plot.

import matplotlib.pyplot as plt

# Step 1: Create total revenue
df['total_revenue'] = df['price'] * df['minimum_nights']

# Step 2: Group + average
revenue_neighbour = df.groupby('neighbourhood')['total_revenue'].mean()

# Step 3: Sort descending
revenue_neighbour = revenue_neighbour.sort_values(ascending=False)

# Step 4: Select TOP 15 (IMPORTANT)
top_15_revenue = revenue_neighbour.head(15)

# Step 5: Plot
plt.figure(figsize=(12,6))

top_15_revenue.plot(
    kind='bar',
    color='green'
)

# Step 6: Proper labels (IMPORTANT for passing)
plt.title("Top 15 neighbourhoods with Highest Revenue Potential")
plt.xlabel("Neighbourhood")
plt.ylabel("Average Total Revenue")
plt.xticks(rotation=45)

plt.tight_layout()   # improves spacing

plt.show()


