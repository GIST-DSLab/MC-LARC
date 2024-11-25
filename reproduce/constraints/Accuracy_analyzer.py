import os
import pandas as pd
import scipy.stats as stats

def analyze_csv_files(folder_name):
    folder_path = f"./Results/ChatGPT answers/{folder_name}"
    output_folder = "./Results/ChatGPT answers/Analysis/Accuracy"
    
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
    
    # Initialize list to store analysis results
    analysis_data = []
    
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        print(f"Analyzing {file_path}:")
        
        # Load CSV file into pandas DataFrame
        df = pd.read_csv(file_path)
        
        # Perform analysis
        total_entries = len(df)
        correct_entries = df['Correct(1) / Wrong(0)'].sum()
        accuracy = correct_entries / total_entries * 100 if total_entries > 0 else 0
        
        # Append analysis results to list
        analysis_data.append({'File': csv_file,
                              'Total Entries': total_entries,
                              'Correct Entries': correct_entries,
                              'Accuracy': accuracy})
    
    # Create DataFrame from analysis data
    analysis_df = pd.DataFrame(analysis_data)
    
    # Save analysis results to CSV
    output_file = os.path.join(output_folder, f"{folder_name}_accuracy.csv")
    analysis_df.to_csv(output_file, index=False)
    print(f"Analysis results saved to {output_file}")
    
def analyze_csv_statistics(file_name):
    # Set the current directory as the base directory for file paths
    current_dir = os.path.dirname(__file__) if __file__ is not None else "."
    # Move to the directory where the file exists
    file_path = os.path.abspath(os.path.join(current_dir, "Results", "ChatGPT answers", "Analysis", "Accuracy", f"{file_name}.csv"))
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File '{file_name}.csv' not found.")
        return
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Calculate statistical measures
    accuracy_mean = df['Accuracy'].mean()
    accuracy_variance = df['Accuracy'].var()
    accuracy_std_deviation = df['Accuracy'].std()
    
    # Calculate 95% confidence interval
    n = len(df)
    z_score = stats.norm.ppf(0.975)  # 95% confidence level
    margin_of_error = z_score * (accuracy_std_deviation / (n ** 0.5))
    confidence_interval_lower = accuracy_mean - margin_of_error
    confidence_interval_upper = accuracy_mean + margin_of_error
    
    # Create a DataFrame for statistical measures including confidence interval
    statistics_df = pd.DataFrame({
        'Acc. Mean': [accuracy_mean],
        'Acc. Var': [accuracy_variance],
        'Acc. Std': [accuracy_std_deviation],
        'Confidence Lower Bound': [confidence_interval_lower],
        'Confidence Upper Bound': [confidence_interval_upper]
    })
    
    # Print statistical measures
    print("Statistical Measures:")
    print(statistics_df)
    
    # Save the result to a new CSV file with the additional columns
    output_folder = os.path.join(current_dir, "Results", "ChatGPT answers", "Analysis", "Accuracy")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file_path = os.path.join(output_folder, f"{file_name}_analysis.csv")
    statistics_df.to_csv(output_file_path, index=False)
    print(f"Analysis results saved to {output_file_path}")
    
    # Return the path to the new CSV file
    return output_file_path
        

# folder setting
# 1 = with image, 0 = without image
setting = 1

# file name variable
file_name = ""

if setting == 1:
    folder_name = "with_image"
    analyze_csv_files(folder_name)
    file_name = f"{folder_name}_accuracy"
    analyze_csv_statistics(file_name)
else:
    folder_name = "without_image"
    analyze_csv_files(folder_name)
    file_name = f"{folder_name}_accuracy"
    analyze_csv_statistics(file_name)
    
