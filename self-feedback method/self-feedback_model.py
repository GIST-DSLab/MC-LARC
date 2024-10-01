import os
import csv
import pandas as pd
import random
import base64
from mimetypes import guess_type
from openai import AzureOpenAI
from utils import local_image_to_data_url, select_random_images_and_convert_to_data_urls, select_constraints, log_wrong_format_error, log_openai_error, shuffle_responses_in_csv

# Azure OpenAI setting
api_type = "azure"
api_base = "https://mc-larc.openai.azure.com/"
api_key = "e485753d492d4e0bb1ebecb8e45aabf9"
api_version = "2024-02-01"
deployment_name = '4o'

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=api_base
)
 
# read language description from revised LARC
df = pd.read_csv('original_revised_LARC.csv')
task_ids = df['task_id']
task_names = df['task_name']
description_inputs = df['description_input']
description_outputs = df['description_output']

# problem numbers
numbers = random.sample(range(7, 400), 20)
# numbers = [12, 15, 26, 33, 35]
# numbers = list(range(37, 400))
# numbers = list(range(400))

# prompt
messages_grid = [
    { "role": "user", "content": "The answer that I'll provide is for a puzzle where you place square-shaped pixels of various colors within a grid of different sizes." },
    { "role": "user", "content": "The overall background grid is rectangular and can have an NxM size, where N and M can be arbitrarily chosen integer from 1 to 30 for each problem." }
]

messages_color = [
    { "role": "user", "content": "You have a total of 10 colors of pixels to use: black, blue, red, yellow, orange, light blue, pink, gray, green, and brown." },
    { "role": "user", "content": "You can only use available colors, and you must not use any other colors when creating incorrect answer choices." }
]

messages_vocabulary = [
    { "role": "user", "content": "Do not use words such as circles, ellipses, pentagons, hexagons." },
    { "role": "user", "content": "Since pixels are squares, you can use vocabulary related to rectangular shapes composed of these squares." },
    { "role": "user", "content": "For example, you can use words like line, square, rectangle, and rectangle boundary, which can be made up of square pixels." }
]

messages_repeated = [
    { "role": "user", "content": "One of the most important things to be careful about when creating distractors is ensuring that the correct answer cannot be identified just by looking at the options." },
    { "role": "user", "content": "To prevent this, avoid excessive overlap among the options and be mindful of situations where the correct answer can be identified by spotting the most frequently repeated words." }
]

messages_contradiction = [
    { "role": "user", "content": "Another important point to be cautious of is allowing test-takers to eliminate an option easily by finding contradictions through comparison of the choices."},
    { "role": "user", "content": "This significantly lowers the difficulty of the question." },
    { "role": "user", "content": "Therefore, when creating incorrect options, ensure that contradictions cannot be identified just by comparing the choices." },
    { "role": "user", "content": "Be careful to avoid contradictions between specific vocabulary in the options and the concepts in the incorrect choices." },
    { "role": "user", "content": "For example, using the keyword 'gravity' but then saying something falls sideways or flies to the right creates easily eliminated incorrect choices." },
    { "role": "user", "content": "Therefore, when generating incorrect options, it is important to check for contradictions within the wording of the choices." }
]

messages_figure = [
    { "role": "user", "content": "Here are example figures. Please generate distractors based on this example figure." }
]

messages_dict = {
    "grid": messages_grid,
    "color": messages_color,
    "shapes": messages_vocabulary,
    "one_partofcore": messages_repeated,
    "two_contradiction": messages_contradiction,
    "figure": messages_figure
}

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
    { "role": "user", "content": "When providing incorrect answers, please separate each answers with line breaks between them." }
]

