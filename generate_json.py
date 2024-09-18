import json
import os
import pandas as pd

def generate_json(filepath, output_path):
    # Read tsv file
    df = pd.read_csv(filepath, sep='\t')
    dataset_type = filepath.split('_')[-1].split('.')[0]

    # Select only the 'tweet_text' and 'label_text' columns
    selected_columns = df[['tweet_text', 'label_text']]

    # Remove duplicates
    unique_data = selected_columns.drop_duplicates()

    # Function to create JSON object for each row
    def create_json_object(row):
        label = 1 if row['label_text'] == "informative" else 0
        return {
            "instruction": f"Classify the following tweet for crisis management. Decide if it gives important information that could help during a crisis. Reply with only '1' if the tweet provides useful information, or only '0' if it does not. Tweet: {row['tweet_text']}.",
            "answer": label,
        }

    # Apply the function to each row and create a list of JSON objects
    json_data = [create_json_object(row) for _, row in unique_data.iterrows()]

    # Save the JSON data to a file
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    new_filename = f'{output_path}/{dataset_type}.json'
    with open(new_filename, 'w') as f:
        json.dump(json_data, f, indent=2)

    print(f"JSON data has been saved to {new_filename}")

for tsv_file in ['dataset/task_informative_text_img_dev.tsv',
                 'dataset/task_informative_text_img_train.tsv',
                 'dataset/task_informative_text_img_test.tsv']:
    generate_json(tsv_file, "output_digit_api")
