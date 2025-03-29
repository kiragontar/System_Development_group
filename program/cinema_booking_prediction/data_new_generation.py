import pandas as pd
import numpy as np
from faker import Faker
import random
import datetime

random.seed(42)  # Set random seed for reproducity
np.random.seed(42)
fake = Faker()
def generate_film_data(num_films):
    films = []
    all_genres = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Thriller', 'Romance', 'Adventure', 'Horror', 'Mystery']
    for film_id in range(1, num_films + 1):
        num_genres = random.randint(1,3) # Randomly select 1 to 3 genres per film.
        film_genres = random.sample(all_genres, num_genres)
        films.append({
            'film_id': film_id,
            'genre': film_genres,
            'release_date': fake.date_between(start_date='-10y', end_date='today'),
            'rating': round(random.uniform(1, 10), 1) # Generates float number between 1 and 10, round its to 1 decimal place.
        })
    return pd.DataFrame(films) # makes each film a row.

films_df = generate_film_data(20) #generate 20 films.

num_rows = 5000

cities_population = { # 2025 Population
    'Birmingham': 2704620,
    'Bristol': 720052,
    'Cardiff': 495378,
    'London': 9840740
}

def generate_cinema_data(cities_population):
    cinema_data = [] # Add cinema data.
    cinema_id_counter = 1 
    for city, population in cities_population.items():
        # Generate number of cinemas based on population
        num_cinemas = int(population / 1000000) + random.randint(1, 3) # adds some randomness to number  of cinemas in different cities.
        num_cinemas = max(2, num_cinemas) #ensure minimum is 2.
        for _ in range(num_cinemas):
            cinema_data.append({'cinema_id': cinema_id_counter, 'cinema_location': city})
            cinema_id_counter += 1
    return pd.DataFrame(cinema_data)

cinema_df = generate_cinema_data(cities_population)

screen_data = [] # To store screens
screen_id_counter = 1
for cinema_id in cinema_df['cinema_id']:
    num_screens = random.randint(1, 6) # Create randomly between 1 to 6 screens per cinema.
    for _ in range(num_screens):
        num_seats = random.randint(50, 120) # Create randomly between 50 and 120 seats per screen.
        screen_data.append({
            'screen_id': screen_id_counter,
            'cinema_id': cinema_id,
            'capacity': num_seats
        })
        screen_id_counter += 1
screen_df = pd.DataFrame(screen_data)


