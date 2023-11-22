import pandas as pd

# Read the CSV file
df = pd.read_csv('description_output.csv', encoding='ISO-8859-1')

# Set the start sentence
start_sentence = 'To make the output, you have to...'

# Check rows that don't start with the specified sentence in any of the ChatGPT Response columns
rows_not_starting_with = df[~df['ChatGPT Response1'].str.startswith(start_sentence) &
                            ~df['ChatGPT Response2'].str.startswith(start_sentence) &
                            ~df['ChatGPT Response3'].str.startswith(start_sentence) &
                            ~df['ChatGPT Response4'].str.startswith(start_sentence)]

# Save the wrong row numbers and create a list of row_numbers
row_numbers = list(rows_not_starting_with.index)  # Save wrong row numbers as a list

# Write to Wrong_row_numbers.txt file
with open('ChatGPT4_error_log/Wrong_format_numbers.txt', 'w') as f:
    for row_number in row_numbers:
        f.write(str(row_number) + '\n')
    f.write('\n')  # Newline for separating content
    f.write('numbers = ' + str(row_numbers) + '\n')

print("Check the Wrong_format_numbers.txt.")