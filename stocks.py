import requests
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime # Import the datetime module

# --- IMPORTANT: Replace with your actual Finnhub API key ---
API_KEY = 'd0pnf21r01qgccua7rl0d0pnf21r01qgccua7rlg' 
# For testing, you might use a dummy key, but it won't fetch real data.

def get_finnhub_quote(symbol):
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}'
    r = requests.get(url)
    data = r.json()
    
    try:
        current = data.get('c')
        previous = data.get('pc')
        if current is not None and previous is not None and previous != 0:
            change_percent = ((current - previous) / previous) * 100
            return change_percent
        return None
    except Exception as e:
        print(f"Error fetching quote for {symbol}: {e}")
        return None

def get_performance_data(symbols):
    """
    Fetches daily percentage change for a list of symbols.
    Returns a dictionary mapping symbol to percentage change, or None if error.
    """
    performance_data = {}
    for symbol in symbols:
        change = get_finnhub_quote(symbol)
        if change is not None:
            performance_data[symbol] = change
        time.sleep(0.5) # Adhere to API rate limits (e.g., 60 calls/minute on free tier)
    return performance_data

def calculate_stats(percentages_list):
    """Calculates mean and variance for a list of percentages."""
    if not percentages_list:
        return {'mean': 0.0, 'variance': 0.0}
    
    mean_val = np.mean(percentages_list)
    variance_val = np.var(percentages_list) # Use np.var for population variance
    
    return {'mean': mean_val, 'variance': variance_val}

def plot_category_stats(categories_data, metric_name, title, filename, color='skyblue'):
    """
    Plots a bar chart for category-wise statistics (mean or variance).
    
    Args:
        categories_data (dict): A dictionary where keys are category names (str)
                                and values are the metric values (float).
        metric_name (str): The name of the metric being plotted (e.g., 'Mean', 'Variance').
        title (str): The title of the plot.
        filename (str): The name of the file to save the plot.
        color (str): Color of the bars.
    """
    category_labels = list(categories_data.keys())
    metric_values = list(categories_data.values())

    num_categories = len(category_labels)
    # Adjust figure height dynamically, especially useful for more categories or longer labels
    dynamic_height = max(6, num_categories * 0.8) 

    fig, ax = plt.subplots(figsize=(10, dynamic_height))

    ax.bar(category_labels, metric_values, color=color)

    ax.set_xlabel('Stock Categories', fontsize=12)
    ax.set_ylabel(f'{metric_name} Percentage (%)', fontsize=12)
    ax.set_title(title, fontsize=14)

    plt.xticks(rotation=0) # Categories are few, so no rotation needed
    
    # Add labels on top of bars
    for i, value in enumerate(metric_values):
        ax.text(i, value + (0.5 if value >= 0 else -1.0), f'{value:.2f}', 
                ha='center', va='bottom' if value >= 0 else 'top', fontsize=10, color='gray')

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust y-limits to encompass both positive and negative values correctly
    if metric_values:
        min_val = min(metric_values)
        max_val = max(metric_values)
        padding = (max_val - min_val) * 0.1 if (max_val - min_val) != 0 else 1.0
        ax.set_ylim(min_val - padding, max_val + padding)
    else:
        ax.set_ylim(-1, 1) # Default range for empty data

    plt.tight_layout()
    plt.savefig(filename)
    plt.close(fig) # Close the figure to free up memory

