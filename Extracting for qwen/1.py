# Importing necessary libraries
import pandas as pd

file_path = '/kaggle/input/sad-juice-2/resultlst-7.csv'

# Reading the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# # Print the 'Predicted Answer' column
# print("Predicted Answer Column:")
# print(df['Predicted Answer'])

# Print the first row of the 'Predicted Answer' column
print("First row of the 'Predicted Answer' column:")
print(df['Predicted Answer'].iloc[1])



# Count the occurrences of the sentence "End of thought process"
sentence_to_count = "End of thought process"
count = df['Predicted Answer'].str.contains(sentence_to_count, na=False).sum()

print(f'The sentence "{sentence_to_count}" appears {count} times in the "Predicted Answer" column.')

















