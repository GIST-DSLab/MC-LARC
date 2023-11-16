# Read the content of the two files.
with open('MC-LARC/prompt_answer.txt', 'r') as file1, open('answer.txt', 'r') as file2:
    content1 = file1.readlines()
    content2 = file2.readlines()

# Convert the content of both files into dictionaries.
data1 = {}
data2 = {}
for line in content1:
    parts = line.strip().split(': ')
    if len(parts) == 2:
        key, value = parts
        data1[key] = int(value)
for line in content2:
    parts = line.strip().split(': ')
    if len(parts) == 2:
        key, value = parts
        data2[key] = int(value)

# Compare the two dictionaries to find differing items and save them in wrong_answer_prompt.txt.
difference_count = 0
total_items = 0

with open('MC-LARC/wrong_answer_prompt_with_hint.txt', 'w') as wrong_file:
    for key in data1:
        if key in data2:
            total_items += 1
            if data1[key] != data2[key]:
                difference_count += 1
                wrong_file.write(f"{key}: {data1[key]} (file1) - {data2[key]} (file2)\n")

# Calculate the ratio of differing items to total items.
if total_items == 0:
    difference_ratio = 0.0
else:
    difference_ratio = (total_items - difference_count) / total_items

print(f"Number of differing items: {difference_count}")
print(f"Total items compared: {total_items}")
print(f"Difference ratio: {difference_ratio:.2%}")
