import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from scipy.stats import ttest_rel

# Function to perform t-test on the given dataframe with corrected column names
def perform_t_test(df, distance_column, correct_columns):
    # Calculate correct rate
    df['correct_rate'] = df[correct_columns].mean(axis=1)

    # Calculate correct sum
    df['correct_sum'] = df[correct_columns].sum(axis=1)

    # Group by correct sum
    low_correct_rate = df[df['correct_sum'] <= 3]
    high_correct_rate = df[df['correct_sum'] >= 4]

    # Perform t-test
    t_stat, p_value = ttest_ind(low_correct_rate[distance_column], high_correct_rate[distance_column], equal_var=False)
    
    # Return t-test results
    return {'t-statistic': t_stat, 'p-value': p_value}

# Load the CSV files
file_path_jaccard_with_image = 'jaccard_distance_after_revised.csv'
file_path_levenshtein_with_image = 'levenshtein_distance_after_revised.csv'
file_path_jaccard_no_image = 'jaccard_distance_after_revised_without_image.csv'
file_path_levenshtein_no_image = 'levenshtein_distance_after_revised_without_image.csv'

df_jaccard_with_image = pd.read_csv(file_path_jaccard_with_image)
df_levenshtein_with_image = pd.read_csv(file_path_levenshtein_with_image)
df_jaccard_no_image = pd.read_csv(file_path_jaccard_no_image)
df_levenshtein_no_image = pd.read_csv(file_path_levenshtein_no_image)

# Perform t-tests on the datasets
correct_columns_with_image = [
    'Correct(1) / Wrong(0)_1', 'Correct(1) / Wrong(0)_2', 
    'Correct(1) / Wrong(0)_3', 'Correct(1) / Wrong(0)_4', 
    'Correct(1) / Wrong(0)_5'
]

correct_columns_no_image = [
    'Correct(1) / Wrong(0)_other', 'Correct(1) / Wrong(0)_other.1', 
    'Correct(1) / Wrong(0)_other.2', 'Correct(1) / Wrong(0)_other.3', 
    'Correct(1) / Wrong(0)_other.4'
]

t_test_results_jaccard_with_image = perform_t_test(df_jaccard_with_image, 'Average_distance', correct_columns_with_image)
t_test_results_levenshtein_with_image = perform_t_test(df_levenshtein_with_image, 'Average_distance', correct_columns_with_image)

t_test_results_jaccard_no_image = perform_t_test(df_jaccard_no_image, 'Average_distance', correct_columns_no_image)
t_test_results_levenshtein_no_image = perform_t_test(df_levenshtein_no_image, 'Average_distance', correct_columns_no_image)

# Compile all results
t_test_results = {
    'Jaccard_with_image': t_test_results_jaccard_with_image,
    'Levenshtein_with_image': t_test_results_levenshtein_with_image,
    'Jaccard_no_image': t_test_results_jaccard_no_image,
    'Levenshtein_no_image': t_test_results_levenshtein_no_image
}

print(t_test_results)


# Extract t-statistics and p-values for with images and without images
t_stats_with_images = np.array([t_test_results['Jaccard_with_image']['t-statistic'], 
                                t_test_results['Levenshtein_with_image']['t-statistic']])
t_stats_without_images = np.array([t_test_results['Jaccard_no_image']['t-statistic'], 
                                   t_test_results['Levenshtein_no_image']['t-statistic']])

p_values_with_images = np.array([t_test_results['Jaccard_with_image']['p-value'], 
                                 t_test_results['Levenshtein_with_image']['p-value']])
p_values_without_images = np.array([t_test_results['Jaccard_no_image']['p-value'], 
                                    t_test_results['Levenshtein_no_image']['p-value']])

# Perform paired t-test on t-statistics
t_stat_ttest, p_value_ttest = ttest_rel(t_stats_with_images, t_stats_without_images)

# Perform paired t-test on p-values
t_stat_pvalues, p_value_pvalues = ttest_rel(p_values_with_images, p_values_without_images)

# Compile results
paired_t_test_results = {
    't_stat_ttest': {'t-statistic': t_stat_ttest, 'p-value': p_value_ttest},
    'p_value_ttest': {'t-statistic': t_stat_pvalues, 'p-value': p_value_pvalues}
}

print()
print()
print(paired_t_test_results)