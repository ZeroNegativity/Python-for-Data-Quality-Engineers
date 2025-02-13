import random

def bubble_sort(arr):
    """
    Sorts a list in ascending order using the Bubble Sort algorithm.

    Args:
        arr (list): List of integers to be sorted.

    Returns:
        None: The list is sorted in place.

    Examples:
        >>> numbers = [5, 2, 9, 1, 5, 6]
        >>> bubble_sort(numbers)
        >>> numbers
        [1, 2, 5, 5, 6, 9]

        >>> numbers = [3, 3, 3, 3, 3]
        >>> bubble_sort(numbers)
        >>> numbers
        [3, 3, 3, 3, 3]
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def calculate_average(numbers):
    """
    Calculates the average of a list of numbers.

    Args:
        numbers (list): List of integers.

    Returns:
        float: The average value. Returns 0 if the list is empty.

    Examples:
        >>> calculate_average([2, 4, 6, 8, 10])
        6.0

        >>> calculate_average([1, 3, 5, 7, 9])
        5.0

        >>> calculate_average([])
        0
    """
    return sum(numbers) / len(numbers) if numbers else 0

if __name__ == "__main__":
    # Generate a list of 100 random numbers between 0 and 1000
    random_numbers = [random.randint(0, 1000) for _ in range(100)]

    # Sorting the list using bubble sort
    bubble_sort(random_numbers)

    # Separating even and odd numbers
    even_numbers = [num for num in random_numbers if num % 2 == 0]
    odd_numbers = [num for num in random_numbers if num % 2 != 0]

    # Calculating averages
    avg_even = calculate_average(even_numbers)
    avg_odd = calculate_average(odd_numbers)

    # Printing the results
    print(f"Average of even numbers: {avg_even}")
    print(f"Average of odd numbers: {avg_odd}")

    # Run doctests
    import doctest
    doctest.testmod()
