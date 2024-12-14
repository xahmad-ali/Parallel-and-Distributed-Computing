import os
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

def search_in_chunk(chunk, file_path, keywords):
    """Search for keywords in a chunk of rows and return matching rows."""
    matching_rows = []
    for index, row in chunk.iterrows():
        for value in row.values:
            if any(re.search(keyword, str(value), re.IGNORECASE) for keyword in keywords):
                # Convert row to dictionary, replacing NaN with None
                row_dict = row.to_dict()
                for key, val in row_dict.items():
                    if pd.isna(val):  # Check for NaN
                        row_dict[key] = None
                matching_rows.append(row_dict)
                break  # Skip checking other values in this row if a match is found
    return matching_rows



def process_file(file_path, keywords, chunk_size=10):
    """Process a file by dividing it into chunks and searching for matching rows."""
    matching_rows = []
    try:
        df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
        total_rows = len(df)
        chunks = [df.iloc[i:i + chunk_size] for i in range(0, total_rows, chunk_size)]

        # Create threads for chunks
        with ThreadPoolExecutor(max_workers=min(len(chunks), 4)) as executor:
            future_to_chunk = {executor.submit(search_in_chunk, chunk, file_path, keywords): chunk for chunk in chunks}
            for future in future_to_chunk:
                chunk_results = future.result()
                if chunk_results:
                    matching_rows.extend(chunk_results)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return matching_rows


def process_files_dynamically(file_list, keywords):
    """Process multiple files dynamically based on their size and search for matching rows."""
    all_matching_rows = []

    # Calculate max threads based on number and size of files
    total_chunks = 0
    for file in file_list:
        df = pd.read_excel(file) if file.endswith('.xlsx') else pd.read_csv(file)
        total_chunks += len(df) // 10 + 1

    max_threads = min(total_chunks, os.cpu_count() * 2)  # Set a sensible limit based on system cores
    print(f"Using up to {max_threads} threads.")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_file = {executor.submit(process_file, file, keywords): file for file in file_list}
        for future in future_to_file:
            file_results = future.result()
            if file_results:
                all_matching_rows.extend(file_results)
    # print(all_matching_rows)
    return all_matching_rows

# process_files_dynamically(file_list, keywords)




def generate_new_file(rows, output_path="filtered_rows.xlsx"):
    """Generate a new Excel file with the matching rows."""
    try:
        df = pd.DataFrame(rows)
        df.to_excel(output_path, index=False)
        print(f"Filtered rows saved to {output_path}")
    except Exception as e:
        print(f"Error generating the output file: {e}")

