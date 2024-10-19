import pandas as pd
import random
import os

# Function to shuffle the choices in a dataframe
def shuffle_choices(file_path, output_path):
    # Read the CSV file
    df = pd.read_csv(file_path, encoding='ISO-8859-1', dtype=str)

    # Initialize an empty list to store the shuffled data and answers
    shuffled_data = []

    # Iterate over each row
    for index, row in df.iterrows():
        # Create a list of choices
        choices = [row['description_output'], row['ChatGPT Response1'], row['ChatGPT Response2'], row['ChatGPT Response3'], row['ChatGPT Response4']]
        
        # Shuffle the order of the choices
        random.shuffle(choices)
        
        # Find the position of the correct answer (originally the description_output) in the shuffled list
        answer_index = choices.index(row['description_output']) + 1
        
        # Copy the row and update the choices
        shuffled_row = row.copy()
        shuffled_row[['description_output', 'ChatGPT Response1', 'ChatGPT Response2', 'ChatGPT Response3', 'ChatGPT Response4']] = choices
        shuffled_row['answer'] = answer_index  # Add the answer to the row
        
        # Append the shuffled row to the list
        shuffled_data.append(shuffled_row)

    # Create a new DataFrame from the shuffled data
    shuffled_df = pd.DataFrame(shuffled_data)

    # Rename columns
    new_column_names = {
        'description_output': 'shuffled_description1',
        'ChatGPT Response1': 'shuffled_description2',
        'ChatGPT Response2': 'shuffled_description3',
        'ChatGPT Response3': 'shuffled_description4',
        'ChatGPT Response4': 'shuffled_description5'
    }
    shuffled_df.rename(columns=new_column_names, inplace=True)

    # Save the DataFrame to a new CSV file
    shuffled_df.to_csv(output_path, index=False)

# File paths
base_path = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/constraints_results/"
shuffled_folder = base_path + "shuffled/"
input_files = [
    base_path + 'constraints_gcsotf.csv',
    base_path + 'constraints_cs.csv',
    base_path + 'constraints_gc.csv',
    base_path + 'constraints_gcs.csv',
    base_path + 'constraints_gcsf.csv',
    base_path + 'constraints_gs.csv'
]

output_files = [
    shuffled_folder + 'shuffled_constraints_gcsotf.csv',
    shuffled_folder + 'shuffled_constraints_cs.csv',
    shuffled_folder + 'shuffled_constraints_gc.csv',
    shuffled_folder + 'shuffled_constraints_gcs.csv',
    shuffled_folder + 'shuffled_constraints_gcsf.csv',
    shuffled_folder + 'shuffled_constraints_gs.csv'
]

# Create the shuffled folder if it doesn't exist
os.makedirs(shuffled_folder, exist_ok=True)

# Shuffle choices for each file
for input_file, output_file in zip(input_files, output_files):
    shuffle_choices(input_file, output_file)
