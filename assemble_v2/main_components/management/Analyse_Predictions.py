import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib
from datetime import datetime
from database.database_settings import SessionLocal
from main_components.services.screening_service import ScreeningService
from main_components.services.cinema_service import CinemaService
from main_components.services.screen_service import ScreenService
from main_components.services.film_service import FilmService
from main_components.services.city_service import CityService

class PredictionAnalysisPage(tk.Frame):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.session = SessionLocal()
        self.cinema_service = CinemaService(self.session) 
        self.screening_service = ScreeningService(self.session)
        self.screen_service = ScreenService(self.session)
        self.film_service = FilmService(self.session)
        self.city_service = CityService(self.session)
        self.setup_ui()
        self.model = joblib.load('gradient_boosting_model.joblib')
        self.scaler = joblib.load('scaler.joblib')

    def setup_ui(self):
        # --- Prediction for a Specific Showing ---
        ttk.Label(self, text="--- Predict for a Specific Showing ---").grid(row=0, column=0, columnspan=2, pady=(10, 5))

        ttk.Label(self, text="Screening ID:").grid(row=1, column=0)
        self.screening_id_entry = ttk.Entry(self)
        self.screening_id_entry.grid(row=1, column=1)

        self.predict_button = ttk.Button(self, text="Predict Tickets Sold", command=self.predict_tickets_for_showing)
        self.predict_button.grid(row=2, column=0, columnspan=2, pady=5) 

        self.output_label = ttk.Label(self, text="Predicted Tickets For Showing:")
        self.output_label.grid(row=3, column=0)
        self.prediction_result_label = ttk.Label(self, text="")
        self.prediction_result_label.grid(row=3, column=1)

        # --- Prediction for Total Sales for All Cinemas on a Day ---
        ttk.Label(self, text="--- Predict Total Sales for All Cinemas on a Day ---").grid(row=4, column=0, columnspan=2, pady=(15, 5))

        ttk.Label(self, text="Date (YYYY-MM-DD):").grid(row=5, column=0)
        self.day_prediction_date_entry = ttk.Entry(self)
        self.day_prediction_date_entry.grid(row=5, column=1)

        self.predict_day_sales_button = ttk.Button(self, text="Predict Day Sales (All Cinemas)", command=self.predict_total_day_sales_for_all_cinemas)
        self.predict_day_sales_button.grid(row=6, column=0, columnspan=2, pady=5) 

        self.day_sales_output_label = ttk.Label(self, text="Predicted Total Tickets Sold for All Cinemas on:")
        self.day_sales_output_label.grid(row=7, column=0)
        self.day_sales_result_label = ttk.Label(self, text="")
        self.day_sales_result_label.grid(row=7, column=1)

        # --- Prediction for Total Sales for a Specific Cinema on a Day ---
        ttk.Label(self, text="--- Predict Total Sales for a Specific Cinema on a Day ---").grid(row=8, column=0, columnspan=2, pady=(15, 5))

        ttk.Label(self, text="Specific Cinema ID:").grid(row=9, column=0)
        self.specific_cinema_id_entry = ttk.Entry(self)
        self.specific_cinema_id_entry.grid(row=9, column=1)

        ttk.Label(self, text="Date (YYYY-MM-DD):").grid(row=10, column=0)
        self.specific_cinema_date_entry = ttk.Entry(self)
        self.specific_cinema_date_entry.grid(row=10, column=1)

        self.predict_specific_cinema_sales_button = ttk.Button(self, text="Predict Specific Cinema Sales", command=self.predict_total_day_sales_for_specific_cinema)
        self.predict_specific_cinema_sales_button.grid(row=11, column=0, columnspan=2, pady=5) 

        self.specific_cinema_sales_output_label = ttk.Label(self, text="Predicted Total Tickets Sold for Specific Cinema:")
        self.specific_cinema_sales_output_label.grid(row=12, column=0)
        self.specific_cinema_sales_result_label = ttk.Label(self, text="")
        self.specific_cinema_sales_result_label.grid(row=12, column=1)

        # Back button
        ttk.Button(self, text="Back", command=self.go_back).grid(row=13, column=0, columnspan=2, pady=10) 

    def datetime_to_excel(self, datetime_obj):
        origin = datetime(1900, 1, 1)
        return (datetime_obj - origin).days + 2
    
    def predict_tickets_sold(self, input_data):
        input_df = pd.DataFrame([input_data])
        # Convert release_date and date from string to Excel serial number
        input_df['release_date'] = pd.to_datetime(input_df['release_date']).apply(self.datetime_to_excel)
        input_df['date'] = pd.to_datetime(input_df['date']).apply(self.datetime_to_excel)

        # Convert boolean columns to 0/1
        boolean_cols = input_df.select_dtypes(include='bool').columns
        input_df[boolean_cols] = input_df[boolean_cols].astype(int)

        # Remove duplicates
        input_df.drop_duplicates(inplace=True)

        # Scale the numerical features (same as in training)
        numerical_cols = ['capacity', 'ticket_price', 'release_date', 'rating', 'date'] 
        input_df[numerical_cols] = self.scaler.transform(input_df[numerical_cols])

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
        prediction = round(self.model.predict(input_df_reduced)[0])

        # Enforce the capacity constraint.
        capacity = input_data['capacity']
        prediction = min(prediction, capacity) #ensure prediction is not higher than capacity.

        return prediction


    def predict_tickets_for_showing(self, input_data = None):
        screening_id_str = self.screening_id_entry.get().strip()

        if not screening_id_str:
            messagebox.showerror("Input Error", "Please enter a Screening ID.")
            return
        
        try:
            screening_id = int(screening_id_str)
            if screening_id <= 0:
                messagebox.showerror("Input Error", "Screening ID must be a positive integer.")
                return

            screening = self.screening_service.get_screening_by_id(screening_id)
            if not screening:
                messagebox.showerror("Input Error", f"Screening with ID {screening_id} not found.")
                return
            cinema_id = screening.cinema_id
            film_id = screening.film_id
            screen_id = screening.screen_id
            date = screening.date
            start_time = screening.start_time

            film = self.film_service.get_film_by_id(film_id)
            release_date = film.release_date
            rating = film.critic_rating
            genres = film.get_genre()
            film_title = film.name

            genre_scores = {
                "Action": 0,
                "Adventure": 0,
                "Comedy": 0,
                "Drama": 0,
                "Horror": 0,
                "Mystery": 0,
                "Romance": 0,
                "Sci-Fi": 0,
                "Thriller": 0,
            }
            
            for genre in genres:
                if genre in genre_scores:
                    genre_scores[genre] = 1

            cinema = self.cinema_service.get_cinema_by_id(cinema_id)
            city_id = cinema.city_id
            city = self.city_service.get_city_by_id(city_id)
            city_name = city.name
            birmingham = 1 if city_name == "Birmingham" else 0
            bristol = 1 if city_name == "Bristol" else 0
            cardiff = 1 if city_name == "Cardiff" else 0
            london = 1 if city_name == "London" else 0
            screen = self.screen_service.get_screen_by_id(screen_id)
            capacity = screen.total_capacity

            start_hour = start_time.hour
            start_minute = start_time.minute
            start_second = start_time.second

            morning = 1 if 8 <= start_hour < 12 else 0
            afternoon = 1 if 12 <= start_hour < 17 else 0
            evening = 1 if 17 <= start_hour <= 23 else 0
            

            # Create input dictionary
            input_data = {
                'capacity': capacity,
                'release_date': release_date,
                'date': date,
                'rating': rating,
                'show_time_category_Evening': evening,
                'show_time_category_Morning': morning,
                'show_time_category_Afternoon': afternoon,
                'seat_type_Lower': 0,
                'seat_type_Upper': 0,
                'seat_type_VIP': 0,
                'cinema_location_Birmingham': birmingham,
                'cinema_location_Bristol': bristol,
                'cinema_location_Cardiff': cardiff,
                'cinema_location_London': london,
                'cinema_id': cinema_id,
                'screen_id': screen_id,
                'film_id': film_id,
                'Action': genre_scores["Action"],
                'Adventure': genre_scores["Adventure"],
                'Comedy': genre_scores["Comedy"],
                'Drama': genre_scores["Drama"],
                'Horror': genre_scores["Horror"],
                'Mystery': genre_scores["Mystery"],
                'Romance': genre_scores["Romance"],
                'Sci-Fi': genre_scores["Sci-Fi"],
                'Thriller': genre_scores["Thriller"],
                'ticket_price': 1000, # Cant calculate as every seat in a screen has a different price.
            }

            # Call predict_tickets_sold
            prediction = self.predict_tickets_sold(input_data)

            # Display prediction with film title and showing time
            output_text = f"Film: {film_title}\nDate: {date}\nStart Time: {start_time}\nPredicted Tickets: {prediction}"
            self.output_label.config(text=output_text)

        except ValueError as ve:
            messagebox.showerror("Input Error", "Invalid Screening ID. Please enter a whole number.")
        except Exception as e:
            messagebox.showerror("An Error Occurred", f"An unexpected error occurred: {e}")
        finally:
            self.session.close()
        
    def predict_total_day_sales_for_all_cinemas(self):
        date_str = self.day_prediction_date_entry.get().strip()

        if not date_str:
            messagebox.showerror("Input Error", "Please enter a date.")
            return

        try:
            prediction_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
            return

        all_cinemas = self.cinema_service.get_all_cinemas()
        total_predicted_sales = 0

        for cinema in all_cinemas:
            screenings_on_date = self.screening_service.get_screenings_by_cinema_and_date(cinema.cinema_id, prediction_date)
            for screening in screenings_on_date:
                film = self.film_service.get_film_by_id(screening.film_id)
                screen_obj = self.screen_service.get_screen_by_id(screening.screen_id)

                if film and screen_obj:
                    start_hour = screening.start_time.hour
                    morning = 1 if 8 <= start_hour < 12 else 0
                    afternoon = 1 if 12 <= start_hour < 17 else 0
                    evening = 1 if 17 <= start_hour <= 23 else 0
                    genres = film.get_genre()
                    genre_scores = {genre: 1 if genre in genres else 0 for genre in ["Action", "Adventure", "Comedy", "Drama", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller"]}
                    city_id = cinema.city_id
                    city = self.city_service.get_city_by_id(city_id)
                    city_name = city.name
                    birmingham = 1 if city_name == "Birmingham" else 0
                    bristol = 1 if city_name == "Bristol" else 0
                    cardiff = 1 if city_name == "Cardiff" else 0
                    london = 1 if city_name == "London" else 0

                    input_data = {
                        'capacity': screen_obj.total_capacity,
                        'release_date': film.release_date,
                        'date': screening.date,
                        'rating': film.critic_rating,
                        'show_time_category_Evening': evening,
                        'show_time_category_Morning': morning,
                        'show_time_category_Afternoon': afternoon,
                        'seat_type_Lower': 0,
                        'seat_type_Upper': 0,
                        'seat_type_VIP': 0,
                        'cinema_location_Birmingham': birmingham,
                        'cinema_location_Bristol': bristol,
                        'cinema_location_Cardiff': cardiff,
                        'cinema_location_London': london,
                        'cinema_id': cinema.cinema_id,
                        'screen_id': screen_obj.screen_id,
                        'film_id': film.film_id,
                        **genre_scores,
                        'ticket_price': 1000, # Placeholder
                    }
                    total_predicted_sales += self.predict_tickets_sold(input_data)

        self.day_sales_result_label.config(text=f"all cinemas on {prediction_date.strftime('%Y-%m-%d')}: {total_predicted_sales}")
        



    def predict_total_day_sales_for_specific_cinema(self):
        cinema_id_str = self.specific_cinema_id_entry.get().strip()
        date_str = self.specific_cinema_date_entry.get().strip()

        if not cinema_id_str:
            messagebox.showerror("Input Error", "Please enter a Cinema ID.")
            return
        if not date_str:
            messagebox.showerror("Input Error", "Please enter a date.")
            return

        try:
            cinema_id = int(cinema_id_str)
            if cinema_id <= 0:
                messagebox.showerror("Input Error", "Cinema ID must be a positive integer.")
                return
            prediction_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid Cinema ID or Date format (YYYY-MM-DD).")
            return

        cinema = self.cinema_service.get_cinema_by_id(cinema_id)
        if not cinema:
            messagebox.showerror("Input Error", f"Cinema with ID {cinema_id} not found.")
            return

        screenings_on_date = self.screening_service.get_screenings_by_cinema_and_date(cinema_id, prediction_date)
        total_predicted_sales = 0

        if not screenings_on_date:
            self.specific_cinema_sales_result_label.config(text=f"No screenings found for Cinema {cinema_id} on {prediction_date.strftime('%Y-%m-%d')}.")
            return

        for screening in screenings_on_date:
            film = self.film_service.get_film_by_id(screening.film_id)
            screen_obj = self.screen_service.get_screen_by_id(screening.screen_id)

            if film and screen_obj:
                start_hour = screening.start_time.hour
                morning = 1 if 8 <= start_hour < 12 else 0
                afternoon = 1 if 12 <= start_hour < 17 else 0
                evening = 1 if 17 <= start_hour <= 23 else 0
                genres = film.get_genre()
                genre_scores = {genre: 1 if genre in genres else 0 for genre in ["Action", "Adventure", "Comedy", "Drama", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller"]}
                city_id = cinema.city_id
                city = self.city_service.get_city_by_id(city_id)
                city_name = city.name
                birmingham = 1 if city_name == "Birmingham" else 0
                bristol = 1 if city_name == "Bristol" else 0
                cardiff = 1 if city_name == "Cardiff" else 0
                london = 1 if city_name == "London" else 0

                input_data = {
                    'capacity': screen_obj.total_capacity,
                    'release_date': film.release_date,
                    'date': screening.date,
                    'rating': film.critic_rating,
                    'show_time_category_Evening': evening,
                    'show_time_category_Morning': morning,
                    'show_time_category_Afternoon': afternoon,
                    'seat_type_Lower': 0,
                    'seat_type_Upper': 0,
                    'seat_type_VIP': 0,
                    'cinema_location_Birmingham': birmingham,
                    'cinema_location_Bristol': bristol,
                    'cinema_location_Cardiff': cardiff,
                    'cinema_location_London': london,
                    'cinema_id': cinema.cinema_id,
                    'screen_id': screen_obj.screen_id,
                    'film_id': film.film_id,
                    **genre_scores,
                    'ticket_price': 1000, # Placeholder
                }
                total_predicted_sales += self.predict_tickets_sold(input_data)

        self.specific_cinema_sales_result_label.config(text=f"Cinema {cinema_id} on {prediction_date.strftime('%Y-%m-%d')}: {total_predicted_sales}")


            

    def go_back(self):
        if self.callback:
            self.callback("back")