import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Title for the app
st.title("Random Forest Model Evaluation and Prediction App")

# File uploader for CSV dataset
uploaded_file = st.file_uploader("Upload a CSV file for training", type="csv")

# Initialize global variables for the trained model and dataset
if 'trained_model' not in st.session_state:
    st.session_state.trained_model = None
if 'X' not in st.session_state:
    st.session_state.X = None
if 'y' not in st.session_state:
    st.session_state.y = None

# Function to process data and prepare it for training
def process_data(file_path):
    try:
        data = pd.read_csv(file_path)
        st.success("Dataset loaded successfully.")
    except Exception as e:
        st.error(f"An error occurred while loading the file: {e}")
        return None, None

    # Handle missing values
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    categorical_columns = data.select_dtypes(exclude=[np.number]).columns

    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())
    data[categorical_columns] = data[categorical_columns].fillna(data[categorical_columns].mode().iloc[0])

    # Separate features and labels
    try:
        X = data.drop("label", axis=1)
        y = data["label"]
    except KeyError:
        st.error("The dataset must contain a 'label' column for classification.")
        return None, None

    return X, y

# Function to train the model using a pipeline
def train_random_forest(X, y):
    # Define column transformer to handle categorical and numerical features
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    # Create the preprocessing pipeline for numeric and categorical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),  # Standardize numerical features
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)  # Encode categorical features
        ])

    # Create a pipeline with the preprocessor and the RandomForest model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42, n_jobs=-1))
    ])

    # Train the model
    model.fit(X, y)
    st.session_state.trained_model = model

    # Evaluate the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    st.write("### Random Forest Model Evaluation")
    st.write(f"**Accuracy**: {accuracy:.4f}")
    st.write("**Confusion Matrix**:")
    st.write(confusion_matrix(y_test, y_pred))
    st.write("**Classification Report**:")
    st.text(classification_report(y_test, y_pred))

# Function to predict a single domain
def predict_domain(input_data):
    if st.session_state.trained_model is None:
        st.error("No trained model is available. Please upload a dataset and train the model first.")
        return

    try:
        # Use the stored column names from training data (X) for the prediction
        input_df = pd.DataFrame([input_data], columns=st.session_state.X.columns)

        # Make prediction using the trained model
        prediction = st.session_state.trained_model.predict(input_df)
        st.write(f"### Predicted Label: {prediction[0]}")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

# Display the app UI logic
if uploaded_file is not None:
    st.session_state.X, st.session_state.y = process_data(uploaded_file)
    
    # Only proceed if the data is valid and we have X and y
    if st.session_state.X is not None and st.session_state.y is not None:
        if st.button("Train Random Forest Model"):
            train_random_forest(st.session_state.X, st.session_state.y)

# Input form for domain testing
if st.session_state.X is not None:  # Ensure that X is defined before displaying input fields
    with st.form("domain_prediction"):
        st.write("### Test Domain Prediction")
        domain_features = {}
        for feature in st.session_state.X.columns:  # Use training columns
            domain_features[feature] = st.text_input(f"Enter value for {feature}")
        submitted = st.form_submit_button("Predict")
        if submitted:
            if st.session_state.trained_model is None:
                st.error("You need to train the model first by uploading a dataset and clicking 'Train Random Forest Model'.")
            else:
                predict_domain(domain_features)
