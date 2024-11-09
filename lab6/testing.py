import multiprocessing
from multiprocessing import Process, Pool
import math

# Function to calculate factorial of a number (used by Process class)
def calculate_factorial(number):
    print(f"Factorial of {number} is {math.factorial(number)}")

# Function to calculate the sum of a range of numbers (used by Pool class)
def calculate_sum(start, end):
    total = sum(range(start, end + 1))
    print(f"Sum of numbers from {start} to {end} is {total}")
    return total

if __name__ == "__main__":
    # Step 1: Using Process class to calculate factorials in parallel
    numbers = [5, 7, 10]  # Numbers for which we will calculate the factorial
    processes = []
    
    # Create and start a process for each number
    for number in numbers:
        process = Process(target=calculate_factorial, args=(number,))
        processes.append(process)
        process.start()
    
    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("\nFinished calculating factorials using Process class.")

    # Step 2: Using Pool class to calculate the sum of ranges in parallel
    ranges = [(1, 10), (20, 30), (35, 45)]  # Ranges to calculate the sum
    with Pool(3) as pool:
        results = pool.starmap(calculate_sum, ranges)

    print(f"\nTotal sum of all ranges: {sum(results)}")
    print("Finished calculating sums using Pool class.")
