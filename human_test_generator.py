import os
import pandas as pd
import shutil
import glob

# Read the CSV file
df = pd.read_csv('shuffled_output_description.csv', encoding='ISO-8859-1', dtype=str)

# Read the filtered CSV file
filtered_df = pd.read_csv('filtered_LARC_with_input_output.csv', encoding='ISO-8859-1', dtype=str)

# Process each row
for index, row in df.iterrows():
    task_id = row['task_id']
    task_name = row['task_name']
    # Getting the shuffled descriptions
    descriptions = [row[f'shuffled_description{i}'] for i in range(1, 6)]
    
    # Find the corresponding description_input for the task_id
    description_input = filtered_df.loc[filtered_df['task_id'] == str(task_id), 'description_input'].values[0]
    
    # Create a folder named after the task_id inside the 'Prompt' folder
    prompt_folder = "Prompt_human"
    if not os.path.exists(prompt_folder):
        os.makedirs(prompt_folder)
    task_folder = os.path.join(prompt_folder, str(task_id))
    if not os.path.exists(task_folder):
        os.makedirs(task_folder)
    
    # Copy the image file
    image_folder = 'training_input_output_pair_image'
    for image_filepath in glob.glob(os.path.join(image_folder, f"*{task_name}*")):
        shutil.copy(image_filepath, task_folder)
    
    # Write the text file
    txt_filename = f"{task_name}_prompt.txt"
    txt_filepath = os.path.join(task_folder, txt_filename)
    with open(txt_filepath, 'w', encoding='utf-8') as f:
        # f.write("- Environment Explanation:\n")
        # f.write("The given images consist of pairs of input and output images. The crucial aspect here is that these image pairs follow a common rule, and accurately inferring this common rule is the key.\n\n")
        # f.write("Upon closely examining the given images, each image is structured as an NxM grid. (N and M are natural numbers.) There are a total of 10 pixel colors: black, blue, red, cyan, brown, pink, gray, yellow, and green.\n\n")
        # f.write("I will provide you with several pairs of input-output images that adhere to a common rule.\n\n")
        f.write("Here are the options:\n")
        for i, description in enumerate(descriptions, start=1):
            f.write(f"{i}. {description}\n\n")
        
        # f.write("- Things you have to do:\n")
        # f.write("Your task is to choose the option among the given choices that most accurately describes the relationship between the given images.\n")
        # f.write("Please choose the most accurate option among the given choices numbered 1 through 5. Please respond with option [number]. Do not say anything else.\n\n")
        
        # f.write("- Hint:\n")
        # for i, description in enumerate(description_input, start=1):
        #     f.write(f"{description}")


