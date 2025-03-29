import pandas as pd
import numpy as np
import joblib  # For loading the 
from datetime import datetime

def datetime_to_excel(datetime_obj):
    """Converts datetime object to Excel serial date."""
    origin = datetime(1900, 1, 1)
    return (datetime_obj - origin).days + 2

def predict_tickets_sold(input_data):
    """
    Predicts the number of tickets sold using the saved Gradient Boosting model.

    Args:
        input_data (dict): A dictionary containing the input features.

    Returns:
        float: The predicted number of tickets sold.
    """

    # Load the saved model
    model = joblib.load('program/cinema_booking_prediction/gradient_boosting_model.joblib')

    # Convert the input dictionary to a DataFrame
    input_df = pd.DataFrame([input_data])

    # Convert release_date and date from string to Excel serial number
    input_df['release_date'] = pd.to_datetime(input_df['release_date']).apply(datetime_to_excel)
    input_df['date'] = pd.to_datetime(input_df['date']).apply(datetime_to_excel)

    # Convert boolean columns to 0/1
    boolean_cols = input_df.select_dtypes(include='bool').columns
    input_df[boolean_cols] = input_df[boolean_cols].astype(int)

    # Remove duplicates
    input_df.drop_duplicates(inplace=True)

    # Scale the numerical features (same as in training)
    numerical_cols = ['capacity', 'ticket_price', 'release_date', 'rating', 'date']
    scaler = joblib.load('program/cinema_booking_prediction/scaler.joblib') #Load scaler here.
    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])


    # Drop low importance features (same as in training)
    low_importance_features = [
        'ticket_price',
        'screen_id',
        'film_id',
        'show_time_category_Morning',
        'Romance',
        'Comedy',
        'Sci-Fi',
        'cinema_location_Cardiff',
        'show_time_category_Afternoon',
        'Drama',
        'Adventure',
        'Action',
        'seat_type_Lower',
        'cinema_id',
        'cinema_location_Bristol',
        'seat_type_VIP',
        'Mystery',
        'seat_type_Upper',
        'Horror',
        'cinema_location_London',
        'cinema_location_Birmingham',
        'Thriller'
    ]

    input_df_reduced = input_df.drop(low_importance_features, axis=1)

    # Reorder columns to match training data order.
    # Reorder columns to match training data order.
    training_columns = ['date', 'capacity', 'release_date', 'rating', 'show_time_category_Evening',
                       'day_of_week_Friday', 'day_of_week_Monday', 'day_of_week_Saturday',
                       'day_of_week_Sunday', 'day_of_week_Thursday', 'day_of_week_Tuesday',
                       'day_of_week_Wednesday']
    
     # Create the day of week columns.
    day_name = pd.to_datetime(input_data['date']).day_name() # Extracts day of week from date.
    for day in ['Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']:
        input_df_reduced[f'day_of_week_{day}'] = 1 if day == day_name else 0 # Creates each column day 
    
    input_df_reduced = input_df_reduced[training_columns]

    # Make the prediction
    prediction = round(model.predict(input_df_reduced)[0])

    # Enforce the capacity constraint.
    capacity = input_data['capacity']
    prediction = min(prediction, capacity) #ensure prediction is not higher than capacity.

    return prediction

test_data_monday = {
    'capacity': 120,
    'release_date': "2023-11-01",
    'date': "2023-11-06",  # Monday
    'rating': 7.0,
    'show_time_category_Evening': 1,
    'show_time_category_Morning': 0,
    'show_time_category_Afternoon': 1,
    'seat_type_Lower': 0,
    'seat_type_Upper': 0,
    'seat_type_VIP': 0,
    'cinema_location_Birmingham': 0,
    'cinema_location_Bristol': 0,
    'cinema_location_Cardiff': 0,
    'cinema_location_London': 1,
    'cinema_id': 1,
    'screen_id': 1,
    'film_id': 1,
    'Action': 0,
    'Adventure': 1,
    'Comedy': 0,
    'Drama': 0,
    'Horror': 0,
    'Mystery': 0,
    'Romance': 0,
    'Sci-Fi': 0,
    'Thriller': 0,
    'ticket_price': 1000,
}

