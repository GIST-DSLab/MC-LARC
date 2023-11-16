import pandas as pd
import json
import os

# Read the CSV file
df = pd.read_csv('filtered_LARC_with_input_output.csv')

# Create a dictionary to store the results
result = {"training": []}

# Iterate through each row of the CSV file
for index, row in df.iterrows():
    # Create a dictionary in the format of the training data
    training_data = {
        "task_id": str(index),
        "task_name": row['task_name'],
        "description_input": row['description_input'],
        "description_output": row['description_output']
    }
    
    # Add to the result dictionary
    result["training"].append(training_data)
    
    # Find the JSON file with the same task_name
    task_name = row['task_name']
    training_files = [f for f in os.listdir('training') if f.endswith('.json') and task_name in f]
    
    # Read the JSON file and repeat the training data for the number of times equal to the length of the 'train' data
    for file in training_files:
        with open(os.path.join('training', file), 'r') as f:
            training_json = json.load(f)
            for _ in range(len(training_json['train']) - 1):
                result["training"].append(training_data)

# Save the results to a JSON file
with open('LARC_with_input_output.json', 'w') as f:
    json.dump(result, f, indent=4)

print('Conversion complete! Check output.json file.')
