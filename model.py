import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from retrieve_sites import target_param

class WaterDataModeler:
    def __init__(self, filepath, target_param):
        self.df = pd.read_csv(filepath)
        self.target_param = target_param
        self.models = {'Linear': LinearRegression()}
        self.results = {}
        self.model_results = {model: [] for model in self.models}
        self.setup_plot()

    def setup_plot(self):
        num_models = len(self.models)
        self.fig, self.axes = plt.subplots(num_models, 3, figsize=(15, 6))
        if num_models == 1:
            self.axes = [self.axes]

    def preprocess_data(self, feature):
        subset = self.df.dropna(subset=[feature, self.target_param])
        X = subset[[feature]]
        y = subset[self.target_param]
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_and_evaluate(self, model_name, X_train, X_test, y_train, y_test, feature):
        model = self.models[model_name]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        self.model_results[model_name].append({
            'Feature': feature, 'MSE': mse, 'R2': r2,
            'X_test': X_test, 'y_test': y_test, 'y_pred': y_pred
        })

    def plot_results(self):
        for i, (model_name, results) in enumerate(self.model_results.items()):
            top_features = sorted(results, key=lambda x: x['R2'], reverse=True)[:3]
            for j, result in enumerate(top_features):
                ax = self.axes[i][j]
                ax.scatter(result['X_test'], result['y_test'], color='blue', label='Actual')
                ax.plot(result['X_test'], result['y_pred'], color='red', label='Predicted')
                ax.set_title(f'{model_name} - {result["Feature"]}')
                ax.set_xlabel(result['Feature'])
                ax.set_ylabel(self.target_param)
                ax.legend()
                ax.text(0.5, -0.2, f'R²: {result["R2"]:.2f}, MSE: {result["MSE"]:.2f}', 
                        transform=ax.transAxes, ha='center', fontsize=10)

    def run(self):
        features = self.df.columns[2:]
        features = features.drop(self.target_param)
        for feature in features:
            X_train, X_test, y_train, y_test = self.preprocess_data(feature)
            for model_name in self.models:
                self.train_and_evaluate(model_name, X_train, X_test, y_train, y_test, feature)

        self.plot_results()
        plt.tight_layout(pad=3.0)
        plt.show()

def model_data(target_param = target_param):
    filepath = 'clean_data.csv'
    modeler = WaterDataModeler(filepath, target_param)
    modeler.run()

if __name__ == '__main__':
    model_data()
