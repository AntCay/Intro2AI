import os
import csv
import matplotlib.pyplot as plt


def read_csv(filepath):
    """
    Reads a CSV file and returns a list of dictionaries.
    Each dictionary represents a row in the CSV file.
    """
    with open(filepath, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def analyze_results(result_folder):
    """
    Reads all CSV files in the given folder and analyzes the results.
    """
    all_results = {}

    # Walk through the directory, find CSV files, and read them
    for filename in os.listdir(result_folder):
        if filename.lower().endswith(".csv"):
            full_path = os.path.join(result_folder, filename)
            csv_data = read_csv(full_path)
            all_results[filename] = csv_data

    return all_results

def plot_histogram(all_results):
    """
    Plots a histogram of the number of wins for each algorithm.
    """
    for fname, rows in all_results.items():
        win_distribution = {}

        for row in rows:
            winner = row['winner']
            if winner not in win_distribution:
                win_distribution[winner] = 0
            win_distribution[winner] += 1

        # Plot histogram
        plt.figure(figsize=(10, 5))
        plt.bar(win_distribution.keys(), win_distribution.values())
        plt.xlabel('Algorithm')
        plt.ylabel('Number of Wins')
        plt.title(f'Win Distribution for {fname}')
        plt.show()

# Adjust this path to point to your "result" folder
result_folder = r"c:\Workspace\Git\Master repos\Intro2AI\result"

# Analyze results
all_results = analyze_results(result_folder)

# Plot histogram
plot_histogram(all_results)
