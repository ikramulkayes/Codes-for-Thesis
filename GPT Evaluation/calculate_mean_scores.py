# This script calculates mean similarity scores for contextual and parametric answers from a CSV file.


import pandas as pd
import numpy as np
import re

def extract_percentage_value(score_str):
    """
    Extract numerical percentage value from similarity score string.
    Returns None if the score is invalid or empty.
    """
    if pd.isna(score_str) or str(score_str).strip() == '':
        return None
    
    # Convert to string and remove any extra whitespace
    score_str = str(score_str).strip()
    
    # Extract percentage using regex
    percentage_match = re.search(r'(\d+(?:\.\d+)?)%?', score_str)
    if percentage_match:
        try:
            return float(percentage_match.group(1))
        except ValueError:
            return None
    
    return None

def has_nan_parametric_answer(answer_text):
    """
    Check if the Answer column contains both 'parametric answer: nan' AND 'contextual answer: nan'
    """
    if pd.isna(answer_text):
        return True
    
    answer_str = str(answer_text).lower()
    # Check for both "parametric answer: nan" AND "contextual answer: nan" patterns
    has_parametric_nan = 'parametric answer: nan' in answer_str
    has_contextual_nan = 'contextual answer: nan' in answer_str
    
    # Return True if both are nan (meaning we should exclude this row)
    return has_parametric_nan and has_contextual_nan

def calculate_mean_scores(csv_file_path):
    """
    Calculate mean scores for Contextual and Parametric similarity,
    excluding rows with 'parametric answer: nan' in the Answer column.
    """
    print(f"Loading CSV file: {csv_file_path}")
    
    # Load the CSV file
    df = pd.read_csv(csv_file_path)
    
    print(f"Total rows in dataset: {len(df)}")
    
    # Filter out rows with 'parametric answer: nan'
    valid_rows_mask = ~df['Answer'].apply(has_nan_parametric_answer)
    valid_df = df[valid_rows_mask].copy()
    
    print(f"Rows with both 'parametric answer: nan' AND 'contextual answer: nan' excluded: {len(df) - len(valid_df)}")
    print(f"Valid rows for evaluation: {len(valid_df)}")
    
    # Extract numerical values from similarity scores
    valid_df['Contextual_Score'] = valid_df['Contextual Similarity'].apply(extract_percentage_value)
    valid_df['Parametric_Score'] = valid_df['Parametric Similarity'].apply(extract_percentage_value)
    
    # Count rows with valid scores
    contextual_valid_count = valid_df['Contextual_Score'].notna().sum()
    parametric_valid_count = valid_df['Parametric_Score'].notna().sum()
    both_valid_count = (valid_df['Contextual_Score'].notna() & valid_df['Parametric_Score'].notna()).sum()
    
    print(f"\nScore availability:")
    print(f"Rows with valid Contextual Similarity scores: {contextual_valid_count}")
    print(f"Rows with valid Parametric Similarity scores: {parametric_valid_count}")
    print(f"Rows with both valid scores: {both_valid_count}")
    
    # Calculate mean scores
    contextual_mean = valid_df['Contextual_Score'].mean()
    parametric_mean = valid_df['Parametric_Score'].mean()
    
    # Calculate overall mean (average of both contextual and parametric)
    overall_scores = []
    for idx, row in valid_df.iterrows():
        contextual_score = row['Contextual_Score']
        parametric_score = row['Parametric_Score']
        
        if pd.notna(contextual_score) and pd.notna(parametric_score):
            overall_scores.append((contextual_score + parametric_score) / 2)
    
    overall_mean = np.mean(overall_scores) if overall_scores else None
    
    # Print results
    print(f"\n" + "="*50)
    print(f"EVALUATION RESULTS")
    print(f"="*50)
    print(f"Mean Contextual Similarity Score: {contextual_mean:.2f}%" if pd.notna(contextual_mean) else "Mean Contextual Similarity Score: N/A")
    print(f"Mean Parametric Similarity Score: {parametric_mean:.2f}%" if pd.notna(parametric_mean) else "Mean Parametric Similarity Score: N/A")
    print(f"Overall Mean Score: {overall_mean:.2f}%" if overall_mean is not None else "Overall Mean Score: N/A")
    
    # Additional statistics
    if pd.notna(contextual_mean) and pd.notna(parametric_mean):
        print(f"\nAdditional Statistics:")
        print(f"Contextual Score - Min: {valid_df['Contextual_Score'].min():.1f}%, Max: {valid_df['Contextual_Score'].max():.1f}%, Std: {valid_df['Contextual_Score'].std():.2f}")
        print(f"Parametric Score - Min: {valid_df['Parametric_Score'].min():.1f}%, Max: {valid_df['Parametric_Score'].max():.1f}%, Std: {valid_df['Parametric_Score'].std():.2f}")
    
    # Show some examples of excluded rows
    excluded_df = df[~valid_rows_mask]
    if len(excluded_df) > 0:
        print(f"\nExamples of excluded rows (with both 'parametric answer: nan' AND 'contextual answer: nan'):")
        for i, (idx, row) in enumerate(excluded_df.head(3).iterrows()):
            print(f"Row {idx}: {row['Answer'][:100]}...")
            if i >= 2:  # Show only first 3 examples
                break
    
    # Save detailed results to a file
    results_summary = {
        'Total_Rows': len(df),
        'Excluded_Rows_With_Both_NaN': len(df) - len(valid_df),
        'Valid_Rows': len(valid_df),
        'Contextual_Valid_Count': contextual_valid_count,
        'Parametric_Valid_Count': parametric_valid_count,
        'Both_Valid_Count': both_valid_count,
        'Mean_Contextual_Score': contextual_mean,
        'Mean_Parametric_Score': parametric_mean,
        'Overall_Mean_Score': overall_mean
    }
    
    results_df = pd.DataFrame([results_summary])
    results_file = csv_file_path.replace('.csv', '_evaluation_summary.csv')
    results_df.to_csv(results_file, index=False)
    print(f"\nDetailed results saved to: {results_file}")
    
    return results_summary

if __name__ == "__main__":
    # Specify the path to your CSV file
    csv_file_path = "processed_factual_llama_results_final.csv"
    
    try:
        results = calculate_mean_scores(csv_file_path)
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
        print("Please make sure the file exists in the current directory.")
    except Exception as e:
        print(f"Error processing file: {e}")