# one-shot example
messages_example =[
    {"role": "assistant", "content": "Here I will show you example of incorrect answers based on the correct answer."},
    
    {"role": "assistant", "content": "Example 1"},
    {"role": "assistant", "content": "Correct answer: "},
    {"role": "assistant", "content": "To make the output, you have to...erase the all objects below the horizontal line."},
    
    {"role": "assistant", "content": "Four wrong answers: \n"},
    {"role": "assistant", "content": "To make the output, you have to...erase only some of the objects below the horizontal line.\n"},
    {"role": "assistant", "content": "To make the output, you have to...keep all objects below the horizontal line.\n"},
    {"role": "assistant", "content": "To make the output, you have to...erase the all objects above the horizontal line.\n"},
    {"role": "assistant", "content": "To make the output, you have to...move the all objects below the horizontal line.\n"}
]

messages_base2 =[
    {"role": "user", "content": "When creating incorrect options, multiple correct answers should not arise."},
    {"role": "user", "content": "An example of multiple correct answers is as follows:"},
    {"role": "user", "content": "To make the output, you have to...move each tile so that the gray square in each tile occupies the center square of the output 3x3 grid."},
    {"role": "user", "content": "To make the output, you have to...move each pattern so that the gray rectangle in each pattern occupies the center rectangle of the output 3x3 grid."},
    {"role": "user", "content": "By examining these two sentences, it can be observed that square was changed to rectangle, but in this context, square, rectangle, and pixels doesn't show different meanings."},
    {"role": "user", "content": "Therefore, since the two sentences convey exactly the same meaning, it cannot be considered as appropriately creating incorrect options."},
    {"role": "user", "content": "And you don't need to explain about the options."},
    {"role": "user", "content": "Do not use asterisk marks and quotation marks."}
]

messages_first, filepath = select_constraints(messages_dict)
messages = messages_base + messages_first

with open(filepath, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["task_id", "task_name", "description_output", "ChatGPT Response1", "ChatGPT Response2", "ChatGPT Response3", "ChatGPT Response4"])

def process_task(i, messages):
    task_name = df.loc[df['task_id'] == i, 'task_name'].values[0]
    folder_path = f"C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/Image file/training_IO_each_pair_folder_without_label/{task_name}.json"

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

    messages_base3 = [
        {"role": "user", "content": "Now, I will give you the correct answer. Here is the correct answer."},
        {"role": "user", "content": f"The correct answer{description_outputs[df.index[df['task_id'] == i].tolist()[0]]}"},
        {"role": "user", "content": "Generate 4 incorrect options based on this correct answer."},
        {"role": "user", "content": "You must create exactly 4 distractors."}
    ]

    messages += messages_example + messages_base2 + messages_base3
    
    try:
        response = client.chat.completions.create(
            model="4o",
            messages=messages
        )
        
        response_text = response.choices[0].message.content
        split_texts = response_text.split("\n")
        filtered_texts = [text.strip() for text in split_texts if text.startswith('To make the output, you have to...')]

        output_text = '\n'.join(filtered_texts)
        print(f"{i}:\n{output_text}")

        if len(filtered_texts) >= 4:
            with open(filepath, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([i, task_name, description_outputs[df.index[df['task_id'] == i].tolist()[0]], filtered_texts[0], filtered_texts[1], filtered_texts[2], filtered_texts[3]])
        else:
            log_wrong_format_error(i)
            wrong_format_errors.append(i)

    except Exception as e:
        log_openai_error(i, str(e))
        openai_errors.append(i)

openai_errors = []
wrong_format_errors = []

for i in numbers:
    process_task(i, messages)
    messages = messages_base + messages_first

# Retry for failed tasks
while openai_errors or wrong_format_errors:
    current_openai_errors = openai_errors[:]
    current_wrong_format_errors = wrong_format_errors[:]
    openai_errors = []
    wrong_format_errors = []

    for i in current_openai_errors + current_wrong_format_errors:
        process_task(i, messages)
        messages = messages_base + messages_first

# shuffle csv
directory = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/results/initial_MC-LARC"
shuffle_responses_in_csv(directory)