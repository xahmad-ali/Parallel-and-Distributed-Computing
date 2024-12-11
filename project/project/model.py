# import os
# import pandas as pd
# import re
# from concurrent.futures import ThreadPoolExecutor, as_completed

# def search_in_chunk(chunk, file_path, keywords):
#     """Search for keywords in a chunk of rows."""
#     results = []
#     for index, row in chunk.iterrows():
#         for column, value in row.items():
#             for keyword in keywords:
#                 if re.search(keyword, str(value), re.IGNORECASE):
#                     results.append((file_path, index, column, value))
#     return results

# #####################################################
# def process_file(file_path, keywords, chunk_size=10):
#     """Process a file by dividing it into chunks and searching each chunk."""
#     results = []
#     try:
#         df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
#         total_rows = len(df)
#         chunks = [df.iloc[i:i + chunk_size] for i in range(0, total_rows, chunk_size)]

#         # Create threads for chunks
#         with ThreadPoolExecutor(max_workers=min(len(chunks), 4)) as executor:
#             future_to_chunk = {executor.submit(search_in_chunk, chunk, file_path, keywords): chunk for chunk in chunks}
#             for future in (future_to_chunk): #as_completed
#                 chunk_results = future.result()
#                 if chunk_results:
#                     results.extend(chunk_results)
#     except Exception as e:
#         print(f"Error processing file {file_path}: {e}")
#     return results

# ########################################
# def process_files_dynamically(file_list, keywords):
#     """Process multiple files dynamically based on their size."""
#     all_results = []

#     # Calculate max threads based on number and size of files
#     total_chunks = 0
#     for file in file_list:
#         df = pd.read_excel(file) if file.endswith('.xlsx') else pd.read_csv(file)
#         total_chunks += len(df) // 10 + 1

#     max_threads = min(total_chunks, os.cpu_count() * 2)  # Set a sensible limit based on system cores
#     print(f"Using up to {max_threads} threads.")

#     with ThreadPoolExecutor(max_workers=max_threads) as executor:
#         future_to_file = {executor.submit(process_file, file, keywords): file for file in file_list}
#         for future in (future_to_file): #as_completed
#             file_results = future.result()
#             if file_results:
#                 all_results.extend(file_results)
#     return all_results

# ####################################################
# def generate_excel_file(results, output_path="search_results.xlsx"):
#     """Generate an Excel file from the search results."""
#     try:
#         # Prepare data for the Excel file
#         data = [{
#             "File": file,
#             "Row": row,
#             "Column": column,
#             "Value": value
#         } for file, row, column, value in results]

#         # Create a DataFrame and write to Excel
#         df = pd.DataFrame(data)
#         df.to_excel(output_path, index=False)
#         print(f"Results saved to {output_path}")
#     except Exception as e:
#         print(f"Error generating Excel file: {e}")

# ####################################################
# if __name__ == "__main__":
#     # Prompt user for input
#     print("Enter the paths to Excel or CSV files, separated by commas (e.g., file1.xlsx,file2.csv):")
#     input_files = input().strip()
#     file_list = [file.strip() for file in input_files.split(',') if os.path.isfile(file)]
#     print("Enter the keywords to search for, separated by commas (e.g., keyword1,keyword2):")
#     keywords = [keyword.strip() for keyword in input().split(',')]

#     if not file_list or not keywords:
#         print("Invalid input. Please provide files and keywords.")
#         exit(1)

#     print("\nSearching for keywords in files...")
#     results = process_files_dynamically(file_list, keywords)

#     if results:
#         print("\nSearch Results:")
#         for file, row, column, value in results:
#             print(f"File: {file}, Row: {row}, Column: {column}, Match: {value}")
        
#         # Generate Excel file from results
#         generate_excel_file(results)
#     else:
#         print("No matches found.")

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
                matching_rows.append(row)
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
    return all_matching_rows

def generate_new_file(rows, output_path="filtered_rows.xlsx"):
    """Generate a new Excel file with the matching rows."""
    try:
        df = pd.DataFrame(rows)
        df.to_excel(output_path, index=False)
        print(f"Filtered rows saved to {output_path}")
    except Exception as e:
        print(f"Error generating the output file: {e}")

if __name__ == "__main__":
    # Prompt user for input
    print("Enter the paths to Excel or CSV files, separated by commas (e.g., file1.xlsx,file2.csv):")
    input_files = input().strip()
    file_list = [file.strip() for file in input_files.split(',') if os.path.isfile(file)]
    print("Enter the keywords to search for, separated by commas (e.g., keyword1,keyword2):")
    keywords = [keyword.strip() for keyword in input().split(',')]

    if not file_list or not keywords:
        print("Invalid input. Please provide files and keywords.")
        exit(1)

    print("\nSearching for keywords in files...")
    matching_rows = process_files_dynamically(file_list, keywords)

    if matching_rows:
        print(f"\n{len(matching_rows)} matching rows found.")
        
        # Save matching rows to a new file
        generate_new_file(matching_rows)
    else:
        print("No matching rows found.")
