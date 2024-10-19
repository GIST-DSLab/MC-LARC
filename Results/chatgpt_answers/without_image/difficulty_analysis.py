import pandas as pd

# Load the CSV file
file_path = 'new_merged_correct_wrong.csv'
df = pd.read_csv(file_path)

# 난이도 그룹 확인
difficulty_groups = df['difficulty'].value_counts().sort_index()

# 각 문제의 정확도를 계산
df['average_correct'] = df[['Correct(1) / Wrong(0)_1', 'Correct(1) / Wrong(0)_2', 'Correct(1) / Wrong(0)_3', 'Correct(1) / Wrong(0)_4', 'Correct(1) / Wrong(0)_5']].mean(axis=1)

# 각 난이도별 정확도 계산
difficulty_accuracy = df.groupby('difficulty')['average_correct'].mean()

# 각 난이도별로 맞춘 문제 수를 계산
df['total_correct'] = df[['Correct(1) / Wrong(0)_1', 'Correct(1) / Wrong(0)_2', 'Correct(1) / Wrong(0)_3', 'Correct(1) / Wrong(0)_4', 'Correct(1) / Wrong(0)_5']].sum(axis=1)
difficulty_correct = df.groupby('difficulty')['total_correct'].sum() / 5

# 전체 정확도 계산
total_tasks = df.shape[0]
total_correct_answers = df['total_correct'].sum()
overall_accuracy = total_correct_answers / (total_tasks * 5)

# 데이터프레임으로 정리하고 소수점 3자리까지 반올림
difficulty_groups_df = pd.DataFrame({
    "Number of Tasks": difficulty_groups,
    "Total Correct": difficulty_correct,
    "Average Accuracy": difficulty_accuracy.round(3) * 100
})

# 전체 정확도를 포함한 행 추가
difficulty_groups_df.loc['Overall'] = [total_tasks, total_correct_answers / 5, round(overall_accuracy, 3)]

# 결과 출력
print(difficulty_groups_df)
