import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def clean_and_encode(df):
    df.columns = df.columns.str.strip()
    df.drop_duplicates(inplace=True)

    encoder = LabelEncoder()
    df['LUNG_CANCER'] = encoder.fit_transform(df['LUNG_CANCER'])
    df['GENDER'] = encoder.fit_transform(df['GENDER'])
    return df

def prepare_features_and_target(df):
    X = df.drop(columns=['LUNG_CANCER'])
    y = df['LUNG_CANCER']

    # Convert binary features from (1,2) → (0,1)
    for col in X.columns[2:]:
        X[col] = X[col] - 1

    return X, y

def standardize_age(X_train, X_test):
    scaler = StandardScaler()
    X_train['AGE'] = scaler.fit_transform(X_train[['AGE']])
    X_test['AGE'] = scaler.transform(X_test[['AGE']])
    return X_train, X_test, scaler
