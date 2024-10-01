import os
import csv
import pandas as pd
import random
import datetime
import base64
from mimetypes import guess_type
from openai import AzureOpenAI

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

# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{base64_encoded_data}"

# Function to randomly select image files
def select_random_images_and_convert_to_data_urls(folder_path, num_images=4):
    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png')]
    selected_images = random.sample(images, min(len(images), num_images))
    data_urls = [local_image_to_data_url(image) for image in selected_images]
    return data_urls

def create_custom_messages():
    # Predefined message sets
    messages_grid = [
        { "role": "user", "content": "The answer that I'll provide is for a puzzle where you place square-shaped pixels of various colors within a grid of different sizes." },
        { "role": "user", "content": "The overall background grid is rectangular and can have an NxM size, where N and M can be arbitrarily chosen integer from 1 to 30 for each problem." }
    ]

    messages_color = [
        { "role": "user", "content": "You have a total of 10 colors of pixels to use: black, blue, red, yellow, light blue, pink, gray, green, and brown." },
        { "role": "user", "content": "You can only use available colors, and you must not use any other colors when creating incorrect answer choices." }
    ]

    messages_shapes = [
        { "role": "user", "content": "Do not use words such as circles, ellipses, pentagons, hexagons, and so on." }
    ]
    
    messages_figure = [
        { "role": "user", "content": "Here are example figures. Please generate distractors based on this example figure." }
    ]


    messages_dict = {
        "grid": messages_grid,
        "color": messages_color,
        "shapes": messages_shapes,
        "figure": messages_figure
    }

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

    if not os.path.exists('constraints_results'):
        os.makedirs('constraints_results')

    filename = f"constraints_{''.join(selected_keys)}.csv"
    filepath = os.path.join('constraints_results', filename)

    return final_messages, filepath

messages_base = [
    { "role": "system", "content": "You are my assistant who creates incorrect options based on the correct answers that I provide." },
    { "role": "user", "content": "The following are the rules that you must adhere to when creating incorrect options:" },
    { "role": "user", "content": "It is important to note that the original correct answers and the incorrect options must have different meanings. You should not simply change the words in the sentences, especially not to synonyms that do not change the meaning." },
    { "role": "user", "content": "When generating incorrect options, you should not create a sentence that is identical to the given correct answer." },
    { "role": "user", "content": "When creating incorrect options by changing words, you must always use antonyms to generate the wrong choices." },
    { "role": "user", "content": "And avoid using difficult words like 'haphazardly' as much as possible." }
]

messages_length = [
    { "role": "user", "content": "Also, when creating incorrect answer choices for the provided correct answer options, you have to make sure to keep the length of the sentences fairly similar." }
]

messages_format = [
    { "role": "user", "content": "And you don't need to explain about the options." },
    { "role": "user", "content": "Please only create incorrect options in the same format as the answer I provided." },
    { "role": "user", "content": "You should specifically maintain the part 'To make the output, you have to...' consistently across all responses." },
    { "role": "user", "content": "Specific examples include the following:" },
    { "role": "user", "content": "To make the output, you have to...fill the blank black grid part." },
    { "role": "user", "content": "Do not use asterisk marks and quotation marks." },
    { "role": "user", "content": "When providing incorrect answers, please separate each answers with two line breaks between them." }
]

messages1, filepath = create_custom_messages()
messages = messages_base + messages1

with open(filepath, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["task_id", "task_name", "description_output", "ChatGPT Response1", "ChatGPT Response2", "ChatGPT Response3", "ChatGPT Response4"])

df = pd.read_csv('original_revised_LARC.csv')
task_ids = df['task_id']
task_names = df['task_name']
description_inputs = df['description_input']
description_outputs = df['description_output']

# numbers = [31]
numbers = [31, 86, 13, 96, 67, 145, 234, 307, 273, 331]

openai_errors = []
wrong_format_errors = []
skip_errors = []

for i in numbers:
    task_name = df.loc[df['task_id'] == i, 'task_name'].values[0]
    folder_path = f"C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/Image file/training_IO_each_pair_folder_without_label/{task_name}.json"

    data_urls = select_random_images_and_convert_to_data_urls(folder_path)
    messages_figure = [
        {"role": "user", "content": [  
            { 
                "type": "image_url", 
                "image_url": {"url": data_url}
            } for data_url in data_urls
        ]}
    ]

    messages += messages_figure + messages_format + messages_length
    
    messages_example =[
        # few-shot example
        {"role": "assistant", "content": "Here I will show you example of incorrect answers based on the correct answer."},
        
        {"role": "assistant", "content": "Example 1"},
        {"role": "assistant", "content": "Correct answer: "},
        {"role": "assistant", "content": "To make the output, you have to...erase the all objects below the horizontal line."},
        
        {"role": "assistant", "content": "Four wrong answers: "},
        {"role": "assistant", "content": "To make the output, you have to...erase only some of the objects below the horizontal line."},
        {"role": "assistant", "content": "To make the output, you have to...keep all objects below the horizontal line."},
        {"role": "assistant", "content": "To make the output, you have to...erase the all objects above the horizontal line."},
        {"role": "assistant", "content": "To make the output, you have to...move the all objects below the horizontal line."},
    ]

    messages_base2 = [
        {"role": "user", "content": "When creating incorrect options, multiple correct answers should not arise."},
        {"role": "user", "content": "An example of multiple correct answers is as follows:"},
        {"role": "user", "content": "To make the output, you have to...move each tile so that the gray square in each tile occupies the center square of the output 3x3 grid."},
        {"role": "user", "content": "To make the output, you have to...move each pattern so that the gray rectangle in each pattern occupies the center rectangle of the output 3x3 grid."},
        {"role": "user", "content": "By examining these two sentences, it can be observed that square was changed to rectangle, but in this context, square, rectangle, and pixels doesn't show different meanings."},
        {"role": "user", "content": "Therefore, since the two sentences convey exactly the same meaning, it cannot be considered as appropriately creating incorrect options."},
        {"role": "user", "content": "And you don't need to explain about the options."},
        {"role": "user", "content": "Do not use asterisk marks and quotation marks."},
        {"role": "user", "content": "Now, I will give you the correct answer. Here is the correct answer."},
        {"role": "user", "content": f"The correct answer{description_outputs[df.index[df['task_id'] == i].tolist()[0]]}"},
        {"role": "user", "content": "Generate 4 incorrect options based on this correct answer."},
        {"role": "user", "content": "You must create exactly 4 distractors."}
    ]

    messages += messages_example + messages_base2
    
    try:
        response = client.chat.completions.create(
            model="4o",
            messages=messages
        )
        
        response_text = response.choices[0].message.content

        split_texts = response_text.split("\n\n")

        filtered_texts = [text.strip() for text in split_texts if text.startswith('To make the output, you have to...')]

        print(filtered_texts)

        if len(filtered_texts) >= 4:
            with open(filepath, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([i, task_name, description_outputs[df.index[df['task_id'] == i].tolist()[0]], filtered_texts[0], filtered_texts[1], filtered_texts[2], filtered_texts[3]])
        else:
            with open('ChatGPT4_error_log/Wrong_format_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
                WF_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f'{i}\n')
            wrong_format_errors.append(i)

    except Exception as e:
        with open('ChatGPT4_error_log/Openai_error_log.txt', 'a', newline='\n', encoding='utf-8') as file:
            Openai_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f'{i}번째: {e}')
        openai_errors.append(i)

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
