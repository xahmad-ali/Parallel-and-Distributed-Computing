import re
from concurrent.futures import ProcessPoolExecutor
from flask import Flask, render_template, request, redirect, url_for, flash
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Function for searching in chunks
def search_chunk(lines_with_numbers, pattern):
    """Searches for the pattern in a chunk of lines, and includes line numbers."""
    matches = []
    for line_number, line in lines_with_numbers:
        if re.search(pattern, line, re.IGNORECASE):  # Case-insensitive search
            matches.append(f"{line_number}: {line.strip()}")  # Format with line number
    return matches

# Function to read files in chunks
def read_file_in_chunks(file_path, chunk_size=100):
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

# Function to search for a pattern in a file in chunks
def search_file_in_chunks(file_path, pattern, chunk_size=100):
    """Splits the file into chunks and searches each chunk for the pattern."""
    matches = []
    chunks = read_file_in_chunks(file_path, chunk_size)

    with ProcessPoolExecutor() as executor:
        threads = [executor.submit(search_chunk, chunk, pattern) for chunk in chunks]
        for thread in threads:
            try:
                chunk_matches = thread.result()  # Get the result from the future
                matches.extend(chunk_matches)  # Add matches to the overall list
            except Exception as e:
                print(f"Error processing chunk in {file_path}: {e}")

    return matches

# Function to perform parallel search across multiple files
def parallel_search(file_paths, pattern, chunk_size=100):
    """Performs parallel search across multiple files, using chunk-based logic."""
    all_matches = []
    with ProcessPoolExecutor() as executor:
        threads = {executor.submit(search_file_in_chunks, path, pattern, chunk_size): path for path in file_paths}
        for thread in threads:
            file_path = threads[thread]
            try:
                matches = thread.result()
                if matches:
                    all_matches.append(f"\nMatches in {file_path}:\n" + "\n".join(matches))
                else:
                    all_matches.append(f"\nNo matches found in {file_path}.\n")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    return "\n".join(all_matches)

# Flask route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to handle file upload and search
@app.route('/search', methods=['POST'])
def search():
    pattern = request.form['pattern']
    if not pattern:
        flash('Please enter a search pattern.')
        return redirect(url_for('index'))

    # Handle file uploads
    uploaded_files = request.files.getlist('files')
    if not uploaded_files:
        flash('Please upload at least one file.')
        return redirect(url_for('index'))

    # Save the uploaded files temporarily and perform the search
    file_paths = []
    for file in uploaded_files:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        file_paths.append(file_path)

    # Perform the search
    results = parallel_search(file_paths, pattern)

    # Remove the uploaded files after searching
    for file_path in file_paths:
        os.remove(file_path)

    return render_template('results.html', pattern=pattern, results=results)

if __name__ == '__main__':
    app.run(debug=True)
