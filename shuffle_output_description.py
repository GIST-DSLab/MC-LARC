import pandas as pd
import random

# Read the CSV file
df = pd.read_csv('MC-LARC/MC-LARC_description_output.csv', encoding='ISO-8859-1', dtype=str)

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
shuffled_df.to_csv('MC-LARC/shuffled_output_description.csv', index=False)