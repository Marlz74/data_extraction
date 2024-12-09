import pandas as pd
from ast import literal_eval
from datetime import datetime

# Function to format datetime values
def format_date(value):
    try:
        if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
            # Convert list-like strings to Python lists
            parsed_list = literal_eval(value)
            # Format each datetime object in the list
            return ", ".join(datetime.strftime(date, "%Y-%m-%d %H:%M:%S") for date in parsed_list)
        elif isinstance(value, str):
            # Convert single string datetime to a formatted string
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, datetime):
            # Format datetime objects
            return value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return "N/A"
    except Exception:
        return "N/A"

# Load CSV
input_file = "whois_results/a.csv"  # Replace with your input file path
output_file = "dateoutput.csv"  # Replace with your output file path

# Read the CSV file
df = pd.read_csv(input_file)

# Apply formatting to each relevant column
columns_to_format = ["Created Date", "Updated Date", "Expiry Date"]  # Specify columns to format
for column in columns_to_format:
    df[column] = df[column].apply(format_date)

# Save the reformatted DataFrame to a new CSV
df.to_csv(output_file, index=False)
print(f"Reformatted data saved to {output_file}")
