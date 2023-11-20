import pandas as pd

# File path to the CSV file
file_path = 'shuffled_output_description.csv'

# Read the CSV file
df = pd.read_csv(file_path)

# Extract data from the 'answer' column and drop NaN values
answers = df['answer'].dropna()

# Open a text file to write the results
with open('answer.txt', 'w') as f:
    # Loop through the answers and write to the file
    for index, answer in enumerate(answers, start=1):
        f.write(f"task_{index - 1}: {answer}\n")

print("The answers have been successfully written to answer.txt")