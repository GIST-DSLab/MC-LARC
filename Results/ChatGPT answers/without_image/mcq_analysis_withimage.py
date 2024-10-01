import pandas as pd
import numpy as np
from scipy.stats import f_oneway
from scipy.stats import pointbiserialr

# Load the dataset
file_path = 'summary_without_image.csv'
data = pd.read_csv(file_path)

# 전처리: 응시 데이터만 추출
response_data = data.drop(columns=['task_id', 'task_name'])

# 1. KR-20 (Kuder-Richardson 20) 계산
def calculate_kr20(df):
    k = df.shape[1]
    p = df.mean(axis=0)
    q = 1 - p
    pq = p * q
    variance = df.sum(axis=1).var()
    kr20 = (k / (k - 1)) * (1 - pq.sum() / variance)
    return kr20

kr20 = calculate_kr20(response_data)

# 2. Cronbach's alpha 계산
def calculate_cronbach_alpha(df):
    item_variances = df.var(axis=0, ddof=1)
    total_variance = df.sum(axis=1).var(ddof=1)
    n_items = df.shape[1]
    cronbach_alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
    return cronbach_alpha

cronbach_alpha = calculate_cronbach_alpha(response_data)

# 3. ANOVA 테이블 생성
def calculate_anova_table(df):
    # 각 문항을 그룹으로 나눠서 ANOVA 수행
    f_statistic, p_value = f_oneway(*[df[col] for col in df.columns])
    return f_statistic, p_value

anova_f_statistic, anova_p_value = calculate_anova_table(response_data)

# 결과 출력 (소수점 셋째 자리까지 반올림)
print(f"KR-20: {round(kr20, 3)}")
print(f"Cronbach's alpha: {round(cronbach_alpha, 3)}")
print(f"ANOVA F-statistic: {round(anova_f_statistic, 3)}")
print(f"ANOVA p-value: {round(anova_p_value, 3)}")
