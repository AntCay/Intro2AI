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

def plot_histograms(all_results, images_folder):
    """
    Plots:
    1. A single histogram of total wins for each algorithm (shows+ saves).
    2. A single figure with subplots for move counts of each algorithm.
    """
    win_distribution = {}
    move_counts = {}

    for rows in all_results.values():
        for row in rows:
            winner = row['winner']
            moves_count_str = row['moves_count']
            
            # Skip invalid moves_count values
            if not moves_count_str.isdigit():
                print(f"Skipping invalid moves_count value: {moves_count_str}")
                continue

            moves_count = int(moves_count_str)

            if winner not in win_distribution:
                win_distribution[winner] = 0
                move_counts[winner] = []

            win_distribution[winner] += 1
            move_counts[winner].append(moves_count)

    # Sort the distributions alphabetically
    win_distribution = dict(sorted(win_distribution.items()))
    move_counts = dict(sorted(move_counts.items()))

    # Plot histogram of wins
    plt.figure(figsize=(10, 5))
    plt.bar(win_distribution.keys(), win_distribution.values())
    plt.xlabel('Algorithm')
    plt.ylabel('Number of Wins')
    plt.title('Win Distribution Across All Files')
    plt.savefig(os.path.join(images_folder, 'win_distribution.png'))
    plt.show()

    # Create a single figure with subplots for move counts (one subplot per algorithm)
    num_algorithms = len(move_counts)
    if num_algorithms == 0:
        print("No valid move counts to plot.")
        return

    # Determine the number of rows and columns for the subplots
    num_cols = int(num_algorithms**0.5)
    num_rows = (num_algorithms + num_cols - 1) // num_cols

    fig, axes = plt.subplots(
        nrows=num_rows,
        ncols=num_cols,
        figsize=(5 * num_cols, 5 * num_rows),
        squeeze=False
    )

    # Plot a histogram on each subplot
    for idx, (algorithm, counts) in enumerate(move_counts.items()):
        row = idx // num_cols
        col = idx % num_cols
        ax = axes[row, col]
        ax.hist(counts, bins=20, alpha=0.75)
        ax.set_xlabel('Move Count')
        ax.set_ylabel('Number of wins')
        ax.set_title(f'{algorithm}')

    # Hide any unused subplots
    for idx in range(num_algorithms, num_rows * num_cols):
        fig.delaxes(axes.flatten()[idx])

    plt.tight_layout()
    plt.savefig(os.path.join(images_folder, 'move_count_distribution_subplots.png'))
    plt.show()

def main():
    # Adjust this path to point to your "result" folder
    result_folder = r"c:\Workspace\Git\Master repos\Intro2AI\result"
    images_folder = os.path.join(result_folder, 'images')

    # Create images folder if it doesn't exist
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Analyze results
    all_results = analyze_results(result_folder)

    # Plot histograms
    plot_histograms(all_results, images_folder)

if __name__ == "__main__":
    main()
