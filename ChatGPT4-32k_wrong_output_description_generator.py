import openai
import csv
import pandas as pd
import datetime


# Read revised input LARC and output LARC
df = pd.read_csv('original_data/filtered_LARC_with_input_output_description.csv')
        
task_ids = df['task_id']
task_names = df['task_name']
description_inputs = df['description_input']
description_outputs = df['description_output']

# OpenAI API key setting
openai.api_type = "azure"
openai.api_base = "AZURE_OPENAI_ENDPOINT"         # Here - AZURE_OPENAI_ENDPOINT
openai.api_key = "API-KEY"             # Here - API-KEY
openai.api_version = "API-VERSION"       # Here - API-VERSION    EX) 2023-05-15


with open('MC-LARC_output.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["task_id", "task_name", "description_output", "ChatGPT Response1", "ChatGPT Response2", "ChatGPT Response3", "ChatGPT Response4"])

# Error numbers
numbers = [382]    # Examples, check the error_log.txt files

# Error list
openai_errors = []
wrong_format_errors = []
skip_errors = []

# for i in range(0, 400):     # For all descriptions,

for i in numbers:          # For error numberes,
    
    # ChatGPT prompt
    messages = [
        # system
        {"role": "system", "content": "You are my assistant who creates incorrect options based on the correct answers that I provide."},
        
        # user
        # correct answer vs. wrong answer
        {"role": "user", "content": "It is important to note that the original correct answers and the incorrect options must have different meanings. You should not simply change the words in the sentences, especially not to synonyms that do not change the meaning."},
        
        # format of output
        {"role": "user", "content": "And you don't need to explain about the options."},
        {"role": "user", "content": "Please only create incorrect options in the same format as the answer I provided."},
        {"role": "user", "content": "You should specifically maintain the part 'To make the output, you have to...' consistently across all responses."},
        {"role": "user", "content": "Specific examples include the following:"},
        {"role": "user", "content": "To make the output, you have to...fill the blank black grid part."},
        
        # length of output
        {"role": "user", "content": "Also, when creating incorrect answer choices for the provided correct answer options, you have to make sure to keep the length of the sentences fairly similar."},
        {"role": "user", "content": "Do not use asterisk marks and quotation marks."},
        
        # line breaks
        {"role": "user", "content": "When providing incorrect answers, please separate each answers with two line breaks between them."},
        
        # grid system explanation
        {"role": "user", "content": "The answer that I'll provide is for a puzzle where you place square-shaped pixels of various colors within a grid of different sizes."},
        {"role": "user", "content": "The overall background grid is rectangular and can have an NxM size, where N and M can be arbitrarily chosen integer from 1 to 30 for each problem."},
        
        # colors
        {"role": "user", "content": "You have a total of 9 colors of pixels to use: black, blue, red, yellow, light blue, pink, gray, green, and brown."},
        {"role": "user", "content": "You can only use available colors, and you must not use any other colors when creating incorrect answer choices."},
        
        # shapes
        {"role": "user", "content": "While multiple pixels can come together to form the shape of some abstract shapes, it should be noted that each individual pixel must be square in shape."},
        {"role": "user", "content": "The shape of objects created by clustered pixels is based on a square pixel shape; therefore, it is not possible to represent shapes like circles, ellipses, or polygons with more than four sides."},
        {"role": "user", "content": "Therefore, when creating incorrect answer choices, refrain from using expressions such as circles, ellipses, pentagons, hexagons, and so on."},
        
        # assistant
        # one-shot example
        {"role": "assistant", "content": "Here I will show you examples of incorrect answers based on the correct answer."},
        
        {"role": "assistant", "content": "Correct answer: "},
        {"role": "assistant", "content": "To make the output, you have to...draw a vertical red line, first. Then, draw horizontal lines through the green and blue squares."},
        
        {"role": "assistant", "content": "Four wrong answers: "},
        {"role": "assistant", "content": "To make the output, you have to...draw a vertical red line, frist. Then, draw horizontal lines through the green and blue squares."},
        {"role": "assistant", "content": "To make the output, you have to...draw a horizontal blue line, frist. Then, draw vertical lines through the green and red squares."},
        {"role": "assistant", "content": "To make the output, you have to...draw a vertical green, red, and blue line through the green, red, and blue squares."},
        {"role": "assistant", "content": "To make the output, you have to...draw a vertical green line, frist. Then, draw horizontal lines through the blue and red squares."},
        
        # user
        # correct answer
        {"role": "user", "content": "And you don't need to explain about the options."},
        {"role": "user", "content": "Do not use asterisk marks and quotation marks."},
        {"role": "user", "content": "Now, I will give you the correct answer, and I want you to create four wrong answers for me. Here is the correct answer."}, 
        {"role": "user", "content": description_outputs[i]},
    ]

    # ChatGPT API request
    try:
        response = openai.ChatCompletion.create(
            engine="TIST", # My deploying model name
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
            with open('MC-LARC_output.csv', 'a', newline='', encoding='utf-8') as file:
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