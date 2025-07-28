
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
from utils.data_loader import load_student_data

def train_prediction_model():
    df = load_student_data()
    subjects = ['Nepali', 'English', 'Mathematics', 'Science', 'Social&Arts', 'Health_physical_CA', 'Computer']
    behavioral_fields = ['Late_Coming_Frequency', 'Assignment_Submission', 'Class_Attention', 'Responsibility_Behavior']

    # Calculate total marks
    df['Total'] = df[subjects].sum(axis=1)

    # Prepare features including behavioral factors
    X_numeric = df[subjects + ['Attendance']].copy()

    # Encode behavioral categorical variables
    label_encoders = {}
    X_behavioral = pd.DataFrame()

    for field in behavioral_fields:
        if field in df.columns:
            le = LabelEncoder()
            X_behavioral[field] = le.fit_transform(df[field])
            label_encoders[field] = le

    # Combine numeric and behavioral features
    X = pd.concat([X_numeric, X_behavioral], axis=1)
    y = df['Total']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Use Random Forest with more trees for better performance with mixed features
    model = RandomForestRegressor(n_estimators=150, random_state=42, max_depth=10)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    accuracy = 100 - (np.sqrt(mse) / np.mean(y_test) * 100)

    return model, accuracy, label_encoders

def predict_with_behavioral_factors(model, label_encoders, student_data):
    """Make prediction including behavioral factors"""
    subjects = ['Nepali', 'English', 'Mathematics', 'Science', 'Social&Arts', 'Health_physical_CA', 'Computer']
    behavioral_fields = ['Late_Coming_Frequency', 'Assignment_Submission', 'Class_Attention', 'Responsibility_Behavior']

    # Prepare numeric features
    prediction_input = [student_data[s] for s in subjects] + [student_data['Attendance']]

    # Encode behavioral features
    for field in behavioral_fields:
        if field in student_data and field in label_encoders:
            try:
                encoded_value = label_encoders[field].transform([student_data[field]])[0]
                prediction_input.append(encoded_value)
            except ValueError:
                # If the value is not in the training data, use the most common value (0)
                prediction_input.append(0)
        else:
            prediction_input.append(0)  # Default value if field is missing

    predicted_total = model.predict([prediction_input])[0]
    return predicted_total
