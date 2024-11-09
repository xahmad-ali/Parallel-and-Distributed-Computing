import re
from concurrent.futures import ProcessPoolExecutor

def search_chunk(lines_with_numbers, pattern):
    """Searches for the pattern in a chunk of lines, and includes line numbers."""
    matches = []
    for line_number, line in lines_with_numbers:
        if re.search(pattern, line, re.IGNORECASE):  # Case-insensitive search
            matches.append(f"{line_number}: {line.strip()}")  # Format with line number # remove white spaces
    return matches

#convert the file into chunks
def read_file_in_chunks(file_path, chunk_size):
    """Reads a file in chunks of lines, including line numbers."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line_number = 1
            while True:
                lines_with_numbers = [(line_number + i, file.readline()) for i in range(chunk_size)]
                if not lines_with_numbers[0][1]:  # If the first line is empty, end of file reached
                    break
                yield lines_with_numbers
                line_number += chunk_size
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def search_file_in_chunks(file_path, pattern, chunk_size):
    """Splits the file into chunks and searches each chunk for the pattern."""
    matches = []
    chunks = read_file_in_chunks(file_path, chunk_size)
    # print(chunks)
    # Use ProcessPoolExecutor to process each chunk in parallel
    with ProcessPoolExecutor() as executor:
        threads = [executor.submit(search_chunk, chunk, pattern) for chunk in chunks]
        for thread in threads:
            try:
                chunk_matches = thread.result()  # Get the result from the future
                matches.extend(chunk_matches)    # Add matches to the overall list
            except Exception as e:
                print(f"Error processing chunk in {file_path}: {e}")

    return matches

def parallel_search(file_paths, pattern, chunk_size):
    """Performs parallel search across multiple files, using chunk-based logic."""
    with ProcessPoolExecutor() as executor:
        threads = {executor.submit(search_file_in_chunks, path, pattern, chunk_size): path for path in file_paths}
        for thread in threads:
            file_path = threads[thread]
            try:
                matches = thread.result()
                if matches:
                    print(f"\nMatches in {file_path}:")
                    for match in matches:
                        print("Line where match is found: " + match)
                else:
                    print(f"\nNo matches found in {file_path}.\n")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":

    # pattern = input("enter the pattren you want to search: ")
    pattern = "chin tapak dum dum"
    
    file_paths =[]
    while True:
        # enter name one by one
        file_name = input("Enter name of file with .txt or press 'z' to go for search: \n")
        if file_name == 'z':
            break
        else:
            file_paths.append(file_name)
    
    if len(file_paths) <= 0:
        print("Please enter name of file")
    else:
        parallel_search(file_paths, pattern, chunk_size=5)
    