test_data_tuesday = {
    'capacity': 120,
    'release_date': "2023-11-01",
    'date': "2023-11-07",  # Tuesday
    'rating': 7.0,
    'show_time_category_Evening': 1,
    'show_time_category_Morning': 0,
    'show_time_category_Afternoon': 1,
    'seat_type_Lower': 0,
    'seat_type_Upper': 0,
    'seat_type_VIP': 0,
    'cinema_location_Birmingham': 0,
    'cinema_location_Bristol': 0,
    'cinema_location_Cardiff': 0,
    'cinema_location_London': 1,
    'cinema_id': 1,
    'screen_id': 1,
    'film_id': 1,
    'Action': 0,
    'Adventure': 1,
    'Comedy': 0,
    'Drama': 0,
    'Horror': 0,
    'Mystery': 0,
    'Romance': 0,
    'Sci-Fi': 0,
    'Thriller': 0,
    'ticket_price': 1000,
}

test_data_wednesday = {
    'capacity': 120,
    'release_date': "2023-11-01",
    'date': "2023-11-08",  # Wednesday
    'rating': 7.0,
    'show_time_category_Evening': 1,
    'show_time_category_Morning': 0,
    'show_time_category_Afternoon': 1,
    'seat_type_Lower': 0,
    'seat_type_Upper': 0,
    'seat_type_VIP': 0,
    'cinema_location_Birmingham': 0,
    'cinema_location_Bristol': 0,
    'cinema_location_Cardiff': 0,
    'cinema_location_London': 1,
    'cinema_id': 1,
    'screen_id': 1,
    'film_id': 1,
    'Action': 0,
    'Adventure': 1,
    'Comedy': 0,
    'Drama': 0,
    'Horror': 0,
    'Mystery': 0,
    'Romance': 0,
    'Sci-Fi': 0,
    'Thriller': 0,
    'ticket_price': 1000,
}

test_data_thursday = {
    'capacity': 120,
    'release_date': "2023-11-01",
    'date': "2023-11-09",  # Thursday
    'rating': 7.0,
    'show_time_category_Evening': 1,
    'show_time_category_Morning': 0,
    'show_time_category_Afternoon': 1,
    'seat_type_Lower': 0,
    'seat_type_Upper': 0,
    'seat_type_VIP': 0,
    'cinema_location_Birmingham': 0,
    'cinema_location_Bristol': 0,
    'cinema_location_Cardiff': 0,
    'cinema_location_London': 1,
    'cinema_id': 1,
    'screen_id': 1,
    'film_id': 1,
    'Action': 0,
    'Adventure': 1,
    'Comedy': 0,
    'Drama': 0,
    'Horror': 0,
    'Mystery': 0,
    'Romance': 0,
    'Sci-Fi': 0,
    'Thriller': 0,
    'ticket_price': 1000,
}

test_data_friday = {
    'capacity': 120,
    'release_date': "2023-11-01",
    'date': "2023-11-10",  # friday
    'rating': 7.0,
    'show_time_category_Evening': 1,
    'show_time_category_Morning': 0,
    'show_time_category_Afternoon': 1,
    'seat_type_Lower': 0,
    'seat_type_Upper': 0,
    'seat_type_VIP': 0,
    'cinema_location_Birmingham': 0,
    'cinema_location_Bristol': 0,
    'cinema_location_Cardiff': 0,
    'cinema_location_London': 1,
    'cinema_id': 1,
    'screen_id': 1,
    'film_id': 1,
    'Action': 0,
    'Adventure': 1,
    'Comedy': 0,
    'Drama': 0,
    'Horror': 0,
    'Mystery': 0,
    'Romance': 0,
    'Sci-Fi': 0,
    'Thriller': 0,
    'ticket_price': 1000,
}
    
