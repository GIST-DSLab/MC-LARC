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
explanation_results_dir = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/results/initial_MC-LARC/shuffled/"
test_results_dir = os.path.join(explanation_results_dir, "test_results")
if not os.path.exists(test_results_dir):
    os.makedirs(test_results_dir)
    
# Initialize error tracking lists
openai_errors = []
wrong_format_errors = []

# Load additional CSV file
additional_csv_path = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/results/initial_MC-LARC/shuffled/test_results/test_constraints_gcsotf_shuffled.csv"
additional_df = pd.read_csv(additional_csv_path)

def process_task(task_id, task_name, shuffled_options, correct_answer, llm_answer, result_filepath):
    messages = [
        { "role": "system", "content": "You need to provide a reasonable explanation for choosing one correct answer from the given five options as requested." },
        { "role": "system", "content": "The given problem normally requires additional image information to solve, but you identified the correct answer without the image by catching a special aspect among the options." },
        { "role": "system", "content": "Therefore, you need to provide a good explanation for why you chose the most plausible option for an unsolvable problem." },
        { "role": "user", "content": "Give an explanation for choosing the following answer among the five options provided." },
        { "role": "assistant", "content": f"Here is the example: \n1. To make the output, you have to...change the color of the object in the single-color pattern.\n2. To make the output, you have to...move the unnecessary object in the right side.\n3. To make the output, you have to...add more objects in the rectangular boxes.\n4. To make the output, you have to...remove the objects in the input grids.\n5. To make the output, you have to...resize output grids, and then fill the grid with the single-color." },
        { "role": "assistant", "content": f"If your previous answer among the five options was 2, provide a reasonable explanation for why you chose that answer." },
        { "role": "user", "content": "Now, give an explanation for the problem with five options and your previous answer" },
        { "role": "user", "content": "Here are the problem options:" }
    ] + [
        { "role": "user", "content": f"{index}. {shuffled_option}" }
        for index, shuffled_option in enumerate(shuffled_options, start=1)
    ] + [
        { "role": "user", "content": f"And here are your previous answer:" }
    ] + [
        { "role": "user", "content": f"Previous your answer: {llm_answer}" }
    ] + [
        { "role": "user", "content": f"Give me an explanation for why you provided the  answer, {llm_answer}, to the problem with the five given options. \n" },
        { "role": "user", "content": "The explanation should briefly summarize the key points or keywords that led to the selection of the correct answer. \n" },
        { "role": "user", "content": "Also, do not add unnecessary sentences like introductions and conclusions; provide only the core explanation. \n" }
    ]

    try:
        response = client.chat.completions.create(
            model="4o",
            messages=messages
        )

        response_text = response.choices[0].message.content.strip()
        print(f"{task_id}: {response_text}")

        with open(result_filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([task_id, task_name, response_text])

    except Exception as e:
        log_openai_error(task_id, str(e))

# Process each CSV file in the directory
for csv_filename in os.listdir(explanation_results_dir):
    if csv_filename.endswith('.csv'):
        shuffled_csv_path = os.path.join(explanation_results_dir, csv_filename)
        df = pd.read_csv(shuffled_csv_path)

        # Merge with additional CSV data
        merged_df = df.merge(additional_df[['task_id', 'task_name', 'ChatGPT4V answer']],
                             on=['task_id', 'task_name'],
                             how='left')

        task_ids = merged_df['task_id']
        task_names = merged_df['task_name']
        answers = merged_df['answers']
        llm_answers = merged_df['ChatGPT4V answer']

        # Result file setup
        result_filename = f"exaplanation_{csv_filename}"
        result_filepath = os.path.join(test_results_dir, result_filename)
        with open(result_filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["task_id", "task_name", "explanation"])

        # Process each task
        for i in range(len(merged_df)):
            task_id = task_ids[i]
            task_name = task_names[i]
            correct_answer = answers[i]
            llm_answer = llm_answers[i]
            shuffled_options = merged_df.loc[merged_df['task_id'] == task_id, 
                                             ['shuffled_options1', 'shuffled_options2', 'shuffled_options3', 
                                              'shuffled_options4', 'shuffled_options5']].values[0]
            process_task(task_id, task_name, shuffled_options, correct_answer, llm_answer, result_filepath)

# Retry for failed tasks
while openai_errors or wrong_format_errors:
    current_openai_errors = openai_errors[:]
    current_wrong_format_errors = wrong_format_errors[:]
    openai_errors = []
    wrong_format_errors = []

    for task_id in current_openai_errors + current_wrong_format_errors:
        task_name = merged_df.loc[merged_df['task_id'] == task_id, 'task_name'].values[0]
        correct_answer = merged_df.loc[merged_df['task_id'] == task_id, 'answers'].values[0]
        llm_answer = merged_df.loc[merged_df['task_id'] == task_id, 'ChatGPT4V answer'].values[0]
        shuffled_options = merged_df.loc[merged_df['task_id'] == task_id, 
                                         ['shuffled_options1', 'shuffled_options2', 'shuffled_options3', 
                                          'shuffled_options4', 'shuffled_options5']].values[0]
        process_task(task_id, task_name, shuffled_options, correct_answer, llm_answer, result_filepath)
