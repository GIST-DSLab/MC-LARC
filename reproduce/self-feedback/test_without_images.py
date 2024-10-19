import os
import csv
import pandas as pd
import random
import base64
from mimetypes import guess_type
from openai import AzureOpenAI
from utils import log_wrong_format_error, log_openai_error, shuffle_responses_in_csv

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

# Directory paths
constraints_results_dir = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/results/refined_MC-LARC/"
test_results_dir = os.path.join(constraints_results_dir, "test_results")
if not os.path.exists(test_results_dir):
    os.makedirs(test_results_dir)
    
# Initialize error tracking lists
openai_errors = []
wrong_format_errors = []

def process_task(task_id, task_name, shuffled_options, correct_answer, result_filepath):
    messages = [
        { "role": "system", "content": "You need to choose the correct option among the provided five options." },
        { "role": "system", "content": "Normally, you would need to be provided with a sample image to solve this problem, but currently, you cannot be provided with one." },
        { "role": "user", "content": "Select the correct option among the provided options." },
        { "role": "assistant", "content": "Here is the example: \n1. To make the output, you have to...change the color of the object in the single-color pattern.\n2. To make the output, you have to...move the unnecessary object in the right side.\n3. To make the output, you have to...add more objects in the rectangular boxes.\n4. To make the output, you have to...remove the objects in the input grids.\n5. To make the output, you have to...resize output grids, and then fill the grid with the single-color.\n\nIf the correct answer among the five options is 2, your response would be: 2" },
        { "role": "user", "content": "Now, select the correct answer choice from the provided 5 options" },
        { "role": "user", "content": "Here are the options:" }
    ] + [
        { "role": "user", "content": f"{index}. {shuffled_option}" }
        for index, shuffled_option in enumerate(shuffled_options, start=1)
    ] + [
        { "role": "user", "content": "You must choose one option out of the five choices. Originally, this problem requires a reference image to be provided in order to be solved. Considering this point, select the best answer. If you do not know the correct answer, choose any option from 1 to 5. And when you answer, respond with numbers only. For example, if the answer is 2, just say the number 2 and nothing else." }
    ]

    try:
        response = client.chat.completions.create(
            model="4o",
            messages=messages
        )

        response_text = response.choices[0].message.content.strip()
        print(f"{task_id}: {response_text}")

        if response_text.isdigit():
            correct_wrong = 1 if int(correct_answer) == int(response_text) else 0
            with open(result_filepath, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([task_id, task_name, correct_answer, response_text, correct_wrong])
        else:
            log_wrong_format_error(task_id, response_text)

    except Exception as e:
        log_openai_error(task_id, str(e))


for _ in range(5):
    # Process each CSV file in the directory
    for csv_filename in os.listdir(constraints_results_dir):
        if csv_filename.endswith('.csv'):
            shuffled_csv_path = os.path.join(constraints_results_dir, csv_filename)
            df = pd.read_csv(shuffled_csv_path)

            task_ids = df['task_id']
            task_names = df['task_name']
            answers = df['answers']

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
                correct_answer = answers[i]
                shuffled_options = df.loc[df['task_id'] == task_id, 
                                        ['refined_option1', 'refined_option2', 'refined_option3', 
                                        'refined_option4', 'refined_option5']].values[0]
                process_task(task_id, task_name, shuffled_options, correct_answer, result_filepath)

    # Retry for failed tasks
    while openai_errors or wrong_format_errors:
        current_openai_errors = openai_errors[:]
        current_wrong_format_errors = wrong_format_errors[:]
        openai_errors = []
        wrong_format_errors = []

        for task_id in current_openai_errors + current_wrong_format_errors:
            task_name = df.loc[df['task_id'] == task_id, 'task_name'].values[0]
            correct_answer = df.loc[df['task_id'] == task_id, 'answer'].values[0]
            shuffled_options = df.loc[df['task_id'] == task_id, ['refined_option1', 'refined_option2', 'refined_option3', 'refined_option4', 'refined_option5']].values[0]
            process_task(task_id, task_name, shuffled_options, correct_answer, result_filepath)