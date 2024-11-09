import re
from concurrent.futures import ProcessPoolExecutor
import tkinter as tk
from tkinter import filedialog, messagebox

def search_chunk(lines_with_numbers, pattern):
    """Searches for the pattern in a chunk of lines, and includes line numbers."""
    matches = []
    for line_number, line in lines_with_numbers:
        if re.search(pattern, line, re.IGNORECASE):  # Case-insensitive search
            matches.append(f"{line_number}: {line.strip()}")  # Format with line number
    return matches

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

# UI Functions
def select_files():
    file_paths = filedialog.askopenfilenames(title="Select Files", filetypes=[("Text Files", "*.txt")])
    file_list_box.delete(0, tk.END)
    for file_path in file_paths:
        file_list_box.insert(tk.END, file_path)

def search_pattern():
    pattern = pattern_entry.get()
    if not pattern:
        messagebox.showerror("Input Error", "Please enter a search pattern.")
        return

    file_paths = list(file_list_box.get(0, tk.END))
    if not file_paths:
        messagebox.showerror("Input Error", "Please select at least one file.")
        return

    results = parallel_search(file_paths, pattern)
    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, results)

# Setting up the main window
root = tk.Tk()
root.title("Parallel Text Search")
root.geometry("800x600")

# UI Elements
frame = tk.Frame(root)
frame.pack(pady=10)

# File Selection
file_list_label = tk.Label(frame, text="Selected Files:")
file_list_label.grid(row=0, column=0, sticky="w")

file_list_box = tk.Listbox(frame, width=80, height=5, selectmode=tk.MULTIPLE)
file_list_box.grid(row=1, column=0, padx=5, pady=5)

select_files_button = tk.Button(frame, text="Select Files", command=select_files)
select_files_button.grid(row=1, column=1, padx=5)

# Pattern Entry
pattern_label = tk.Label(frame, text="Search Pattern:")
pattern_label.grid(row=2, column=0, sticky="w")

pattern_entry = tk.Entry(frame, width=50)
pattern_entry.grid(row=3, column=0, padx=5, pady=5)

# Search Button
search_button = tk.Button(frame, text="Search", command=search_pattern)
search_button.grid(row=3, column=1, padx=5)

# Results Box
results_label = tk.Label(root, text="Search Results:")
results_label.pack(anchor="w", padx=10)

results_text = tk.Text(root, wrap="word", width=95, height=20)
results_text.pack(padx=10, pady=5)

# Run the UI event loop
root.mainloop()
