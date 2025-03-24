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
    plt.xticks(rotation=45)  # Rotate x-axis labels
    plt.tight_layout()       # Ensure everything fits
    plt.savefig(os.path.join(images_folder, 'win_distribution.png'))
    plt.show()

    # Create figures for move counts with a maximum of 6 subplots per figure
    algorithms = list(move_counts.items())
    total_algorithms = len(algorithms)
    chunk_size = 6

    for chunk_index in range(0, total_algorithms, chunk_size):
        chunk_algos = algorithms[chunk_index:chunk_index+chunk_size]
        current_chunk_size = len(chunk_algos)
        
        # Determine the layout: best to have up to 3 columns per row
        num_cols = min(3, current_chunk_size)
        num_rows = (current_chunk_size + num_cols - 1) // num_cols

        fig, axes = plt.subplots(
            nrows=num_rows,
            ncols=num_cols,
            figsize=(5 * num_cols, 5 * num_rows),
            squeeze=False
        )

        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        # Rotate x-axis labels for each subplot
        for ax_row in axes:
            for ax in ax_row:
                for label in ax.get_xticklabels():
                    label.set_rotation(45)

        # Plot a histogram on each subplot for the current chunk
        for idx, (algorithm, counts) in enumerate(chunk_algos):
            row = idx // num_cols
            col = idx % num_cols
            ax = axes[row, col]
            ax.hist(counts, bins=20, alpha=0.75)
            ax.set_xlabel('Move Count')
            ax.set_ylabel('Number of wins')
            ax.set_title(f'{algorithm}')

        # Hide any unused subplots in this figure
        total_subplots = num_rows * num_cols
        for idx in range(current_chunk_size, total_subplots):
            fig.delaxes(axes.flatten()[idx])

        fig.tight_layout()
        fig_filename = os.path.join(
            images_folder, f'move_count_distribution_subplots_{(chunk_index // chunk_size) + 1}.png'
        )
        plt.savefig(fig_filename)
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
