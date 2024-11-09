from multiprocessing import Pool

def calculate_square(n):
    return n * n

if __name__ == "__main__":
    numbers = range(1, 1000) 

    with Pool() as pool:
        results = pool.map(calculate_square, numbers)

    print("Finished calculating squares for numbers 1 to 10 million.")
    print(results)
