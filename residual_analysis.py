import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from retrieve_sites import target_param

class ResidualAnalysis:
    def __init__(self, filepath, target_param):
        self.df = pd.read_csv(filepath)
        self.target_param = target_param
        self.model = LinearRegression()
        self.setup_plot()

    def setup_plot(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(15, 7))  # One subplot for the regression, one for residuals

    def preprocess_data(self):
        # Specifically focus on the best feature 00480
        X = self.df[['00480']].dropna()
        y = self.df.loc[X.index, self.target_param]  # Ensure alignment of target and feature
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_and_evaluate(self):
        X_train, X_test, y_train, y_test = self.preprocess_data()
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Plotting the results
        self.ax1.scatter(X_test, y_test, color='blue', label='Actual')
        self.ax1.plot(X_test, y_pred, color='red', label='Predicted')
        self.ax1.set_title(f'Linear Regression - Feature 00480\nR2: {r2:.2f}, MSE: {mse:.2f}')
        self.ax1.set_xlabel('00480')
        self.ax1.set_ylabel(self.target_param)
        self.ax1.legend()

        # Plotting residuals
        residuals = y_test - y_pred
        self.ax2.scatter(y_pred, residuals, color='blue')
        self.ax2.hlines(y=0, xmin=min(y_pred), xmax=max(y_pred), colors='red', linestyles='--')
        self.ax2.set_title('Residual Plot')
        self.ax2.set_xlabel('Predicted values')
        self.ax2.set_ylabel('Residuals')

    def run(self):
        self.train_and_evaluate()
        plt.tight_layout()
        plt.show()

def ResidualAnalysis():
    filepath = 'clean_data.csv'
    try:
        modeler = ResidualAnalysis(filepath, target_param)
        modeler.run()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    ResidualAnalysis()