test_data_saturday = {
    'capacity': 120,
    'release_date': "2023-11-01",
    'date': "2023-11-11",  # saturday
    'rating': 7.0,
    'show_time_category_Evening': 1,
    'show_time_category_Morning': 0,
    'show_time_category_Afternoon': 1,
    'seat_type_Lower': 0,
    'seat_type_Upper': 0,
    'seat_type_VIP': 0,
    'cinema_location_Birmingham': 0,
    'cinema_location_Bristol': 0,
    'cinema_location_Cardiff': 0,
    'cinema_location_London': 1,
    'cinema_id': 1,
    'screen_id': 1,
    'film_id': 1,
    'Action': 0,
    'Adventure': 1,
    'Comedy': 0,
    'Drama': 0,
    'Horror': 0,
    'Mystery': 0,
    'Romance': 0,
    'Sci-Fi': 0,
    'Thriller': 0,
    'ticket_price': 1000,
}

test_data_sunday = {
    'capacity': 120,
    'release_date': "2023-11-01",
    'date': "2023-11-12",  # sunday
    'rating': 7.0,
    'show_time_category_Evening': 1,
    'show_time_category_Morning': 0,
    'show_time_category_Afternoon': 1,
    'seat_type_Lower': 0,
    'seat_type_Upper': 0,
    'seat_type_VIP': 0,
    'cinema_location_Birmingham': 0,
    'cinema_location_Bristol': 0,
    'cinema_location_Cardiff': 0,
    'cinema_location_London': 1,
    'cinema_id': 1,
    'screen_id': 1,
    'film_id': 1,
    'Action': 0,
    'Adventure': 1,
    'Comedy': 0,
    'Drama': 0,
    'Horror': 0,
    'Mystery': 0,
    'Romance': 0,
    'Sci-Fi': 0,
    'Thriller': 0,
    'ticket_price': 1000,
}

test_data_mapping = {
    "Monday": test_data_monday,
    "Tuesday": test_data_tuesday,
    "Wednesday": test_data_wednesday,
    "Thursday": test_data_thursday,
    "Friday": test_data_friday,
    "Saturday": test_data_saturday,
    "Sunday": test_data_sunday,
}


for day, data in test_data_mapping.items():
    prediction = predict_tickets_sold(data)
    print(f"Tickets sold on {day}: {prediction}")





def predict_cinema_sales_with_caps(date):
    """
    Predicts the total ticket sales for a cinema with known screen capacities.

    Args:
        date: The date for which to predict sales (string).

    Returns:
        The total predicted ticket sales for the cinema.
    """

    screen_num = 6  # Lets say we have 6 screens
    screen1_cap = 50
    screen2_cap = 100
    screen3_cap = 86
    screen4_cap = 120
    screen5_cap = 110
    screen6_cap = 67

    total_sales = 0

    screen_capacities = [screen1_cap, screen2_cap, screen3_cap, screen4_cap, screen5_cap, screen6_cap]

    for i, capacity in enumerate(screen_capacities):
        # basic screen data dictionary. You'll need to fill in
        # the other features based on your actual data.
        screen_data = {
            'capacity': capacity,
            'release_date': "2023-11-01",  # Example release date
            'date': date,
            'rating': 7.0,  # Example rating
            'show_time_category_Evening': 1, # Example showing time
            'ticket_price': 1000, #example ticket price
            'show_time_category_Morning': 0, #example
            'show_time_category_Afternoon': 1, #example
            'seat_type_Lower': 0, #example
            'seat_type_Upper': 0, #example
            'seat_type_VIP': 1, #example
            'cinema_location_Birmingham': 0, #example
            'cinema_location_Bristol': 0, #example
            'cinema_location_Cardiff': 0, #example
            'cinema_location_London': 1, #example
            'cinema_id': 1, #example
            'screen_id': i + 1, #example
            'film_id': 1, #example
            'Action': 0, #example
            'Adventure': 1, #example
            'Comedy': 0, #example
            'Drama': 0, #example
            'Horror': 0, #example
            'Mystery': 0, #example
            'Romance': 0, #example
            'Sci-Fi': 0, #example
            'Thriller': 0, #example
        }

        sales_for_screen = predict_tickets_sold(screen_data)
        total_sales += sales_for_screen

    return total_sales

# Example usage
date_to_predict = "2023-11-12"
total_cinema_sales = predict_cinema_sales_with_caps(date_to_predict)
# Get the day name
day_name = pd.to_datetime(date_to_predict).day_name()
print(f"Total predicted sales for the cinema on {day_name}: {total_cinema_sales}")
