import csv
import json
import requests
import time

# Replace with your actual API key
API_KEY = 'at_aVj3zvbWdWX4pi55klEQeIIWRWosd'

# Input and output file paths
input_csv_path = 'urls.csv'
output_csv_path = 'output_whois_data.csv'

# Rate limit constants
MAX_REQUESTS_PER_SECOND = 50  # API limit
WAIT_TIME = 1 / MAX_REQUESTS_PER_SECOND  # Time to wait between requests

# Function to get WHOIS data for a given domain
def get_whois_data(domain):
    url = f'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={API_KEY}&domainName={domain}&outputFormat=JSON'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for {domain}. Status code: {response.status_code}")
        return None

# Read input CSV file
with open(input_csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    # Skip header if there is one
    next(reader, None)
    
    # Prepare output CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Domain', 'NameServers', 'Updated Date', 'Created Date', 'Expiry Date'])
        
        for i, row in enumerate(reader):
            domain = row[0]  # Assuming the domain name is in the first column
            data = get_whois_data(domain)
            
            if data and 'WhoisRecord' in data:
                record = data['WhoisRecord']
                domain_name = record.get('domainName', 'N/A')
                name_servers = ', '.join(record.get('nameServers', {}).get('hostNames', []))
                updated_date = record.get('updatedDate', 'N/A')
                created_date = record.get('createdDate', 'N/A')
                expiry_date = record.get('expiresDate', 'N/A')
                
                # Write to output CSV
                writer.writerow([domain_name, name_servers, updated_date, created_date, expiry_date])
            
            # Add delay after every request to respect API rate limit
            if (i + 1) % MAX_REQUESTS_PER_SECOND == 0:
                print(f"Rate limit reached. Waiting for {WAIT_TIME} seconds...")
                time.sleep(WAIT_TIME)

print(f"WHOIS data has been written to {output_csv_path}")
