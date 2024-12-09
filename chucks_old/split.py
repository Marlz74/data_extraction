import csv

def split_file(input_file, output_prefix, batch_size):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        urls = [row['Domain'] for row in reader if 'Domain' in row and row['Domain'].strip()]
    
    total_files = (len(urls) + batch_size - 1) // batch_size  # Calculate number of files
    for i in range(total_files):
        chunk = urls[i * batch_size:(i + 1) * batch_size]
        output_file = f"{output_prefix}_{i + 1}.csv"
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=['Domain'])
            writer.writeheader()
            for url in chunk:
                writer.writerow({'Domain': url})
        print(f"Created: {output_file} with {len(chunk)} entries.")

# Example usage:
split_file('../urls.csv', 'urls_chunk', batch_size=10000)
