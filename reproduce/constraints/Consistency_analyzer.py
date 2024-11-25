import os
import pandas as pd
import numpy as np
import itertools
from scipy.stats import entropy

# get anwers from csv files
def get_csv_answers(folder_name):
    folder_path = f"./Results/ChatGPT answers/{folder_name}"
    output_folder = "./Results/ChatGPT answers/Analysis/Consistency"

    print(f"setting = {setting}.")
    print("1 = with image, 0 = without image")

    if not os.path.exists(folder_path):
        print(f"The folder '{folder_name}' does not exist.")
        return
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in '{folder_name}'.")
        return
    
    # Initialize DataFrame to store analysis results
    combined_analysis_df = pd.DataFrame()
    
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        print(f"Analyzing {file_path}:")
        
        # Load CSV file into pandas DataFrame
        df = pd.read_csv(file_path)
        
        # Get task_id, task_name columns (if not already stored)
        if combined_analysis_df.empty:
            task_info = df[['task_id', 'task_name']].copy()
            combined_analysis_df = task_info
        
        # Get Correct(1) / Wrong(0) columns and rename them with file name (without .csv extension)
        file_name = os.path.splitext(csv_file)[0]  # Remove .csv extension
        correct_wrong_cols = df.filter(regex='Correct\(1\) / Wrong\(0\)')
        correct_wrong_cols.columns = [f'{file_name}' for _ in range(len(correct_wrong_cols.columns))]
        
        # Concatenate correct_wrong_cols with combined_analysis_df
        combined_analysis_df = pd.concat([combined_analysis_df, correct_wrong_cols], axis=1)
    
    # Save combined analysis results to CSV
    output_file = os.path.join(output_folder, f"{folder_name}_consistency.csv")
    file_name = output_file
    combined_analysis_df.to_csv(output_file, index=False)
    print(f"Combined analysis results saved to {output_file}")
    
# analyze the answers
def analyze_csv_file(file_name):
    # Set the current directory as the base directory for file paths
    current_dir = os.path.dirname(__file__) if __file__ is not None else "."
    # Move to the directory where the file exists
    file_path = os.path.abspath(os.path.join(current_dir, "Results", "ChatGPT answers", "Analysis", "Consistency", f"{file_name}.csv"))
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File '{file_name}.csv' not found.")
        return
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Add the '# correct' column to the original DataFrame
    df['# correct'] = df.drop(columns=['task_id', 'task_name']).sum(axis=1)
    
    # Save the result to the original CSV file with the additional column
    df.to_csv(file_path, index=False)
    
    # Return the path to the original CSV file (unchanged)
    return file_path

# Function to calculate Krippendorff's Alpha
def krippendorff_alpha(data: np.ndarray) -> float:
    """
    Calculate Krippendorff's alpha for reliability of coding.
    
    :param data: numpy array where each row represents a coder and each column an item
    :return: Krippendorff's alpha
    """
    data = np.ma.masked_invalid(data)  # Handle NaN and inf values
    n_coders, n_items = data.shape
    
    if n_items == 0:
        raise ValueError("No items to compare.")
    
    # Count the number of coders for each item
    n_coders_per_item = np.sum(~data.mask, axis=0)
    
    # Create coincidence matrix
    coincidence_matrix = np.zeros((2, 2))
    for i in range(n_items):
        item_data = data[:, i].compressed()  # Remove masked values
        if len(item_data) < 2:
            continue  # Skip items with less than 2 ratings
        item_data = item_data[:, np.newaxis]
        coincidence = (item_data == item_data.T).astype(int)
        np.fill_diagonal(coincidence, 0)
        coincidence_matrix += coincidence
    
    # Calculate observed disagreement
    n_total = np.sum(coincidence_matrix)
    o = np.sum(coincidence_matrix[0, 1] + coincidence_matrix[1, 0]) / n_total
    
    # Calculate expected disagreement
    p = np.sum(coincidence_matrix, axis=1) / n_total
    e = 2 * p[0] * p[1]
    
    # Compute alpha
    if e == 0:
        return 1.0  # Perfect agreement
    else:
        return 1.0 - o / e
    
def calculate_krippendoff_alpha_csv(file_name):
    # Set the current directory as the base directory for file paths
    current_dir = os.path.dirname(__file__) if __file__ is not None else "."
    # Move to the directory where the file exists
    file_path = os.path.abspath(os.path.join(current_dir, "Results", "ChatGPT answers", "Analysis", "Consistency", f"{file_name}.csv"))
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File '{file_name}.csv' not found.")
        return
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Extract the relevant columns for consistency analysis
    relevant_columns = [col for col in df.columns if col not in ['task_id', 'task_name', '# correct']]
    consistency_df = df[relevant_columns]
    
    # Calculate Krippendorff's Alpha value
    alpha_value = krippendorff_alpha(consistency_df.values)
    print(f"Krippendorff's Alpha value: {alpha_value}")

    # Return the path to the original CSV file (unchanged)
    return file_path


# folder setting
setting = 0     # 1 = with image, 0 = without image

# file name variable
file_name = ""

if setting == 1:
    folder_name = "with_image"
    get_csv_answers(folder_name)
    file_name = f"{folder_name}_consistency"
    analyze_csv_file(file_name)
    calculate_krippendoff_alpha_csv(file_name)
else:
    folder_name = "without_image"
    get_csv_answers(folder_name)
    file_name = f"{folder_name}_consistency"
    analyze_csv_file(file_name)
    calculate_krippendoff_alpha_csv(file_name)