showing_data = [] # Store each screening.
for _ in range(num_rows):
    screen_id = random.choice(screen_df['screen_id']) # Picks a random screen.
    cinema_id = screen_df[screen_df['screen_id'] == screen_id]['cinema_id'].values[0] # Gets cinema corresponding to chosen screen. so filters to find the screenid in the screen df, then accesses the cinema_id column and gets its value.
    city = cinema_df[cinema_df['cinema_id'] == cinema_id]['cinema_location'].values[0] # Gets city corresponding to cinema.
    film_row = films_df.sample(1).iloc[0] # Randomly selects 1 row from the films_df , illoc[0] extracts the first row.
    film_id = film_row['film_id']
    genres = film_row['genre']
    release_date = film_row['release_date']
    rating = film_row['rating']
    date = datetime.date.today() + datetime.timedelta(days=random.randint(-365, 365))
    show_time_category = random.choice(['Morning', 'Afternoon', 'Evening'])
    capacity = screen_df[screen_df['screen_id'] == screen_id]['capacity'].values[0]

    lower_hall_count = int(capacity * 0.3) # 30 % of total seats
    vip_count = 10 # 10 vip seats always
    upper_hall_count = capacity - lower_hall_count - vip_count # Calculates upper hall seats.
    seats = ['Lower'] * lower_hall_count + ['Upper'] * upper_hall_count + ['VIP'] * vip_count # create the seats.
    seat_type = random.choice(seats) # Randomly select seat types.

    lower_hall_price = {
        'Birmingham': [500, 600, 700], # $5, $6, $7
        'Bristol': [600, 700, 800], # $6, $7, $8
        'Cardiff': [500, 600, 700],
        'London': [1000, 1100, 1200]
    }[city][['Morning', 'Afternoon', 'Evening'].index(show_time_category)] # .index returns either 0 1 or 2, we can then decide what price to retrieve.

    ticket_price = lower_hall_price
    if seat_type == 'Upper':
        ticket_price = int(lower_hall_price * 1.2)
    elif seat_type == 'VIP':
        ticket_price = int(lower_hall_price * 1.2 * 1.2)

    # Genre Influence
    genre_popularity = { # The weight of each genre.
        'Action': 1.2,
        'Sci-Fi': 1.1,
        'Comedy': 1.05,
        'Drama': 0.95,
        'Thriller': 1.0,
        'Romance': 0.9,
        'Adventure': 1.1,
        'Horror': 1.0,
        'Mystery': 0.95
    }
    genre_multipliers = [genre_popularity[g] for g in genres]
    genre_multiplier = sum(genre_multipliers) / len(genre_multipliers) # Calculates average genre multiplier.

    # Time Since Release, decay weight the longer it has been released.
    days_since_release = (date - release_date).days 
    release_decay = max(0.5, 1 - (days_since_release / 180)) # create a value that decreases as days_since_release increases. Simulates a linear decay over 180 days. Ensures release_decay is never less than 0.5 so film doesnt lose its influence.

    tickets_sold = int(
        min(rating * 5, 50) + # Higher ratings tend to sell more.
        (capacity * 0.007) - # Simulate that only a fraction of the cinema seats are sold as its rare for all seats to be sold.
        (ticket_price / 200) + # Higher ticket prices result in fewer tickets sold, so a - is done. Also its divided by 100 to reduce its magnitude so that its in the range of the other factors.
        (40 if date.weekday() >= 5 else 0) + # Weekends are more popular so more tickets are sold on weekends, so adds 40 tickets sold.
        (50 if show_time_category == 'Evening' else 0) + # Evening shows are more popular so more tickets are sold in the evening, adds 50 tickets.
        (60 if date.month in [12, 1, 7, 8] else 0) + # December, January, July, August are popular months so more tickets are sold in these months, adds 60 tickets.
        min(genre_multiplier * 10, 30)+ # Genre of movie plays a huge role in number of tickets as preference.
        (release_decay * 30)+ # days since release plays a huge role as many people may have already seen the movie.
        np.random.normal(0, 20) # Add some random noise to the tickets sold to make it more realistic.
    )
    print(f"Calculated tickets_sold before min/max: {tickets_sold}")
    tickets_sold = max(0, min(tickets_sold, capacity)) # Ensures ticket sold is not higher than capacity as it would not make sense otherwise.
    print(f"Calculated tickets_sold after min/max: {tickets_sold}")
    showing_data.append({
            'screen_id': screen_id,
            'cinema_id': cinema_id,
            'cinema_location': city,
            'film_id': film_id,
            'date': date,
            'show_time_category': show_time_category,
            'capacity': capacity,
            'seat_type': seat_type,
            'ticket_price': ticket_price,
            'tickets_sold': tickets_sold
        })
        
showing_df = pd.DataFrame(showing_data)

final_df = pd.merge(showing_df, films_df, on='film_id', how='left') # Combines the film df and showing df based on film_id with a left join.

final_df = pd.get_dummies(final_df, columns=['cinema_location', 'seat_type', 'show_time_category']) # Performs one hot encoding on the string types.
genre_dummies = pd.get_dummies(final_df['genre'].apply(pd.Series).stack()).groupby(level=0).sum() # One hot encodes the genre strings. Converts each genre into a panda series, creating a df where each genre is in a seperate column.
final_df = pd.concat([final_df, genre_dummies], axis=1).drop('genre', axis=1) # removes the original genre column.

final_df.to_csv('program/cinema_booking_prediction/cinema_data_booking_prediction_essential.csv', index=False)
