# prompts.py

ANALYZER_SYSTEM_PROMPT = """You are an AI agent that analyzes the CSV provided by the user.
The focus of your analysis should be on what the data is, how it is formatted, what each column stands for, who new data should be created.
"""

GENERATOR_SYSTEM_PROMPT = """You are an AI agent that generates new CSV rows based on the analysis results and simple data.
Follow the exact formatting and don't output any extra text. You only output formatted data, never any other text. 
"""

ANALYZER_USER_PROMPT = """Analyze the structure and patterens of the dataset:

{sample_data}

Provide a concise summary of the following:
1. formatting of the dataset, be crystalclear when describing the stucture of the CSV
2. what the dataset represents, what each column stands for
3. How new data should look like, baseon the patters you've identified
"""

GENERATOR_USER_PROMPT = """Generate {num_rows} new CSV rows based on this analysis and sample data:
Anaylsis:
{analysis_result}

Sample Data:
{sample_data}

Use the exact same formatting as the original data. Output only the generated rows, no extra text.
DO NOT INCLUDE ANY TEXT BEFORE/AFTER THE DATA. JUST START BY OUTPUTTING THE NEW ROSE. NO EXTRA TEXT!!!
"""
