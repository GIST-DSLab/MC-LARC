import json
import os
import csv
from collections import Counter

def analyze_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    train_data = data['train']
    
    total_input_numbers = 0
    total_input_types = 0
    total_output_numbers = 0
    total_output_types = 0
    
    for item in train_data:
        input_matrix = item['input']
        output_matrix = item['output']
        
        # Flatten the matrices
        input_flat = [num for row in input_matrix for num in row]
        output_flat = [num for row in output_matrix for num in row]
        
        # Count numbers and types
        input_counter = Counter(input_flat)
        output_counter = Counter(output_flat)
        
        total_input_numbers += sum(input_counter.values())
        total_input_types += len(input_counter)
        total_output_numbers += sum(output_counter.values())
        total_output_types += len(output_counter)
    
    num_of_inputs = len(train_data)
    num_of_outputs = len(train_data)
    
    # Calculate averages
    average_input_numbers = total_input_numbers / num_of_inputs
    average_input_types = total_input_types / num_of_inputs
    average_output_numbers = total_output_numbers / num_of_outputs
    average_output_types = total_output_types / num_of_outputs
    
    return {
        'file_name': os.path.splitext(os.path.basename(file_path))[0],  # Remove the .json extension
        'num_of_input': num_of_inputs,
        'num_of_output': num_of_outputs,
        'average_input_numbers': average_input_numbers,
        'average_input_types': average_input_types,
        'average_output_numbers': average_output_numbers,
        'average_output_types': average_output_types
    }

def save_to_csv(results, output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file_name', 'num_of_input', 'num_of_output', 'average_input_numbers', 'average_input_types', 'average_output_numbers', 'average_output_types']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def main():
    # Define the directory containing JSON files
    directory_path = r"C:\Users\oollccddss\Desktop\Work\MC-LARC\MC-LARC-EMNLP.ver\original_data\training"
    output_csv_path = os.path.join(r"C:\Users\oollccddss\Desktop\Work\MC-LARC\MC-LARC-EMNLP.ver\baseline statistics", 'analysis_results.csv')
    
    results = []
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            result = analyze_json_file(file_path)
            results.append(result)
    
    # Save all results to a CSV file
    save_to_csv(results, output_csv_path)

if __name__ == "__main__":
    main()
