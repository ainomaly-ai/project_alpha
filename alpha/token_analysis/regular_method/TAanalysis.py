import pickle
import pandas as pd
import talib
import matplotlib.pyplot as plt

# Load the dataset from a pickle file
def load_dataset(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

# Function to plot price and indicators
def plot_data(data, signals):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 8), sharex=True)
    
    # Plot price and Bollinger Bands
    ax1.plot(data['priceUsd'], label='Price', color='blue')
    ax1.plot(data['upper_band'], label='Upper Band', color='orange', linestyle='--')
    ax1.plot(data['lower_band'], label='Lower Band', color='orange', linestyle='--')
    ax1.scatter(data.index[signals], data['priceUsd'][signals], 
                color='red', marker='^', label='Breakout Signal', zorder=5)
    ax1.set_title('Price and Bollinger Bands')
    ax1.legend()
    
    # Plot MACD
    ax2.plot(data['macd'], label='MACD', color='blue')
    ax2.plot(data['macd_signal'], label='Signal Line', color='red', linestyle='--')
    ax2.bar(data.index, data['macd_histogram'], label='Histogram', color='gray', alpha=0.4)
    ax2.set_title('MACD')
    ax2.legend()
    
    # Plot RSI
    ax3.plot(data['rsi_filtered'], label='RSI', color='purple')
    ax3.axhline(70, color='red', linestyle='--', label='Overbought')
    ax3.axhline(30, color='green', linestyle='--', label='Oversold')
    ax3.set_title('RSI')
    ax3.legend()
    
    plt.tight_layout()
    plt.show()

def calculate_indicators(data):
    df = data.copy()
    
    # Calculate indicators
    df['upper_band'], df['middle_band'], df['lower_band'] = talib.BBANDS(df['priceUsd'], timeperiod=20)
    df['macd'], df['macd_signal'], df['macd_histogram'] = talib.MACD(df['priceUsd'], fastperiod=12, slowperiod=26, signalperiod=9)
    
    df['rsi'] = talib.RSI(df['priceUsd'] / df['priceUsd'].max(), timeperiod=40)
    df['rsi_filtered'] = df['rsi'] >= 60
    print(any(df["rsi_filtered"]))
    
    return df

def bollinger_band_breakout(data):
    signals = []
    cooldown_period = 5
    last_signal_index = -100
    
    for i in range(25, len(data)):
        if i - last_signal_index < cooldown_period:
            continue

        price = data['priceUsd'][i]
        upper_band = data['upper_band'][i]
        macd_hist = data['macd_histogram'][i]
        rsi_flag = data['rsi_filtered'][i]
        recent_std = data['priceUsd'][i-20:i].std()

        # Add a volatility filter
        if recent_std / price < 0.005:  # Adjust threshold based on your token's price scale
            continue

        if price > upper_band and rsi_flag == 1 and macd_hist > 1e-11:
            signals.append(i)
            last_signal_index = i
    
    return signals


# Main function to execute the strategy
def main(file_path):
    data = load_dataset(file_path)
    # print(data["priceUsd"].head().to_string())
    sorted_data = data[data["token"] == "ECMYTGjvXWR3mb5RFEh3F1mAqFBe5EEe53A2n1F1sbpg"]
    # print(sorted_data["priceUsd"])
    data = calculate_indicators(sorted_data)
    signals = bollinger_band_breakout(data)
    # print(f"Bollinger Band Breakout signals at indices: {signals}")
    # Plot the data with signals
    plot_data(data, signals)

# Example usage
file_path = 'alpha/data/data.pkl'
main(file_path)