import pandas as pd
import numpy as np
import scipy.stats as stats

# Load the dataset
file_path = 'C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/results/refined_MC-LARC/test_results/summary_with_image_before.csv'
data = pd.read_csv(file_path)

# Extract the relevant columns for analysis
results = data.iloc[:, 2:]

# Calculate the mean for each trial
means = results.mean(axis=0)

# Calculate the standard error of the mean (SEM) for each trial
sem = stats.sem(results, axis=0)

# Calculate the variance for each trial
variance = results.var(axis=0, ddof=1)

# Calculate the 95% confidence intervals
confidence_interval = 1.96 * sem
lower_bound = means - confidence_interval
upper_bound = means + confidence_interval

# Create a DataFrame to display the results
analysis_results = pd.DataFrame({
    'Trial': results.columns,
    'Mean': means,
    'Variance': variance,
    'Lower Bound (95% CI)': lower_bound,
    'Upper Bound (95% CI)': upper_bound
})

# Display the results
print(analysis_results)


data = pd.read_csv(file_path)

# 정답 여부를 나타내는 열들만 선택 (첫 두 열 제외)
correct_columns = data.columns[2:]

# 각 열에 대한 정답률 계산
accuracy_data = data[correct_columns].sum() / len(data) * 100

# 평균 정답률 계산
mean_accuracy = np.mean(accuracy_data)

# 표준편차 계산
std_dev = np.std(accuracy_data, ddof=1)

# 분산 계산 (표준편차 제곱)
variance_accuracy = std_dev ** 2

# 표준오차 계산
std_err = std_dev / np.sqrt(len(accuracy_data))

# 95% 신뢰구간 계산
confidence_interval = stats.t.interval(0.95, len(accuracy_data) - 1, loc=mean_accuracy, scale=std_err)

# 결과 출력
print(f'Mean accuracy of five repeated experiments: {mean_accuracy:.3f}%')
print(f'Variance of accuracy: {variance_accuracy:.3f}')
print(f'95% Confidence Interval: {confidence_interval[0]:.3f}% ~ {confidence_interval[1]:.3f}%')
