import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

'''
This script contains my commonly used visualizations used for ML models 
'''

def TS_plot_actuals_vs_predicted(train_df,predicted_df,target):
    '''
    Args: 
    predicted_df pd.DataFrame: pandas df containing the date, actuals, predicted of the test set.
    train_df pd.DataFrame: pandas df containing the date, actuals of the training set
    target string: name of our target variable

    Returns: plt.plot

    NOTE: Define the figure sizes before this function call :)
    '''

    # Plot the actual quantities for training data
    plt.plot(train_df['Date'], train_df[target], label=f'Training {target}', color='green', linestyle='-', alpha=0.7)

    # Plot the actual vs predicted quantities for test data
    plt.plot(predicted_df['Date'], predicted_df[f'Actual {target}'], label=f'Test {target}', color='blue',linestyle='-', alpha=0.7)
    plt.plot(predicted_df['Date'], predicted_df[f'Predicted {target}'], label=f'Predicted {target}', color='red',  linestyle='--', alpha=0.7)

    # Add title and labels
    plt.title(f'Actual vs Predicted {target}')
    plt.xlabel('Date')
    plt.ylabel('Quantity')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    return plt.figure()

def residual_plot(y_test, y_pred):
    '''
    Args: 
    y_test pd.Dataframe: column containing all actuals for the test set
    y_pred pd.Dataframe: array containing all the predicted values for the test set
    Returns: plt.plot

    NOTE: Define the figure sizes before this function call :)
    '''
    residuals = y_test - y_pred
    # Create residual plot
    plt.scatter(y_pred, residuals)
    plt.axhline(y=0, color='r', linestyle='--')  # Add a horizontal line at y=0
    plt.xlabel("Predicted Values")
    plt.ylabel("Residuals")
    plt.title("Residual Plot")
    plt.show()
    return plt.figure()


def plot_correlation_matrix(df):
    """
    Plots a heatmap of the correlation matrix for numerical features in a DataFrame.
    """
    numerical_df = df.select_dtypes(include=['number'])
    correlation_matrix = numerical_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.show()