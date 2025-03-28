import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, KFold
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import lightgbm as lgb
import joblib  # Import joblib for model saving

# 1. Load the data
df = pd.read_csv('program\cinema_booking_prediction\cinema_data_booking_prediction_essential.csv') # load the data from the csv file.

# 2. Handle missing values and duplicates
print(df.isnull().sum())  # Check for missing values in each column
df.drop_duplicates(inplace=True) # remove duplicate rows

# 3. Encode categorical variables
label_encoder = LabelEncoder()
df['seat_type_encoded'] = label_encoder.fit_transform(df['seat_type']) # encode the seat_type column into numerical values.

onehot_encoder = OneHotEncoder(sparse_output=False, drop='first') # converts nominal categorical features into a numerical format. sparse_output=False returns the encoded data as a dense NumPy array. drop='first' means that the first category is dropped to avoid multicollinearity.
onehot_encoded = onehot_encoder.fit_transform(df[['cinema_location']]) # encode the cinema_location column into numerical values.
onehot_df = pd.DataFrame(onehot_encoded, columns=onehot_encoder.get_feature_names_out(['cinema_location']), index=df.index) # convert the encoded data into a dataframe, with the column names as the cinema locations.
df = pd.concat([df, onehot_df], axis=1) # add the encoded cinema_location columns to the dataframe.

# 5. Drop original categorical columns
df = df.drop(['cinema_location', 'seat_type'], axis=1) 

# 6. Cap outliers using IQR
def cap_outliers_iqr(df, col):
    q1 = df[col].quantile(0.25) # get the 25th percentile of the column.
    q3 = df[col].quantile(0.75) # get the 75th percentile of the column.
    iqr = q3 - q1 # calculate the interquartile range.
    if iqr == 0:
        return df # Return df, do not try to cap
    lower_bound = q1 - (1.5 * iqr) # calculate the lower bound for outliers.
    upper_bound = q3 + (1.5 * iqr) # calculate the upper bound for outliers.
    if np.isnan(lower_bound) or np.isnan(upper_bound):
        return df # return the df, do not try to cap.
    df[col] = df[col].apply(lambda x: lower_bound if x < lower_bound else upper_bound if x > upper_bound else x) # cap the outliers in the column.
    return df

# Cap outliers in numerical columns, excluding one-hot encoded columns
numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
one_hot_cols = [col for col in numerical_cols if 'cinema_location_' in col]
continuous_cols = [col for col in numerical_cols if col not in one_hot_cols and col != 'tickets_sold'] # do not cap the target variable.

for col in continuous_cols:
    df = cap_outliers_iqr(df, col)


# 7. Split the data into features and target variable
X = df.drop('tickets_sold', axis=1)
y = df['tickets_sold']

# 8. Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # split the data into training and test sets.

# 9. Scale numerical variables using MinMaxScaler (excluding IDs)
numerical_cols = X_train.select_dtypes(include=['number']).columns.tolist()
scaler = MinMaxScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols]) # scale the numerical columns in the training set.
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols]) # scale the numerical columns in the test set.


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

# 11. Print results
for name, metrics in results.items():
    print(f'{name}: MSE={metrics["MSE"]:.2f}, RMSE={metrics["RMSE"]:.2f}, MAE={metrics["MAE"]:.2f}, R2={metrics["R2"]:.2f}')

# We found out the best model is the Gradient Boosting Regressor, we can now proceed to analyze the feature importance of the model.
"""
# 12. Feature Importance (Gradient Boosting)
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
"""
# Having found the low importance features, we can now proceed to tune the hyperparameters of the Gradient Boosting model with the reduced feature set.


# 13. Hyperparameter Tuning (Gradient Boosting) with reduced features.
low_importance_features = ['ticket_price', 'year', 'seat_type_encoded', 'cinema_location_Bristol', 'cinema_location_Cardiff', 'cinema_location_London']
X_train_reduced = X_train.drop(low_importance_features, axis=1)
X_test_reduced = X_test.drop(low_importance_features, axis=1)
trained_reduced_features = X_train_reduced.columns.tolist()
joblib.dump(trained_reduced_features, 'program/cinema_booking_prediction/trained_reduced_features.joblib')


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


# 14. LightGBM Regressor with reduced features and hyperparameter tuning.

param_grid = {
    'n_estimators': [100, 300], 
    'learning_rate': [0.05, 0.1], 
    'num_leaves': [15, 63],
    'max_depth': [4, -1], 
    'min_child_samples': [20], 
    'subsample': [0.8], 
    'colsample_bytree': [0.8], 
    'reg_alpha': [0], 
    'reg_lambda': [0]
}

grid_search_reduced = GridSearchCV(lgb.LGBMRegressor(random_state=42), param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1, verbose=1)
grid_search_reduced.fit(X_train_reduced, y_train)

best_lgbm_reduced = grid_search_reduced.best_estimator_
y_pred_best_lgbm_reduced = best_lgbm_reduced.predict(X_test_reduced)

mse_best_lgbm_reduced = mean_squared_error(y_test, y_pred_best_lgbm_reduced)
rmse_best_lgbm_reduced = np.sqrt(mse_best_lgbm_reduced)
mae_best_lgbm_reduced = mean_absolute_error(y_test, y_pred_best_lgbm_reduced)
r2_best_lgbm_reduced = r2_score(y_test, y_pred_best_lgbm_reduced)

print(f'LightGBM Regressor (Reduced Features, Tuned): MSE={mse_best_lgbm_reduced:.2f}, RMSE={rmse_best_lgbm_reduced:.2f}, MAE={mae_best_lgbm_reduced:.2f}, R2={r2_best_lgbm_reduced:.2f}')
print(f'Best Parameters (Reduced Features): {grid_search_reduced.best_params_}')


# 15. K-Fold Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# LightGBM Cross-Validation
lgbm_cv_scores = cross_val_score(best_lgbm_reduced, X_train_reduced, y_train, cv=kf, scoring='neg_mean_squared_error')
print(f'LightGBM CV MSE: {-lgbm_cv_scores.mean():.2f}')

# 16. LightGBM Feature Importance
feature_importance_lgbm = best_lgbm_reduced.feature_importances_
feature_importance_df_lgbm = pd.DataFrame({'Feature': X_train_reduced.columns, 'Importance': feature_importance_lgbm})
feature_importance_df_lgbm = feature_importance_df_lgbm.sort_values(by='Importance', ascending=False)

# Gradient Boosting Cross-Validation
gb_cv_scores = cross_val_score(best_gb_reduced, X_train_reduced, y_train, cv=kf, scoring='neg_mean_squared_error')
print(f'Gradient Boosting CV MSE: {-gb_cv_scores.mean():.2f}')

# Plot feature importance
plt.figure(figsize=(12, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df_lgbm)
plt.title('Feature Importance (LightGBM)')
plt.show()

print(feature_importance_df_lgbm)

# 17. Save the LightGBM Model
joblib.dump(best_lgbm_reduced, 'program/cinema_booking_prediction/best_lgbm_model.joblib') # save the best LightGBM model to a file.
joblib.dump(scaler, 'program/cinema_booking_prediction/scaler.joblib') #save the scaler to use in predict_tickets
joblib.dump(label_encoder, 'program/cinema_booking_prediction/label_encoder.joblib')
joblib.dump(onehot_encoder, 'program/cinema_booking_prediction/onehot_encoder.joblib')
print('LightGBM model saved as best_lgbm_model.joblib') 

