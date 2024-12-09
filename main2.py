import whois
import csv

# Read URLs from a file
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

# Open CSV file for writing
with open('whois_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Domain Name', 'Registrar', 'Creation Date', 'Expiration Date', 'Name Servers']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for url in urls:
        try:
            w = whois.whois(url)
            writer.writerow({
                'Domain Name': w.domain_name,
                'Registrar': w.registrar,
                'Creation Date': w.creation_date,
                'Expiration Date': w.expiration_date,
                'Name Servers': ', '.join(w.name_servers) if w.name_servers else ''
            })
        except Exception as e:
            print(f"Error retrieving data for {url}: {e}")

print("Data extraction complete. CSV file saved as whois_data.csv.")
