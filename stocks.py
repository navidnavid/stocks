import requests
import time
import matplotlib.pyplot as plt
import numpy as np

API_KEY = 'd0pnf21r01qgccua7rl0d0pnf21r01qgccua7rlg'

def get_finnhub_quote(symbol):
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}'
    r = requests.get(url)
    data = r.json()
    
    try:
        current = data['c']
        previous = data['pc']
        if current and previous:
            change_percent = ((current - previous) / previous) * 100
            return change_percent
        return None
    except Exception as e:
        print(f"Error for {symbol}: {e}")
        return None

def get_top_finnhub(symbols):
    results = []
    for symbol in symbols:
        change = get_finnhub_quote(symbol)
        if change is not None:
            results.append((symbol, change))
        time.sleep(0.5)
    
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def plot_stock_percentages(data_dict, title, filename):
    categories = list(data_dict.keys())
    percentages = list(data_dict.values())

    num_categories = len(categories)
    base_height_per_item = 0.7
    min_height = 6

    dynamic_height = max(min_height, num_categories * base_height_per_item)

    fig, ax = plt.subplots(figsize=(10, dynamic_height))

    ax.bar(categories, percentages, color='skyblue')

    ax.set_xlabel('Stock Symbols')
    ax.set_ylabel('Percentage Change (%)')
    ax.set_title(title)

    plt.xticks(rotation=45, ha='right')

    for i, value in enumerate(percentages):
        ax.text(i, value + 0.5, f'{value:.1f}%', ha='center', va='bottom', fontsize=10, color='gray')

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust y-limits dynamically to fit both positive and negative percentages
    min_percentage = min(0, min(percentages) * 1.1 if percentages else 0)
    max_percentage = max(0, max(percentages) * 1.1 if percentages else 0)
    if min_percentage == 0 and max_percentage == 0:
        ax.set_ylim(-1, 1) # Default small range if all percentages are zero
    else:
        ax.set_ylim(min_percentage, max_percentage)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close(fig)

if __name__ == "__main__":
    symbols1 = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ORCL', 'IBM', 'INTC', 'AMD']
    symbols2 = ['ABT', 'MDT', 'ISRG', 'SYK', 'BDX', 'BSX', 'DHR', 'EW', 'RMD', 'DXCM']
    symbols3 = ['JPM', 'BAC', 'WFC', 'V', 'MA', 'GS', 'MS', 'C', 'SCHW', 'PYPL']

    if API_KEY == 'YOUR_FINNHUB_API_KEY':
        print("Please replace 'YOUR_FINNHub_API_KEY' with your actual Finnhub API key to run this example.")
    else:
        print("Fetching data for Tech Stocks...")
        tech_data = get_top_finnhub(symbols1)
        tech_dict = {symbol: percent for symbol, percent in tech_data}
        plot_stock_percentages(tech_dict, 'Daily Performance: US Tech Stocks', 'tech_stock_performance.png')
        print("Generated tech_stock_performance.png")

        print("Fetching data for MedTech Companies...")
        medtech_data = get_top_finnhub(symbols2)
        medtech_dict = {symbol: percent for symbol, percent in medtech_data}
        plot_stock_percentages(medtech_dict, 'Daily Performance: MedTech Companies', 'medtech_stock_performance.png')
        print("Generated medtech_stock_performance.png")

        print("Fetching data for Finance Companies...")
        finance_data = get_top_finnhub(symbols3)
        finance_dict = {symbol: percent for symbol, percent in finance_data}
        plot_stock_percentages(finance_dict, 'Daily Performance: Finance Companies', 'finance_stock_performance.png')
        print("Generated finance_stock_performance.png")

# company_names = {
#     # Original Tech Stocks
#     'AAPL': 'Apple Inc.',
#     'MSFT': 'Microsoft Corporation',
#     'GOOGL': 'Alphabet Inc. (Class A)',
#     'AMZN': 'Amazon.com, Inc.',
#     'TSLA': 'Tesla, Inc.',
#     'META': 'Meta Platforms, Inc.',
#     'NVDA': 'NVIDIA Corporation',
#     'NFLX': 'Netflix, Inc.',
#     'ORCL': 'Oracle Corporation',
#     'IBM': 'International Business Machines Corporation',
#     'INTC': 'Intel Corporation',
#     'AMD': 'Advanced Micro Devices, Inc.',

#     # MedTech Companies
#     'ABT': 'Abbott Laboratories',
#     'MDT': 'Medtronic PLC',
#     'ISRG': 'Intuitive Surgical, Inc.',
#     'SYK': 'Stryker Corporation',
#     'BDX': 'Becton, Dickinson and Company (BD)',
#     'BSX': 'Boston Scientific Corporation',
#     'DHR': 'Danaher Corporation',
#     'EW': 'Edwards Lifesciences Corporation',
#     'RMD': 'ResMed Inc.',
#     'DXCM': 'DexCom, Inc.',

#     # Finance Companies
#     'JPM': 'JPMorgan Chase & Co.',
#     'BAC': 'Bank of America Corporation',
#     'WFC': 'Wells Fargo & Company',
#     'V': 'Visa Inc.',
#     'MA': 'Mastercard Incorporated',
#     'GS': 'The Goldman Sachs Group, Inc.',
#     'MS': 'Morgan Stanley',
#     'C': 'Citigroup Inc.',
#     'SCHW': 'The Charles Schwab Corporation',
#     'PYPL': 'PayPal Holdings, Inc.'
# }