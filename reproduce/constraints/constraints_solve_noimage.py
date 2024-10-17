import csv
import pandas as pd
import os
import datetime
from openai import AzureOpenAI

# Directory paths
constraints_results_dir = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/constraints_results/shuffled/"
test_results_dir = os.path.join(constraints_results_dir, "test_results")
if not os.path.exists(test_results_dir):
    os.makedirs(test_results_dir)

# OpenAI API setting
api_type = "azure"
api_base = "END-POINT"
api_key= "OPENAI-KEY"
api_version = 'MODEL-VERSION'
deployment_name = 'DEPLOY-NAME'

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=api_base
)

# Error lists
openai_errors = []
wrong_format_errors = []
skip_errors = []

# Process each CSV file in the directory
for csv_filename in os.listdir(constraints_results_dir):
    if csv_filename.endswith('.csv'):
        shuffled_csv_path = os.path.join(constraints_results_dir, csv_filename)
        df = pd.read_csv(shuffled_csv_path)

        task_ids = df['task_id']
        task_names = df['task_name']
        answers = df['answer']

        # Result file setup
        result_filename = f"test_{csv_filename}"
        result_filepath = os.path.join(test_results_dir, result_filename)
        with open(result_filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["task_id", "task_name", "Correct answer", "ChatGPT4V answer", "Correct(1) / Wrong(0)"])

        # Process each task
        for i in range(len(df)):
            task_id = task_ids[i]
            task_name = task_names[i]
            
            # Get shuffled descriptions for the current task_id
            shuffled_descriptions = df.loc[df['task_id'] == task_id, 
                                            ['shuffled_description1', 'shuffled_description2', 'shuffled_description3', 
                                             'shuffled_description4', 'shuffled_description5']].values[0]
            messages = [
                { "role": "system", "content": "You need to choose the correct option among the provided five options." },
                { "role": "system", "content": "Normally, you would need to be provided with a sample image to solve this problem, but currently, you cannot be provided with one." },
                { "role": "user", "content": [  
                    { 
                        "type": "text", 
                        "text": "select the correct option among the provided options."
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
                            "text": "You must choose one option out of the five choices. \
                                    Originally, this problem requires a reference image to be provided in order to be solved. \
                                    Considering this point, select the best answer. \
                                    If you do not know the correct answer, choose any option from 1 to 5. \
                                    And when you answer, respond with numbers only. \
                                    For example, if the answer is 2, just say the number 2 and nothing else."
                        }
                    ]
                }
            ]

            log_directory = 'ChatGPT4V_error_log'
                
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)
            
            try:
                response = client.chat.completions.create(
                    model = "4o",
                    messages=messages
                )
                
            except Exception as e:
                with open('ChatGPT4V_error_log/Openai_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
                    Openai_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write(f'{task_id}: {e}\n')
                openai_errors.append(task_id)
                continue
            
            response_text = response.choices[0].message.content.strip()
            print(f"{task_id}: {response_text}")

            # Extraction response
            try:
                # Check
                if response_text.isdigit():
                    # Find correct answer in the CSV
                    correct_answer = df.loc[df['task_id'] == task_id, 'answer'].values[0]
                    
                    # Calculate Correct(1) / Wrong(0)
                    correct_wrong = 1 if int(correct_answer) == int(response_text) else 0
                    
                    # Attempt to write to CSV
                    with open(result_filepath, 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([task_id, task_name, correct_answer, response_text, correct_wrong])
                else:
                    # Error log
                    with open('ChatGPT4V_error_log/Wrong_format_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
                        WF_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        file.write(f'{task_id}\n')
                    wrong_format_errors.append(task_id)
                    wrong_format_errors.append(response_text)
                    
            except Exception as e:
                with open('ChatGPT4V_error_log/Skip_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
                    skip_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write(f'{task_id} : {e}\n')
                skip_errors.append(task_id)
                
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
