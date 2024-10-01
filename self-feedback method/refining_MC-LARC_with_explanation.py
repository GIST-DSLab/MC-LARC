import os
import csv
import pandas as pd
import random
import base64
from mimetypes import guess_type
from openai import AzureOpenAI
from utils import local_image_to_data_url, select_random_images_and_convert_to_data_urls, log_wrong_format_error, log_openai_error, shuffle_responses_in_csv

# OpenAI API setting
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

# Directory paths
filepath = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/results/"
refined_results_dir = os.path.join(filepath, "refined_MC-LARC")
if not os.path.exists(refined_results_dir):
    os.makedirs(refined_results_dir)

# Initialize error tracking lists
openai_errors = []
wrong_format_errors = []

# Load CSV files
additional_csv_path = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/results/initial_MC-LARC/shuffled/test_results/exaplanation_constraints_gcsotf_shuffled.csv"
main_csv_path = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/results/initial_MC-LARC/shuffled/constraints_gcsotf_shuffled.csv"

additional_df = pd.read_csv(additional_csv_path)
main_df = pd.read_csv(main_csv_path)

# Ensure task_id columns are of the same type
additional_df['task_id'] = additional_df['task_id'].astype(str)
main_df['task_id'] = main_df['task_id'].astype(str)

def process_task(task_id, task_name, shuffled_options, correct_answer, llm_explanation, result_filepath):
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
    
    messages_base = [
        { "role": "system", "content": "You must create multiple choice options that cannot be solved by just looking at the choices." },
        { "role": "system", "content": "Using the provided explanation, make it difficult to determine which of the five options is the correct answer." },
        { "role": "system", "content": "After refining options, You need to give well refined five options." },
        
        { "role": "user", "content": "The given problem normally requires the use of a provided image to solve." },
        { "role": "user", "content": "However, poorly constructed options might allow someone to find the correct answer through comparison alone, even without sufficient information." },
        { "role": "user", "content": "This drastically lowers the quality of the multiple-choice problem, so it needs to be corrected.\n" },
        { "role": "user", "content": "Therefore, I'll provide an explanation of how the correct answer was determined from the five given options, and you need to revise the options so that the correct answer cannot be found by just looking at the options.\n\n" },
        { "role": "user", "content": "Here are the problem options:" }
    ] + [
        { "role": "user", "content": f"{index}. {shuffled_option}\n" }
        for index, shuffled_option in enumerate(shuffled_options, start=1)
    ] + [
        { "role": "user", "content": f"And here is an explanation:" }
    ] + [
        { "role": "user", "content": f"Explanation: {llm_explanation}\n" }
    ] + [
        { "role": "user", "content": f"This is a correct answer number: " }
    ] + [
        { "role": "user", "content": f"Explanation: The option number {correct_answer}\n" }
    ] + [
        { "role": "user", "content": f"If the answer given in the explanation is the same as the actual answer, the options should be changed so you can't find the correct answer just by looking at them.\n" },
        { "role": "user", "content": f"Even if the answer given in the explanation is different from the actual answer, the options should still be changed so you can't find the correct answer just by looking at them.\n\n" }
    ]
    
    messages_example = [
        { "role": "assistant", "content": f"I'll give you an example here: \n" },
        
        { "role": "assistant", "content": f"Before refining (given 5 options): \n" },
        { "role": "assistant", "content": "To make the output, you have to...imagine the grid as a dark field and as the colored squares as being objects flying in space. Gravity is suddenly negated and all of the blocks rise vertically to the top. That produces the correct output grid.\n" },
        { "role": "assistant", "content": "To make the output, you have to...think of the grid as a white field and as the colored squares as being objects fixed in space. Gravity is suddenly turned off and all the blocks rise vertically to the top. That produces the correct output grid.\n" },
        { "role": "assistant", "content": "To make the output, you have to...visualize the grid as a light field and as the colored squares as being static objects in space. Gravity is suddenly engaged and all of the blocks move horizontally to the left. That produces the correct output grid.\n" },
        { "role": "assistant", "content": "To make the output, you have to...consider the grid as a dark field and as the colored squares as being objects moving horizontally in space. Gravity is suddenly turned on and all of the blocks fall horizontally to the right. That produces the correct output grid.\n" },
        { "role": "assistant", "content": "To make the output, you have to...think of the grid as a black field and as the colored squares as being objects floating in space. Gravity is suddenly turned on and all of the block fall vertically to the bottom. That produces the correct output grid.\n" },
        
        { "role": "assistant", "content": f"After refining: \n" },
        { "role": "assistant", "content": "To make the output, you have to...imagine the grid as a dark field and the colored squares as being objects in space. Suddenly, all the blocks move vertically to the top. That produces the correct output grid.\n" },
        { "role": "assistant", "content": "To make the output, you have to...think of the grid as a white field and the colored squares as being objects in space. Suddenly, all the blocks move vertically to the top. That produces the correct output grid.\n" },
        { "role": "assistant", "content": "To make the output, you have to...visualize the grid as a light field and the colored squares as being static objects in space. Suddenly, all the blocks move horizontally to the left. That produces the correct output grid.\n" },
        { "role": "assistant", "content": "To make the output, you have to...consider the grid as a dark field and the colored squares as being objects in space. Suddenly, all the blocks move horizontally to the right. That produces the correct output grid.\n" },
        { "role": "assistant", "content": "To make the output, you have to...think of the grid as a black field and the colored squares as being objects in space. Suddenly, all the blocks move vertically to the bottom. That produces the correct output grid.\n" },

        { "role": "assistant", "content": f"Therefore, your output looks like this: \n" },
        { "role": "assistant", "content": "To make the output, you have to...[refined_option1]\n" },
        { "role": "assistant", "content": "To make the output, you have to...[refined_option2]\n" },
        { "role": "assistant", "content": "To make the output, you have to...[refined_option3]\n" },
        { "role": "assistant", "content": "To make the output, you have to...[refined_option4]\n" },
        { "role": "assistant", "content": "To make the output, you have to...[refined_option5]\n" }
    ]
    
    messages_base2 = [
        { "role": "user", "content": "I will provide the images that are essential for solving this problem. \n" },
        { "role": "user", "content": "The given image shows a pair of grids made up of pixels in 10 different colors: black, blue, red, yellow, orange, light blue, pink, gray, green, and brown. \n" },
        { "role": "user", "content": "The image includes a pair of grids. To solve the problem, you need to choose the option that best explains how the input grid is transformed into the output grid. \n" },
        { "role": "user", "content": "Your task is to refine the five given options into better choices while maintaining the following criteria: \n" },
        
        { "role": "user", "content": "1. The correct answer should be the one marked as the actual answer, and its meaning should not change so that the correct answer remains valid. \n" },
        { "role": "user", "content": "2. The other four options should not be correct answer and should have meanings different from the correct answer. \n" },
        { "role": "user", "content": "3. However, when the image is not provided, it should be impossible to determine which is the correct option just by looking at the choices. \n" },
        { "role": "user", "content": "Now, I'll provide problem images. Here are images: \n" }
    ]
    
    messages_format = [
        { "role": "user", "content": "Here are the rules you must strictly follow.\n" },
        { "role": "user", "content": f"1. Do not change the meaning of the actual correct answer. The option {correct_answer}.\n" },
        { "role": "user", "content": "2. The other incorrect answers should have meanings different from the actual correct answer. \n" },
        { "role": "user", "content": "3. When refining the five choices, you should aim to maximize the independence of words within each choice.  \n" },
        { "role": "user", "content": "4. Provide responses with only the five refined options.\n" },
        { "role": "user", "content": "5. Do not explain the refined options.\n" },
        { "role": "user", "content": "6. Do not use asterisks or quotation marks.\n" },
        { "role": "user", "content": "7. Do not change the order of the given problem options.\n" },
        { "role": "user", "content": "8. When providing refined options, please separate each option with line breaks between them.\n" },
        { "role": "user", "content": "9. Do not include numbers before the refined options. Provide the options as clean sentences.\n" },
        { "role": "user", "content": "10. When generating the problem, keep this prefix 'To make the output, you have to...' the same in all sentences. \n" },
        
        { "role": "user", "content": f"Now, make it difficult to determine which of the five options is the correct answer." }
    ]
    
    messages = messages_base + messages_example + messages_base2 + messages_figure + messages_format

    try:
        response = client.chat.completions.create(
            model="4o",
            messages=messages
        )
        
        response_text = response.choices[0].message.content
        
        print(response_text)
        
        
        split_texts = response_text.split("\n")
        filtered_texts = [text.strip() for text in split_texts if text.startswith('To make the output, you have to')]

        output_text = '\n'.join(filtered_texts)
        print(task_id)
        print(output_text)

        if len(filtered_texts) >= 5:
            with open(result_filepath, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([task_id, task_name, filtered_texts[0], filtered_texts[1], filtered_texts[2], filtered_texts[3], filtered_texts[4], correct_answer])
        else:
            log_wrong_format_error(task_id)
            wrong_format_errors.append(task_id)

    except Exception as e:
        log_openai_error(task_id, str(e))
        openai_errors.append(task_id)

# Merge with additional CSV data
merged_df = main_df.merge(additional_df[['task_id', 'task_name', 'explanation']],
                          on=['task_id', 'task_name'],
                          how='left')

task_ids = merged_df['task_id']
task_names = merged_df['task_name']
answers = merged_df['answers']
llm_explanations = merged_df['explanation']

# Result file setup
result_filename = "refined_constraints_gcsotf_shuffled.csv"
result_filepath = os.path.join(refined_results_dir, result_filename)
with open(result_filepath, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["task_id", "task_name", "refined_option1", "refined_option2", "refined_option3", "refined_option4", "refined_option5", "answers"])

# Process each task
for i in range(len(merged_df)):
    task_id = task_ids[i]
    task_name = task_names[i]
    correct_answer = answers[i]
    llm_explanation = llm_explanations[i]
    shuffled_options = merged_df.loc[merged_df['task_id'] == task_id, 
                                     ['shuffled_options1', 'shuffled_options2', 'shuffled_options3', 
                                      'shuffled_options4', 'shuffled_options5']].values[0]
    process_task(task_id, task_name, shuffled_options, correct_answer, llm_explanation, result_filepath)

# Retry for failed tasks
while openai_errors or wrong_format_errors:
    current_openai_errors = openai_errors[:]
    current_wrong_format_errors = wrong_format_errors[:]
    openai_errors = []
    wrong_format_errors = []

    for task_id in current_openai_errors + current_wrong_format_errors:
        task_name = merged_df.loc[merged_df['task_id'] == task_id, 'task_name'].values[0]
        correct_answer = merged_df.loc[merged_df['task_id'] == task_id, 'answers'].values[0]
        llm_explanation = merged_df.loc[merged_df['task_id'] == task_id, 'explanation'].values[0]
        shuffled_options = merged_df.loc[merged_df['task_id'] == task_id, 
                                         ['shuffled_options1', 'shuffled_options2', 'shuffled_options3', 
                                          'shuffled_options4', 'shuffled_options5']].values[0]
        process_task(task_id, task_name, shuffled_options, correct_answer, llm_explanation, result_filepath)
