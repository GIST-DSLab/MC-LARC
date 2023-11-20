import openai
import csv
import pandas as pd
import datetime


# Read revised input LARC and output LARC
df = pd.read_csv('original_data/filtered_LARC_with_input_output.csv')
        
task_ids = df['task_id']
task_names = df['task_name']
description_inputs = df['description_input']
description_outputs = df['description_output']

# OpenAI API key setting
openai.api_type = "azure"
openai.api_base = "AZURE_OPENAI_ENDPOINT"   # Here
openai.api_key = "API-KEY"                  # Here
openai.api_version = "2023-05-15"


with open('MC-LARC_description_output.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["task_id", "task_name", "description_output", "ChatGPT Response1", "ChatGPT Response2", "ChatGPT Response3", "ChatGPT Response4"])

# Error numbers
numbers = [138, 177, 350]    # Examples, check the error_log.txt files

# Error list
openai_errors = []
wrong_format_errors = []
skip_errors = []

# for i in range(0, 400):     # For all descriptions,

for i in numbers:          # For error numberes,
    
    # ChatGPT prompt
    messages = [
        # system
        {"role": "system", "content": "You are my assistant who creates incorrect options based on the correct answers I provide. It is important to note that the original correct answers and the incorrect options must have different meanings. You should not simply change the words in the sentences, especially not to synonyms that do not change the meaning. "},
        {"role": "system", "content": "And you don't need to explain about the options. Please create incorrect options in the same format as the answer I provided. For example, the response should be as follows:"},
        {"role": "system", "content": "To make the output, you have to...[your answer]."},
        {"role": "system", "content": "Do not say anything other than the 4 incorrect answers. And no asterisk mark, quotation marks."},
        {"role": "system", "content": "When providing incorrect answers, please separate each answers with two line breaks between them"},
        
        # assistant, revised part, additional prompt
        {"role": "assistant", "content": "The answer that I'll provide is for a puzzle where you place square-shaped pixels of various colors within a grid of different sizes."},
        {"role": "assistant", "content": "The overall background grid is rectangular and can have an NxM size, where N and M can be arbitrarily chosen for each problem."},
        {"role": "assistant", "content": "You have a total of 9 colors of pixels to use: black, blue, red, yellow, cyan, pink, gray, green, and brown."},
        {"role": "assistant", "content": "While multiple pixels can come together to form the shape of some abstract shapes, it should be noted that each individual pixel must be square in shape."},
        
        # user
        {"role": "user", "content": "Now, I will give you the correct answer, and I want you to create four incorrect options for me. Here is the correct answer."},
        {"role": "user", "content": description_outputs[i]},
    ]

    # ChatGPT API request
    try:
        response = openai.ChatCompletion.create(
            engine="ARC-LARC", # My deploying model name
            messages=messages
        )
    except Exception as e:
        with open('ChatGPT4_error_log/Openai_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
            Openai_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f'{i}번째: {e}')
        openai_errors.append(i)

    # Extraction response
    try:
        response_text = response['choices'][0]['message']['content'].split("\n\n")
        response_text = list(filter(lambda x: x.startswith('To make the output, you have to...'), response_text))

        # Check
        if len(response_text) >= 4:
            # Saving results
            with open('MC-LARC_description_output.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([i, task_names[i], description_outputs[i], response_text[0], response_text[1], response_text[2], response_text[3]])
        else:
            # Error log
            with open('ChatGPT4_error_log/Wrong_format_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
                WF_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f'{i}\n')
            wrong_format_errors.append(i)
                
    except Exception as e:
        with open('ChatGPT4_error_log/Skip_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
            skip_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f'{i} : {e}\n')
        skip_errors.append(i)
        
    

with open('ChatGPT4_error_log/Openai_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
        if openai_errors:
            file.write('\nnumbers = ' + str(openai_errors) + '\n')
            file.write(Openai_current_time)

with open('ChatGPT4_error_log/Wrong_format_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
    if wrong_format_errors:
        file.write('\nnumbers = ' + str(wrong_format_errors) + '\n')
        file.write(WF_current_time)

with open('ChatGPT4_error_log/Skip_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
    if skip_errors:
        file.write('\nnumbers = ' + str(skip_errors) + '\n')
        file.write(skip_current_time)