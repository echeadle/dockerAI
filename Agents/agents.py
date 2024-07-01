# agents.py
# importing the necessary libraries 
import numpy as np
import os
import csv
import anthropic
from prompts import (
        ANALYZER_SYSTEM_PROMPT,
        GENERATOR_SYSTEM_PROMPT,
        ANALYZER_USER_PROMPT,
        GENERATOR_USER_PROMPT
)

# Set up the Antropic API key
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Please enter your Anthropic API key: ") # Prompt the user for the API Key
    
    
client = anthropic.Anthropic()
sonnet = "claude-3-5-sonnet-20240620"


# function to read the CSV file from the User
def read_csv(file_path):
    data = []
    with open(file_path, "r",newline="") as csvfile: # Open the CSV file in read mode
       csv_reader = csv.reader(csvfile) # Create a CSV reader object
       for row in csv_reader:
           data.append(row) # Add each row to the data list
    return data

# Function to save the generated data to a new CSV file
def save_to_csv(data, output_file, headers=None):
    mode = 'w' if headers else 'a' # Set the ile mode: 'w'(write) if headers are provided, else 'a' (append)
    with open(output_file, mode, newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers) # write headers if provided
        for row in csv.reader(data.splitlines()):
            writer.writerow(row)
            
            
# Create the Analyzer Agent
def analyzer_agent(sample_data):
    message = client.messages.create(
        model = sonnet,
        max_tokens=400, # Limit the response to 400 tokens
        temperature=0.1, # Set a low temperature for more focused, determisitic output
        system=ANALYZER_SYSTEM_PROMPT, # Use the predefined sample data
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
                # format the user prompt with the provided sample data
            }
        ]
    )
    return message.content[0].text # Return the text content of the first message

# Create the Generator Agent
def generator_agent(analysis_result, sample_data, num_rows=30):
    message = client.messages.create(
        model = sonnet,
        max_tokens=1500, # Allow for longer response (1500 tokens)
        temperature=1, # Set a high temperature for more creative, diverse output
        system=GENERATOR_SYSTEM_PROMPT, # Use the predefined sample data
        messages=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data)
                # format the user prompt with the number of rows to generate.
                # the analysis result, and the sample data
            }
        ]
    )
    return message.content[0].text # Return the text content of the first message

# Main Execution Flow

# Get input from the user
file_path = input("\nEnter the name of your CSV file: ")
file_path = os.path.join('/app/data', file_path)
desired_rows = int(input("Enter the number of rows you want in the new dataset: "))

# Read the sample data from the input CSV file
sample_data = read_csv(file_path)
sample_data_str = "\n".join([",".join(row) for row in sample_data]) # Converts 2D list into a single string

print("\nLaunching Team of Agents")
#Analyze the sample data using the Analyzer Agent
analysis_result = analyzer_agent(sample_data_str)
print("\n### Analyzer Agent output: ###\n")
print(analysis_result)
print("\n-----------------------------------------\n\nGenerating new data....")

# Set up the output file
output_file = "/app/data/data_out.csv"
headers = sample_data[0]
save_to_csv("", output_file, headers)

batch_size = 30
generated_rows = 0

# Generate data in batches until we reach the desired number of rows
while generated_rows < desired_rows:
    # Calculate how many rows to generate in this batch
    rows_to_generate = min(batch_size, desired_rows - generated_rows)
    # Generate a batch of data using the Generator Agent
    generator_data = generator_agent(analysis_result,sample_data_str, rows_to_generate)
    # Append to generaged data to the output file
    save_to_csv(generator_data, output_file)
    # Update the count of generated rows
    generated_rows += rows_to_generate
    # Print progress update
    print(f"Generated {generated_rows} out of {desired_rows}")