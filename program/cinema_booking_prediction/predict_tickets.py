import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def predict_tickets(input_data):
    """
    Loads the saved LightGBM model and makes predictions.

    Args:
        input_data (pd.DataFrame): Input data for prediction.

    Returns:
        float: Predicted number of tickets sold.
    """
    try:
        # 1. Load the saved model
        loaded_model = joblib.load('program/cinema_booking_prediction/best_lgbm_model.joblib')
        loaded_scaler = joblib.load('program/cinema_booking_prediction/scaler.joblib') #load the scaler used for scaling the input data
        loaded_label_encoder = joblib.load('program/cinema_booking_prediction/label_encoder.joblib')
        loaded_onehot_encoder = joblib.load('program/cinema_booking_prediction/onehot_encoder.joblib')
        trained_reduced_features = joblib.load('program/cinema_booking_prediction/trained_reduced_features.joblib') # Load trained reduced feature names

        # 2. Preprocess the input data
        df = input_data.copy()
        print("\nInitial df:\n", df)

        # Input Range Validation (as before)
        if not (1 <= df['film_popularity'][0] <= 5):
            raise ValueError("film_popularity must be between 1 and 5.")
        if not (1 <= df['show_time'][0] <= 3):
            raise ValueError("show_time must be between 1 and 3.")
        if df['ticket_price'][0] < 0:
            raise ValueError("ticket_price must be non-negative.")
        if df['cinema_location'][0] not in ['Birmingham', 'Bristol', 'Cardiff', 'London']:
            raise ValueError("cinema_location must be one of 'Birmingham', 'Bristol', 'Cardiff', or 'London'.")
        if not (50 <= df['capacity'][0] <= 120):
            raise ValueError("capacity must be between 50 and 120.")
        if df['seat_type'][0] not in ['Lower Hall', 'Upper Hall', 'VIP']:
            raise ValueError("seat_type must be one of 'Lower Hall', 'Upper Hall', or 'VIP'.")

        df.drop_duplicates(inplace=True)
        df['seat_type_encoded'] = loaded_label_encoder.transform(df['seat_type'])
        onehot_encoded = loaded_onehot_encoder.transform(df[['cinema_location']])
        onehot_df = pd.DataFrame(onehot_encoded, columns=loaded_onehot_encoder.get_feature_names_out(['cinema_location']), index=df.index)
        df = pd.concat([df, onehot_df], axis=1)
        df = df.drop(['cinema_location', 'seat_type'], axis=1)
        print("\nAfter encoding and dropping categoricals:\n", df)

        def cap_outliers_iqr(df, col):
            # ... (your outlier capping function) ...
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            df[col] = df[col].apply(lambda x: lower_bound if x < lower_bound else upper_bound if x > upper_bound else x)
            return df

        if 'tickets_sold' in df.columns:
            X = df.drop('tickets_sold', axis=1)
        else:
            X = df.copy()

        # Align with trained reduced features FIRST
        X_reduced = pd.DataFrame(columns=trained_reduced_features)
        for col in trained_reduced_features:
            if col in X.columns:
                X_reduced[col] = X[col]
            else:
                X_reduced[col] = 0  # Fill missing columns with 0
        print("\nX_reduced after alignment:\n", X_reduced)

        # Identify numerical columns within the ALIGNED X_reduced
        numerical_cols_reduced = X_reduced.select_dtypes(include=['number']).columns.tolist()
        print("\nNumerical columns in X_reduced (after alignment):", numerical_cols_reduced)

        # Scale the numerical columns of the ALIGNED X_reduced
        X_reduced[numerical_cols_reduced] = loaded_scaler.transform(X_reduced[numerical_cols_reduced])
        print("\nX_reduced after scaling:\n", X_reduced)

        # 4. Make predictions
        prediction = loaded_model.predict(X_reduced)
        return prediction[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage (for testing):
if __name__ == "__main__":
    # Create sample input data (replace with your actual data)
    sample_data = pd.DataFrame({
        'film_popularity': [4],
        'show_time': [3],
        'capacity': [100],
        'day_of_week': [4],
        'month': [12],
        'ticket_price': [1100],
        'year': [2023],
        'seat_type': ['Upper Hall'],
        'cinema_location': ['London'],
    })

    try:
        predicted_tickets = predict_tickets(sample_data)
        if predicted_tickets is not None:
            print(f'Predicted Tickets Sold: {predicted_tickets:.2f}')
    except Exception as e:
        print(f"An error occurred: {e}")