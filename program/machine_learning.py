import pandas as pd
import numpy as np
from faker import Faker
import random
import datetime

fake = Faker() # create faker object for creating fake data.
num_rows = 5000 # number of different cinema location rows to generate

cities = ['Birmingham', 'Bristol', 'Cardiff', 'London']
cinema_location = np.random.choice(cities, num_rows, p=[0.2, 0.2, 0.2, 0.4]) # generate random cinema locations, so probability of Birmingham being selected is 0.2, etc.
total_capacity = np.random.randint(50, 121, num_rows) # generate random cinema seat capacities between 50 and 120.
film_popularity = np.random.choice([1, 2, 3, 4, 5], num_rows, p=[0.2, 0.2, 0.3, 0.2, 0.1]) # 1,2,3,4,5 is popularity level so 1 is very low popularity and 5 is very high popularity. it generates 5000 random popularity values, with the corresponding probabilities.
show_time = np.random.choice([1, 2, 3], num_rows, p=[0.2, 0.3, 0.5]) # 1,2,3 is show time so 1 is morning, 2 is afternoon, 3 is evening. it generates 5000 random show time values, with the corresponding probabilities
dates = [fake.date_between(start_date='-2y', end_date='today') for _ in range(num_rows)] # generate random dates between 2 years ago and today and stores the 5000 dates in a list.
# Seat types (Lower Class = 30%, Upper Class, VIP)
seat_types = ['Lower Class', 'Upper Class', 'VIP']

data = {
    'film_code': [random.randint(1000, 2000) for _ in range(num_rows)], # generate random film codes between 1000 and 2000. There will be repeating values to represent real-world data.
    'cinema_code': [random.randint(100, 500) for _ in range(num_rows)], # generate random cinema codes between 100 and 500.
    'film_popularity': film_popularity,
    'cinema_location': cinema_location,
    'show_time': show_time,
    'date': dates,
    'capacity': total_capacity,
}

df = pd.DataFrame(data) # create a pandas dataframe from the data dictionary.

def generate_seat_type(capacity):
    lower_hall_count = int(capacity * 0.3)
    vip_count = 10
    upper_hall_count = capacity - lower_hall_count - vip_count

    seats = ['Lower Hall'] * lower_hall_count + ['Upper Hall'] * upper_hall_count + ['VIP'] * vip_count # create a list of seats with the correct proportions.
    return random.choice(seats) # randomly select a seat type from the list.

df['seat_type'] = df['capacity'].apply(generate_seat_type) # apply the generate_seat_type function to each row in the dataframe to get the seat type.

df['date'] = pd.to_datetime(df['date']) # convert the date column to a datetime object.
df['day'] = df['date'].dt.day # get the day from the date column.
df['day_of_week'] = df['date'].dt.dayofweek # get the day of the week from the date column.
df['month'] = df['date'].dt.month # get the month from the date column.
df['year'] = df['date'].dt.year # get the year from the date column.

def get_ticket_price(city, show_time, seat_type):
    lower_hall_price = 0
    if city == 'Birmingham':
        if show_time == 1:
            lower_hall_price = 500 # £5 for morning show in Birmingham
        elif show_time == 2:
            lower_hall_price = 600 # £6 for afternoon show in Birmingham
        else:
            lower_hall_price = 700 # £7 for evening show in Birmingham
    elif city == 'Bristol':
        if show_time == 1:
            lower_hall_price = 600 # £6 
        elif show_time == 2:
            lower_hall_price = 700 # £7
        else:
            lower_hall_price = 800 # £8
    elif city == 'Cardiff':
        if show_time == 1:
            lower_hall_price = 500 # £5
        elif show_time == 2:
            lower_hall_price = 600 # £6
        else:
            lower_hall_price = 700 # £7
    else:
        if show_time == 1:
            lower_hall_price = 1000 # £10
        elif show_time == 2:
            lower_hall_price = 1100 # £11
        else:
            lower_hall_price = 1200 # £12

    if seat_type == 'Lower Hall':
        return lower_hall_price
    elif seat_type == 'Upper Hall':
        return int(lower_hall_price * 1.2) # 20% more expensive than lower hall
    else:
        return int(lower_hall_price * 1.2 * 1.2) # 20% more expensive than upper hall

df['ticket_price'] = df.apply(lambda row: get_ticket_price(row['cinema_location'], row['show_time'], row['seat_type']), axis=1) # apply the get_ticket_price function to each row in the dataframe to get the ticket price.

df['tickets_sold'] = ( # generate the number of tickets sold based on the following formula
    (df['film_popularity'] * 20) + # scale the popularity by 20 because the popularity is a strong factor on tickets sold.
    (df['capacity'] * 0.1) - # Simulate that only a fraction of the cinema seats are sold as its rare for all seats to be sold.
    (df['ticket_price'] / 100) + # Higher ticket prices result in fewer tickets sold, so a - is done. Also its divided by 100 to reduce its magnitude so that its in the range of the other factors.
    (df['day_of_week'].apply(lambda x: 30 if x >= 5 else 0)) + # Weekends are more popular so more tickets are sold on weekends, adds 30 to the tickets sold if its a weekend.
    (df['show_time'].apply(lambda x: 40 if x == 3 else 0)) + # Evening shows are more popular so more tickets are sold in the evening, adds 40 to the tickets sold if its an evening show.
    (df['month'].apply(lambda x: 50 if x in [12, 1, 7, 8] else 0)) + # December, January, July, August are popular months so more tickets are sold in these months, adds 50 to the tickets sold if its one of these months.
    np.random.normal(0, 30, num_rows) # Add some random noise to the tickets sold to make it more realistic.
).astype(int)  # convert the tickets sold to an integer.

df['tickets_sold'] = df['tickets_sold'].apply(lambda x: max(0, x)) # ensure that the tickets sold is at least 0. as noise can result in negative values.

df.to_csv('cinema_data_booking_prediction_essential.csv', index=False) # save the dataframe to a csv file so we can train the model on it.
