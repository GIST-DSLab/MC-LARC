from openai import AzureOpenAI
import csv
import pandas as pd
import random
import os
import datetime
import base64
from mimetypes import guess_type

# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

# Function to randomly select image files
def select_random_images_and_convert_to_data_urls(folder_path, num_images=4):
    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png')]
    selected_images = random.sample(images, min(len(images), num_images))
    data_urls = [local_image_to_data_url(image) for image in selected_images]
    return data_urls


# Results csv file
with open('Results/ChatGPT answers/ChatGPT4V_answer_no_image5.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["task_id", "task_name", "Correct answer", "ChatGPT4V answer", "Correct(1) / Wrong(0)"])

# Read revised input LARC and output LARC
df = pd.read_csv('original_data/filtered_LARC_with_input_output.csv')
        
task_ids = df['task_id']
task_names = df['task_name']
description_inputs = df['description_input']
description_outputs = df['description_output']


# Read shuffled descriptions
shuffled_df = pd.read_csv('revised_shuffled_MC-LARC_output2.csv')


# OpenAI API setting
api_base = "END-POINT"
api_key= "OPENAI-KEY"
api_version = 'MODEL-VERSION' # this might change in the future
deployment_name = 'DEPLOY-NAME'


client = AzureOpenAI(
    api_key=api_key,  
    api_version=api_version,
    base_url=f"{api_base}openai/deployments/{deployment_name}/extensions",
)

# Error list
openai_errors = []
wrong_format_errors = []
skip_errors = []

# Error numbers
numbers = [
    13, 275, 282
]




  # Examples, check the error_log.txt files


# for i in range(0, 400):     # For all descriptions,

for i in numbers:          # For error numberes,
    
    task_name = df.loc[df['task_id'] == i, 'task_name'].values[0]
    folder_path = f"training_IO_each_pair_folder_without_label/{task_name}.json"

     # Get shuffled descriptions for the current task_id
    shuffled_descriptions = shuffled_df.loc[shuffled_df['task_id'] == i, 
                                            ['shuffled_description1', 'shuffled_description2', 'shuffled_description3', 
                                             'shuffled_description4', 'shuffled_description5']].values[0]

    # for index, description in enumerate(shuffled_descriptions, start=1):
    #     print(f"{index}. {description} \n")

    
    if os.path.exists(folder_path):
        data_urls = select_random_images_and_convert_to_data_urls(folder_path)
        
        messages = [
            { "role": "system", "content": "You need to choose the best option among the provided five options." },
            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "select the most appropriate option among the provided options."
                }
            ]
            },
            { "role": "assistant", "content": [  
                { 
                    "type": "text", 
                    "text": "Here is the example: \n \
                            1. To make the output, you have to...change the color of the object in the single-color pattern. \n \
                            2. To make the output, you have to...move the unnecessary object in the right side. \n \
                            3. To make the output, you have to...add more objects in the rectangular boxes. \n \
                            4. To make the output, you have to...remove the objects in the input grids. \n \
                            5. To make the output, you have to...resize output grids, and then fill the grid with the single-color. \n\n \
                            If the correct answer among the five options is 2, your response would be: \n \
                            2"
                }
              ]
            },
            { "role": "user", "content": [  
                    { 
                        "type": "text", 
                        "text": "Now, select the correct answer choice from the provided 5 options"
                    }
                ]
            },
            { "role": "user", "content": [  
                    { 
                        "type": "text", 
                        "text": "Here are the options: "
                    }
                ] + [
                    {
                        "type": "text", 
                        "text": f"{index}. {shuffled_description}"
                    } for index, shuffled_description in enumerate(shuffled_descriptions, start=1)
                ] + [
                    {
                        "type": "text", 
                        "text": "You may not know what the best option is, but you must choose one. \
                                Just say the correct option number, and do not provide any additional explanations."
                    }
                ]
            }
        ]
        
        log_directory = 'ChatGPT4V_error_log'
        
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        
        try:
            response = client.chat.completions.create(
                model = "gpt-4",
                messages=messages
            )
        except Exception as e:
            with open('ChatGPT4V_error_log/Openai_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
                Openai_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f'{i}: {e}')
            openai_errors.append(i)
        
        print(f"{i}: {response.choices[0].message.content}")

        # Extraction response
        try:
            response_text = response.choices[0].message.content
            
            
            # Check
            if response_text.isdigit():
                # Saving results
                with open('Results/ChatGPT answers/ChatGPT4V_answer_no_image5.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                        
                    # Find correct answer in Shuffled_MC-LARC_output
                    correct_answer = shuffled_df.loc[shuffled_df['task_id'] == i, 'answer'].values[0]
                        
                    # Calculate Correct(1) / Wrong(0)
                    correct_wrong = 1 if int(correct_answer) == int(response_text) else 0
                        
                    # Attempt to write to CSV
                    writer.writerow([i, task_names[i], correct_answer, response_text, correct_wrong])
            else:
                # Error log
                with open('ChatGPT4V_error_log/Wrong_format_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
                    WF_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write(f'{i}\n')
                wrong_format_errors.append(i)
                wrong_format_errors.append(response_text)
                
        except Exception as e:
            with open('ChatGPT4V_error_log/Skip_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
                skip_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f'{i} : {e}\n')
            skip_errors.append(i)
        
    else:
        with open('ChatGPT4V_error_log/No_folder_path.txt', 'a', newline='\n', encoding='utf-8') as file:
                skip_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f'{i}\n')
        
    

with open('ChatGPT4V_error_log/Openai_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
        if openai_errors:
            file.write('\nnumbers = ' + str(openai_errors) + '\n')
            file.write(Openai_current_time)

with open('ChatGPT4V_error_log/Wrong_format_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
    if wrong_format_errors:
        file.write('\nnumbers = ' + str(wrong_format_errors) + '\n')
        file.write(WF_current_time)

with open('ChatGPT4V_error_log/Skip_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
    if skip_errors:
        file.write('\nnumbers = ' + str(skip_errors) + '\n')
        file.write(skip_current_time)