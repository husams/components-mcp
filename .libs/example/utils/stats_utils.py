"""Statistics utility functions."""

from typing import List


def calculate_stats(numbers: List[float]) -> dict:
    """
    Calculate basic statistics from a list of numbers.
    
    Args:
        numbers: List of numerical values
    
    Returns:
        Dictionary containing mean, median, min, max, and count
    
    Examples:
        >>> calculate_stats([1, 2, 3, 4, 5])
        {'mean': 3.0, 'median': 3, 'min': 1, 'max': 5, 'count': 5}
    """
    if not numbers:
        return {
            'mean': 0,
            'median': 0,
            'min': 0,
            'max': 0,
            'count': 0
        }
    
    sorted_nums = sorted(numbers)
    count = len(numbers)
    mean = sum(numbers) / count
    
    # Calculate median
    if count % 2 == 0:
        median = (sorted_nums[count // 2 - 1] + sorted_nums[count // 2]) / 2
    else:
        median = sorted_nums[count // 2]
    
    return {
        'mean': mean,
        'median': median,
        'min': min(numbers),
        'max': max(numbers),
        'count': count
    }
