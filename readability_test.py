import csv
import readability
# Define a function to calculate the readability score
def calculate_readability_score(contents):
    # Tokenize the content by separating each token with a space and each sentence with a newline
    tokenized_contents = ' '.join(contents.split())  # Separate tokens by spaces
    tokenized_contents = tokenized_contents.replace('. ', '.\n')  # Separate sentences by newlines

    # Calculate the readability score
    results = readability.getmeasures(tokenized_contents, lang='en')

    return results

# Define the path to the policy names CSV file
policy_names_file = 'policy_names.csv'

# Read the file names from the CSV file
file_names = []
with open(policy_names_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        file_names.append(row[0])

# Open the output CSV file
output_file = 'readability_results.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['File Name', 'Readability Score'])

    # Process each file
    for file_name in file_names:
        # Open the file
        with open(file_name, 'r', encoding='utf-8') as file:
            # Read the file contents
            contents = file.read()

            # Calculate the readability score
            results = calculate_readability_score(contents)

            # Write the result to the CSV file
            # Format the results into a string
            result_string = ', '.join(f"{key}: {value}" for key, value in results.items())

            # Write the result to the CSV file
            writer.writerow([file_name, result_string])
            