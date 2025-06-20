import json
import os
from datetime import datetime
import matplotlib
matplotlib.rcParams['toolbar'] = 'none'
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import MaxNLocator

# Path to the reward log file
JSON_PATH = r"C:\Users\gmelk\OneDrive\Desktop\Trading & Coding\Python Projects\CryptoFaucetDrainer\reward_log.json"


def load_rewards(json_path=JSON_PATH):
    """Load and parse the rewards JSON log."""
    if not os.path.exists(json_path):
        print("⚠️ No reward log found.")
        return []

    with open(json_path, "r") as file:
        data = json.load(file)

    for entry in data:
        entry["timestamp"] = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        entry["reward"] = float(entry["reward"])

    return data


def show_latest_rewards(data, count=10):
    """Print recent rewards with full decimal precision."""
    print(f"\n📜 Last {count} Rewards:")
    for entry in data[-count:]:
        print(f"🕒 {entry['timestamp']} → 💰 {entry['reward']:.8f} BTC")



def show_total_btc(data):
    """Calculate and display total BTC earned."""
    total_btc = sum(entry["reward"] for entry in data)
    print(f"\n📊 Total BTC Earned: {total_btc:.8f} BTC")
    return total_btc


def plot_rewards(data):
    # Parse timestamps and rewards
    timestamps = [datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S") if isinstance(entry["timestamp"], str) else entry["timestamp"] for entry in data]
    rewards = [float(entry["reward"]) for entry in data]

    # Compute cumulative sum of rewards
    cumulative_rewards = []
    total = 0
    for r in rewards:
        total += r
        cumulative_rewards.append(total)

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cumulative_rewards, marker='o', linestyle='-')
    plt.title("Rewards Balance Over Time")
    plt.xlabel("Time")
    plt.ylabel("Total BTC Earned")
    plt.grid(True)

    # Format y-axis with full decimal precision
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=15))
    plt.tight_layout()
    plt.show()


# If run directly from terminal
if __name__ == "__main__":
    rewards = load_rewards()
    if rewards:
        show_latest_rewards(rewards)
        show_total_btc(rewards)
        plot_rewards(rewards)
