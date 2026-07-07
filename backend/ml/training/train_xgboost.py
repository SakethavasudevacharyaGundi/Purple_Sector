#load the seasons thing into a pandas dataframe and then train an xgboost model on it keeping the target as lap_time_delta 
#for tyre_degradation model

import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
class XGBoostTrainer:

    def __init__(
        self,
        dataset_path:str,
    ):
        self.dataset_path = dataset_path

    def train(self):
        df = pd.read_parquet(self.dataset_path)
        catattributes=['event_name', 'circuit_name', 'current_compound', 'track_condition', 'position']
        # Drop rows with missing target values
        full_pipeline=ColumnTransformer([('cat', OneHotEncoder(handle_unknown='ignore'), catattributes)])
        df = df.dropna(subset=['lap_time_delta'])

        # Define features and target
        X = df.drop(columns=['lap_time_delta'])
        y = df['lap_time_delta']
        print(X.columns)
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        encoder=full_pipeline.fit(X_train)
        X_train=encoder.transform(X_train)
        X_test=encoder.transform(X_test)
        # Train the XGBoost model
        model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
        model.fit(X_train, y_train)
        # Evaluate the model
        predictions = model.predict(X_test)
        print(predictions[:5])
        mse = ((predictions - y_test) ** 2).mean()
        print(f'Mean Squared Error: {mse}')
        return model
    def save_model(self, model, output_path:str):
        model.save_model(output_path)
if __name__ == "__main__":
    trainer = XGBoostTrainer(dataset_path="data/ml/v1/master_dataset.parquet")
    model = trainer.train()
    trainer.save_model(model, "xgboost_model.json")