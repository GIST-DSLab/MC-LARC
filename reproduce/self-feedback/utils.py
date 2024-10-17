import os
import pandas as pd
import datetime
import random
import base64
from mimetypes import guess_type

def local_image_to_data_url(image_path):
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{base64_encoded_data}"

def select_random_images_and_convert_to_data_urls(folder_path, num_images=4):
    try:
        images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png')]
        if not images:
            print(f"No images found in the folder: {folder_path}")
        selected_images = random.sample(images, min(len(images), num_images))
        data_urls = [local_image_to_data_url(image) for image in selected_images]
        return data_urls
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []

def select_constraints(messages_dict):
    final_messages = []
    selected_keys = []

    def add_message_set(message_key):
        nonlocal final_messages, selected_keys
        user_input = input(f"Add {message_key}? (y/n): ").strip().lower()
        if user_input == 'y':
            final_messages += messages_dict[message_key]
            selected_keys.append(message_key[0])

    for key in messages_dict.keys():
        add_message_set(key)

    if not os.path.exists('results/initial_MC-LARC'):
        os.makedirs('results/initial_MC-LARC')

    filename = f"results/initial_MC-LARC/constraints_{''.join(selected_keys)}.csv"
    return final_messages, filename

def log_wrong_format_error(task_id, response_text):
    log_dir = 'ChatGPT4_error_log'
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, 'Wrong_format_error_log.txt'), 'a', newline='\n', encoding='utf-8') as file:
        WF_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f'{task_id}: {response_text}: {WF_current_time}\n')

def log_openai_error(task_id, error):
    log_dir = 'ChatGPT4_error_log'
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, 'Openai_error_log.txt'), 'a', newline='\n', encoding='utf-8') as file:
        Openai_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f'{task_id}: {error}\n')
        file.write(f'{Openai_current_time}\n')

def read_csv_with_different_encodings(file):
    encodings = ['utf-8', 'ISO-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            return pd.read_csv(file, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Could not decode the file {file} with available encodings")

def shuffle_responses_in_csv(directory):
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    
    shuffled_dir = os.path.join(directory, 'shuffled')
    os.makedirs(shuffled_dir, exist_ok=True)
    
    for file in csv_files:
        df = read_csv_with_different_encodings(file)

        columns_to_shuffle = ["description_output", "ChatGPT Response1", "ChatGPT Response2", "ChatGPT Response3", "ChatGPT Response4"]
        shuffled_columns = ["shuffled_options1", "shuffled_options2", "shuffled_options3", "shuffled_options4", "shuffled_options5"]
        additional_columns = ["task_id", "task_name"]
        
        # Create a DataFrame to hold shuffled results
        shuffled_df = pd.DataFrame(columns=additional_columns + shuffled_columns + ["answers"])

        for index, row in df.iterrows():
            responses = row[columns_to_shuffle].tolist()
            random.shuffle(responses)
            shuffled_data = {col: responses[i] for i, col in enumerate(shuffled_columns)}
            shuffled_data["answers"] = responses.index(row["description_output"]) + 1
            shuffled_data["task_id"] = row["task_id"]
            shuffled_data["task_name"] = row["task_name"]
            shuffled_df = pd.concat([shuffled_df, pd.DataFrame([shuffled_data])], ignore_index=True)
        
        shuffled_file = os.path.join(shuffled_dir, os.path.basename(file).replace('.csv', '_shuffled.csv'))
        shuffled_df.to_csv(shuffled_file, index=False)
        print(f"Shuffled responses saved to: {shuffled_file}")
