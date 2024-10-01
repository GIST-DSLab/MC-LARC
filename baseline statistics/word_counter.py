import pandas as pd

# Function to count words in a text
def count_words(text):
    return len(text.split())

# Load the CSV file with appropriate encoding
file_path = r'C:\Users\oollccddss\Desktop\Work\MC-LARC\MC-LARC-EMNLP.ver\MC-LARC_before_revised.csv'
df = pd.read_csv(file_path, encoding='latin1')

# Create a new dataframe to store word counts
df_word_counts = df[['task_id', 'task_name']].copy()

# Calculate word counts for each relevant column
for col in ['description_output', 'ChatGPT Response1', 'ChatGPT Response2', 'ChatGPT Response3', 'ChatGPT Response4']:
    df_word_counts[col + '_word_count'] = df[col].apply(count_words)

# Save the new dataframe to a CSV file
output_file_path = r'C:\Users\oollccddss\Desktop\Work\MC-LARC\MC-LARC-EMNLP.ver\original_data\word_counts_before.csv'
df_word_counts.to_csv(output_file_path, index=False)

print(f"Word counts have been saved to {output_file_path}")
