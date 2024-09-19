import pandas as pd
import os

# Read the CSV file
df = pd.read_csv('docs/equipment/assets_by_category/User Selection List.csv', encoding='utf-8')

# Filter only active assets and where 'Asset Type' is 0 and any of 'Year 1', 'Year 2', or 'Year 3' is 'Yes'
df = df[(df['Active'] == 'Yes') & (df['Asset Type'] == 0) & ((df['Year 1'] == 'Yes') | (df['Year 2'] == 'Yes') | (df['Year 3'] == 'Yes'))]

# Replace 'Yes' with checkmark and 'No' with empty string in relevant columns
df[['Year 1', 'Year 2', 'Year 4', 'Selected']] = df[['Year 1', 'Year 2', 'Year 4', 'Selected']].replace({'Yes': '&#10003;', 'No': ''}, regex=True)

# Search through the categories for microphones, if there is a match, ignore case, ignore NaNs and replace with just 'Microphones'
df.loc[df['Category'].str.contains('microphone', case=False, na=False), 'Category'] = 'Microphones'

# Replace NaN values in 'Asset Description' with empty string
df.fillna({'Asset Description':''}, inplace=True)

# Replace single line breaks with double line breaks in 'Asset Description'
df['Asset Description'] = df['Asset Description'].str.replace('\n', '\n\n')

# Define function to format Markdown table
def format_markdown_table(data):
    markdown_table = '|'.join(data.columns) + '\n'
    markdown_table += '|'.join(['---'] * len(data.columns)) + '\n'
    for index, row in data.iterrows():
        markdown_table += '|'.join(row) + '\n'
    return markdown_table

# Create a directory to store Markdown files if it doesn't exist
output_dir = 'docs/equipment/assets_by_category'
os.makedirs(output_dir, exist_ok=True)

# Write data to separate Markdown files for each category
for category, group in df.groupby('Category'):
    category_file_path = os.path.join(output_dir, f'{category}.md')
    with open(category_file_path, 'w', encoding='utf-8') as file:
        file.write(f'# {category}\n\n')
        for index, row in group.iterrows():
            # Write asset heading
            file.write(f'## {row["Asset Name"]}\n\n')
            # Write table of years with access
            file.write(format_markdown_table(row[['Year 1', 'Year 2', 'Year 4']].to_frame().T) + '\n')
            # Write asset description
            file.write(f'{row["Asset Description"]}\n\n')
