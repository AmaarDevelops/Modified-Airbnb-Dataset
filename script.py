import pandas as pd
import numpy as np
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'AB_NYC_2019.csv')
df = pd.read_csv(file_path,encoding='latin1')




null_values = df.isnull().sum()

first_10_rows = df.head(10)
dataset_info = df.info()

df.dropna(axis=0,how='any',inplace=True)

duplicates = df.drop_duplicates()

df['last_review'] = pd.to_datetime(df['last_review']) 

df['price_per_minimum_night'] = df['price'] / df['minimum_nights']

total_listings = df['calculated_host_listings_count'].count()

listings_counts_by_room_type = df.groupby('room_type')['calculated_host_listings_count'].value_counts()

listings_counts_by_neighbourhood_group = df.groupby('neighbourhood_group')['calculated_host_listings_count'].value_counts()

listing_counts_by_neighbourhood_top_10 = df.groupby('neighbourhood')['calculated_host_listings_count'].head(10).value_counts()

average_price_in_each_room_type = df.groupby('room_type')['price'].mean()

minimum_price = df['price'].min()
maximum_price = df['price'].max()

availabilty_365 = df['availability_365'].count()
average_number_of_reviews_per_neighbourhood = df.groupby('neighbourhood')['number_of_reviews'].mean()

neighbour_hoods_average_price = df.groupby('neighbourhood')['price'].mean()

top_10_expensive_neighbourhoods_price = neighbour_hoods_average_price.sort_values(ascending=False).head(10)
cheapest_10_neighbourhoods_prices = neighbour_hoods_average_price.sort_values(ascending=True).head(10)

average_price_per_neighbourhood_group = df.groupby('neighbourhood_group')['price'].mean()

listings_greater_than_price_500_in_bronx = df[(df['neighbourhood_group'] == 'Bronx') & (df['price'] > 500)].value_counts().sum()

listings_that_have_never_been_reviewed = df[df['number_of_reviews'] == 0].shape[0]

top_10_listings_with_highest_number_of_reviews = df['number_of_reviews'].sort_values(ascending=False).head(10)

average_reviews_per_month_by_neighbourhood_group = df.groupby('neighbourhood_group')['number_of_reviews'].mean()


most_recent_review_data_30 = df['last_review'].max() 
thirtydays_ago  = most_recent_review_data_30 - pd.Timedelta(days=30)

listings_with_reviews_in_last_30_days = df[df['last_review'] > thirtydays_ago]


hosts_with_most_listings = df.groupby('host_name').size()
top_5_hosts_with_most_listings = hosts_with_most_listings.sort_values(ascending=False).head(5)


hosts_more_than_10_listings = df[df['calculated_host_listings_count'] > 10]['host_name'].value_counts().sum()

average_price = df['price'].mean()

df['is_expensive']  = np.where(df['price'] > average_price, "YES","No")

df['revenue'] = df['price'] * df['availability_365']

for_each_host_total_revenue = df.groupby('host_name')['revenue'].sum()

for_each_neighbourhood_revenue = df.groupby('neighbourhood')['revenue'].sum().sort_values(ascending=False)
neighbour_hood_with_highest_revenue = for_each_neighbourhood_revenue.index[0]


high_reviews = df['number_of_reviews'].quantile(0.75)
low_price = df['price'].quantile(0.25)
high_availability = df['availability_365'].quantile(0.75)

ideal_listings = df[(df['number_of_reviews'] > high_reviews) & 
                    (df['price'] < low_price) &
                    (df['availability_365'] > high_availability)]

suspicious_listings = df[(df['availability_365'] == 0) & (df['number_of_reviews'] == 0) & (df['price'] > 1000)]

df['number_of_reviews'] = df['number_of_reviews'].fillna(0)
df['price'] = df['price'].replace(0,np.nan)
df.dropna(subset=['price'],inplace=True)

bins = [-0.01,1,5,1000]
labels = ["Low",'medium','High']


df['reviews_per_month'] = pd.cut(df['number_of_reviews'], bins=bins,labels=labels)

df['score'] =  df['number_of_reviews'] / df['price']

highest_score_index = df['score'].idxmax()

listing_with_highest_score = df.loc[highest_score_index]

df.to_csv('Cleaned_airbnb.csv',index=False)

print("Null Values:-",null_values)
print("First 10 rows :-",first_10_rows)
print('dataset info:-',dataset_info)
print("Duplicates Remove:-",duplicates)
print('Total Listings:-',total_listings)
print("Listing Counts by room type:-",listings_counts_by_room_type)
print("Listing counts by neighbourhood groups:-",listings_counts_by_neighbourhood_group)
print("Listings counts by neighbourhood top 10:-",listing_counts_by_neighbourhood_top_10)
print("Average price in each room type:-",average_price_in_each_room_type)
print("Availability 365:-",availabilty_365)
print("Minimum Price:-",minimum_price)
print('Maximum Price :-',maximum_price)
print('Average number of reviews per neighbourhood:-',average_number_of_reviews_per_neighbourhood)
print('Top 10 most expensive neighbourhoods:-',top_10_expensive_neighbourhoods_price)
print("Cheapest 10 neighbourhoods price:-",cheapest_10_neighbourhoods_prices)
print("Average price per neighbourhood group:-",average_price_per_neighbourhood_group)
print('Listings greater than price 500 in bronx:-',listings_greater_than_price_500_in_bronx)
print("Listing that were never reviewd:-",listings_that_have_never_been_reviewed)
print("Top 10 highest number of listings:-",top_10_listings_with_highest_number_of_reviews)
print("Average reviews per month by neighbourhood group:-",average_reviews_per_month_by_neighbourhood_group)
print('Listings with reviews in last 30 days:-',listings_with_reviews_in_last_30_days)
print("Top 5 hosts with most listings count:-",top_5_hosts_with_most_listings)
print("Count of how many hosts have more than 10 listings:-",hosts_more_than_10_listings)
print("For each host revenue count:-",for_each_host_total_revenue)
print("For each neighbourhood revenue count:-",for_each_neighbourhood_revenue)
print("Neighbourhood with highest revenue:-",neighbour_hood_with_highest_revenue)
print("Ideal Listings:-",ideal_listings)
print("Number of ideal listings:-",len(ideal_listings))
print("Suspicipious Listings:-",suspicious_listings)
print("Number of suspicious listings:-",len(suspicious_listings))

print("Highest score lisitng:-",listing_with_highest_score)

print("\n\nFinal:-",df)