def plot_combined_category_stats(mean_data, variance_data, title, filename):
    """
    Plots a grouped bar chart showing mean and variance for categories.
    
    Args:
        mean_data (dict): Dictionary of category means.
        variance_data (dict): Dictionary of category variances.
        title (str): Title of the plot.
        filename (str): Name of the file to save the plot.
    """
    categories = list(mean_data.keys())
    means = list(mean_data.values())
    variances = list(variance_data.values())

    num_categories = len(categories)
    bar_width = 0.35 # Width of each bar
    index = np.arange(num_categories) # x-axis locations for the categories

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting Mean bars
    rects1 = ax.bar(index - bar_width/2, means, bar_width, label='Mean', color='teal')

    # Plotting Variance bars
    rects2 = ax.bar(index + bar_width/2, variances, bar_width, label='Variance', color='purple')

    ax.set_xlabel('Stock Categories', fontsize=12)
    ax.set_ylabel('Percentage Value (%)', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.set_xticks(index)
    ax.set_xticklabels(categories)
    ax.legend()

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust y-limits to fit all values from both mean and variance
    all_values = means + variances
    if all_values:
        min_val = min(all_values)
        max_val = max(all_values)
        padding = (max_val - min_val) * 0.1 if (max_val - min_val) != 0 else 1.0
        ax.set_ylim(min_val - padding, max_val + padding)
    else:
        ax.set_ylim(-1, 1) # Default range for empty data

    plt.tight_layout()
    plt.savefig(filename)
    plt.close(fig)

if __name__ == "__main__":
    # Define stock symbols for each category
    tech_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ORCL', 'IBM', 'INTC', 'AMD']
    medtech_symbols = ['ABT', 'MDT', 'ISRG', 'SYK', 'BDX', 'BSX', 'DHR', 'EW', 'RMD', 'DXCM']
    finance_symbols = ['JPM', 'BAC', 'WFC', 'V', 'MA', 'GS', 'MS', 'C', 'SCHW', 'PYPL']

    if API_KEY == 'd0pnf21r01qgccua7rl0d0pnf21r01qgccua7rlg':
        print("WARNING: Using a dummy API key. Live data fetching might fail. Please replace with your actual Finnhub API key.")
        # For demonstration purposes with dummy data if API key is not valid
        tech_performance = {'AAPL': 0.5, 'MSFT': 1.2, 'GOOGL': 0.8, 'AMZN': 2.0, 'TSLA': -1.5, 'META': 0.3, 'NVDA': 2.5, 'NFLX': -0.7, 'ORCL': 0.1, 'IBM': 0.6, 'INTC': -0.2, 'AMD': 1.0}
        medtech_performance = {'ABT': 0.7, 'MDT': 0.2, 'ISRG': 1.1, 'SYK': -0.3, 'BDX': 0.9, 'BSX': 0.4, 'DHR': 1.5, 'EW': -0.1, 'RMD': 0.6, 'DXCM': 1.2}
        finance_performance = {'JPM': 0.3, 'BAC': 0.1, 'WFC': 0.5, 'V': 0.8, 'MA': 1.0, 'GS': -0.2, 'MS': 0.4, 'C': 0.0, 'SCHW': 0.7, 'PYPL': 0.9}
        print("Using dummy data for plotting.")
    else:
        print("Fetching data for Tech Stocks...")
        tech_performance = get_performance_data(tech_symbols)
        print("Fetching data for MedTech Companies...")
        medtech_performance = get_performance_data(medtech_symbols)
        print("Fetching data for Finance Companies...")
        finance_performance = get_performance_data(finance_symbols)
        print("Live data fetched.")

    # Extract lists of percentages for each category
    tech_percentages = list(tech_performance.values())
    medtech_percentages = list(medtech_performance.values())
    finance_percentages = list(finance_performance.values())

    # Calculate mean and variance for each category
    tech_stats = calculate_stats(tech_percentages)
    medtech_stats = calculate_stats(medtech_percentages)
    finance_stats = calculate_stats(finance_percentages)

    # Prepare data for Mean plot
    mean_data_for_plot = {
        'Tech': tech_stats['mean'],
        'MedTech': medtech_stats['mean'],
        'Finance': finance_stats['mean']
    }

    # Prepare data for Variance plot
    variance_data_for_plot = {
        'Tech': tech_stats['variance'],
        'MedTech': medtech_stats['variance'],
        'Finance': finance_stats['variance']
    }
    
    # Get the current date for the plot title
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    # Generate and save the combined Mean and Variance plot
    plot_combined_category_stats(
        mean_data_for_plot, 
        variance_data_for_plot, 
        f'Performance ({current_date}): Mean & Variance by Category', # Updated title
        'combined_category_performance.png'
    )
    print("Generated combined_category_performance.png")
