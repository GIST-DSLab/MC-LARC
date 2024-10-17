import os
import re

# Specify the path to the 'Prompt' folder
prompt_folder = 'MC-LARC/Prompt'

# Create or open the 'prompt_answer.txt' file
with open('MC-LARC/prompt_answer_with_hint.txt', 'w') as answer_file:
    # Loop through folders from 0 to 399
    for folder_number in range(400):
        folder_name = str(folder_number)
        txt_file_path = os.path.join(prompt_folder, folder_name, f'{folder_name}_hint.txt')
        
        # Check if the '0.txt' file exists in the current folder
        if os.path.exists(txt_file_path):
            # Read the content of the '0.txt' file
            with open(txt_file_path, 'r') as txt_file:
                file_contents = txt_file.read()
            
            # Use regular expressions to extract numeric values
            numeric_values = re.findall(r'\d+', file_contents)
            
            # Convert the list of numeric values to a comma-separated string
            numeric_values_str = ', '.join(numeric_values)
            
            # Write the numeric values to 'prompt_answer.txt' with the specified format
            answer_file.write(f'task_{folder_number}: {numeric_values_str}\n')
