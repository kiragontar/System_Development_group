import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import catboost as cb
import joblib  # Import joblib for model saving


# 1. Load the data
df = pd.read_csv('program/cinema_booking_prediction/cinema_data_booking_prediction_essential.csv') # load the data from the csv file.

# 2. Handle missing values and duplicates
#print(df.isnull().sum())  # Check for missing values in each column, we have already checked it, no null values.
df.drop_duplicates(inplace=True) # remove duplicate rows

# 3. Convert False, True one-hot encoded columns to binary 0/1
boolean_cols = df.select_dtypes(include='bool').columns
df[boolean_cols] = df[boolean_cols].astype(int)

# Convert the 'date' column to datetime64[ns]
df['date'] = pd.to_datetime(df['date'])

# 4. Add day of week features

df['day_of_week'] = df['date'].dt.day_name()
df = pd.get_dummies(df, columns=['day_of_week'])
df['date'] = df['date'].apply(lambda x: x.toordinal())  # Convert to ordinal directly.

# 5. Remove rows where tickets_sold is 0.
df = df[df['tickets_sold'] != 0]

# 6. Split the data into features and target variable
X = df.drop('tickets_sold', axis=1)
y = df['tickets_sold']

# 8. Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # split the data into training and test sets.

# 9. Select numerical columns to scale
numerical_cols = ['capacity', 'ticket_price', 'release_date', 'rating', 'date']

# Convert release_date to ordinal, and scale.
X_train['release_date'] = pd.to_datetime(X_train['release_date']).apply(lambda x: x.toordinal()).astype('int64')
X_test['release_date'] = pd.to_datetime(X_test['release_date']).apply(lambda x: x.toordinal()).astype('int64')

scaler = MinMaxScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols]) # Scale the training data
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols]) # Scale the test data using the same scaler

# Save the scaler
joblib.dump(scaler, 'program/cinema_booking_prediction/scaler.joblib') 
print('Scaler saved as scaler.joblib')

# 10. Train and evaluate baseline models
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree Regressor': DecisionTreeRegressor(random_state=42),
    'Random Forest Regressor': RandomForestRegressor(random_state=42),
    'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results[name] = {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'R2': r2}

#Print results
#for name, metrics in results.items():
    #print(f'{name}: MSE={metrics["MSE"]:.2f}, RMSE={metrics["RMSE"]:.2f}, MAE={metrics["MAE"]:.2f}, R2={metrics["R2"]:.2f}')

# We found out the best model is the Gradient Boosting Regressor, we can now proceed to analyze the feature importance of the model.


# 11. Feature Importance (Gradient Boosting)
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train, y_train)

feature_importance = gb_model.feature_importances_ # get the feature importance from the model.
feature_importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': feature_importance}) # create a dataframe with the feature importance.
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False) # sort the dataframe by importance.

# Plot feature importance
plt.figure(figsize=(12, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
plt.title('Feature Importance (Gradient Boosting)')
plt.show()

print(feature_importance_df)


# Having found the low importance features, we can now proceed to tune the hyperparameters of the Gradient Boosting model with the reduced feature set.

# 12. Hyperparameter Tuning (Gradient Boosting) with reduced features.
low_importance_features = ['ticket_price',
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
    'Thriller']

X_train_reduced = X_train.drop(low_importance_features, axis=1)
X_test_reduced = X_test.drop(low_importance_features, axis=1)

print(X_train_reduced.columns)

param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 4, 5],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search_reduced = GridSearchCV(GradientBoostingRegressor(random_state=42), param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_reduced.fit(X_train_reduced, y_train)

best_gb_reduced = grid_search_reduced.best_estimator_
y_pred_best_gb_reduced = best_gb_reduced.predict(X_test_reduced)

mse_best_gb_reduced = mean_squared_error(y_test, y_pred_best_gb_reduced)
rmse_best_gb_reduced = np.sqrt(mse_best_gb_reduced)
mae_best_gb_reduced = mean_absolute_error(y_test, y_pred_best_gb_reduced)
r2_best_gb_reduced = r2_score(y_test, y_pred_best_gb_reduced)

print(f'Gradient Boosting Regressor (Reduced Features, Tuned): MSE={mse_best_gb_reduced:.2f}, RMSE={rmse_best_gb_reduced:.2f}, MAE={mae_best_gb_reduced:.2f}, R2={r2_best_gb_reduced:.2f}')
print(f'Best Parameters (Reduced Features): {grid_search_reduced.best_params_}')



# Hyperparameter tuning for CatBoost
param_grid_catboost = {
    'iterations': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'depth': [3, 4, 5]
}
grid_search_catboost = GridSearchCV(cb.CatBoostRegressor(random_state=42, verbose=0), param_grid_catboost, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_catboost.fit(X_train_reduced, y_train)

best_catboost = grid_search_catboost.best_estimator_
y_pred_best_catboost = best_catboost.predict(X_test_reduced)

mse_best_catboost = mean_squared_error(y_test, y_pred_best_catboost)
rmse_best_catboost = np.sqrt(mse_best_catboost)
mae_best_catboost = mean_absolute_error(y_test, y_pred_best_catboost)
r2_best_catboost = r2_score(y_test, y_pred_best_catboost)

print(f'\nCatBoost (Tuned): MSE={mse_best_catboost:.2f}, RMSE={rmse_best_catboost:.2f}, MAE={mae_best_catboost:.2f}, R2={r2_best_catboost:.2f}')
print(f'Best Parameters (CatBoost): {grid_search_catboost.best_params_}')



# Cross-validation for Gradient Boosting
gb_cv_scores = cross_val_score(best_gb_reduced, X_train_reduced, y_train, cv=5, scoring='neg_mean_squared_error')
gb_cv_rmse_scores = np.sqrt(-gb_cv_scores)

print("\nGradient Boosting Cross-Validation Results:")
print(f"RMSE Scores: {gb_cv_rmse_scores}")
print(f"Mean RMSE: {gb_cv_rmse_scores.mean()}")
print(f"Std RMSE: {gb_cv_rmse_scores.std()}")

# Cross-validation for CatBoost
catboost_cv_scores = cross_val_score(best_catboost, X_train_reduced, y_train, cv=5, scoring='neg_mean_squared_error')
catboost_cv_rmse_scores = np.sqrt(-catboost_cv_scores)

print("\nCatBoost Cross-Validation Results:")
print(f"RMSE Scores: {catboost_cv_rmse_scores}")
print(f"Mean RMSE: {catboost_cv_rmse_scores.mean()}")
print(f"Std RMSE: {catboost_cv_rmse_scores.std()}")


# Save the trained Gradient Boosting model using joblib
joblib.dump(best_gb_reduced, 'program/cinema_booking_prediction/gradient_boosting_model.joblib')

print("Gradient Boosting model saved as 'gradient_boosting_model.joblib'")