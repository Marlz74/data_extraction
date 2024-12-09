import pandas as pd
import whois
import asyncio
import os
import time

# Asynchronous function to query WHOis details with retry
async def get_whois_details(domain, retries=1):
    try:
        # Attempt to get WHOis data
        details = whois.whois(domain)
        
        # Format the result and replace None with 'N/A'
        return {
            "Domain": domain,
            "Created Date": details.creation_date if details.creation_date else 'N/A',
            "Updated Date": details.updated_date if details.updated_date else 'N/A',
            "Expiry Date": details.expiration_date if details.expiration_date else 'N/A',
            "Name Servers": ", ".join(details.name_servers) if details.name_servers else 'N/A'
        }
    except Exception as e:
        print(f"Error fetching WHOis details for {domain}: {e}")
        
        # Retry logic
        if retries > 0:
            print(f"Retrying for {domain}...")
            time.sleep(1)  # Optional delay between retries
            return await get_whois_details(domain, retries=retries - 1)
        
        # Return 'N/A' for all fields if connection fails after retry
        return {
            "Domain": domain,
            "Created Date": 'N/A',
            "Updated Date": 'N/A',
            "Expiry Date": 'N/A',
            "Name Servers": 'N/A'
        }

# Process a single chunk file
async def process_chunk_file(chunk_file, output_file):
    try:
        print(f"Starting to process chunk: {chunk_file}")
        # Load the chunk
        df = pd.read_csv(chunk_file)
        domains = df["Domain"].tolist()

        # Gather WHOis details asynchronously
        results = await asyncio.gather(*(get_whois_details(domain) for domain in domains))

        # Convert results to DataFrame
        output_df = pd.DataFrame(results)

        # Save to output file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        output_df.to_csv(output_file, index=False)
        print(f"Finished processing chunk: {chunk_file}")
        print(f"WHOis data saved to {output_file}")
    except Exception as e:
        print(f"Error processing {chunk_file}: {e}")

# Main function
async def main():
    # List of chunk files to process
    chunk_files = ["chunks/a.csv"]  # Replace with your selected chunk files

    # Directory to save WHOis results
    output_dir = "whois_results"

    # Process each chunk file
    tasks = []
    for chunk_file in chunk_files:
        output_file = os.path.join(output_dir, os.path.basename(chunk_file).replace("chunk", "whois"))
        tasks.append(process_chunk_file(chunk_file, output_file))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
