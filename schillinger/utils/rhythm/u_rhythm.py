
def get_rhythmic_resultant(a: int, b: int): 
    """
    This method creates an array of '0' (rests) and '1' (beats) for a monomial periodicity.
    Then combines the two rhythmic patterns dropping the first resultant perpendicularly
    Args:
        a (int) : major generator
        b (int) : minor generator
    Returns:
        array: rhytmic resultants of the two periodicities
    """
    array_a = []
    array_b = []

    for i in range(a * b):
        array_a.append(1 if i % a == 0 else 0)
        array_b.append(1 if i % b ==  0 else 0)

    return [1 if x == 1 or y == 1 else 0 for x, y in zip(array_a, array_b)]    

def split_in_measures(cont: list, measure_length: int):
    """
    This method splits the given sequence of '0' and '1' into sub-arrays (eq. to bars), 
    each bar being equal to measure_length
    Args:
        cont (list of list of int): the given rhythmic continuity
        measure_length (int): number of beats per bar
    Returns:
        cont: original continuity now divided in sub-arrays (bars)
    """
    return [cont[i:i + measure_length] for i in range(0, len(cont), measure_length)]

def replace_rests(sequence: list):
    """
    This method adds consecutive rests (0s) to the previous beat value,
    creating a rhythmic continuity where rests extend the previous note duration.
    Example:
        Input:  [1,0,0,1,0,0,1]
        Output: [3,3,1]
    Args:
        sequence (list): a list of 0s and 1s representing beats and rests
    Returns:
        list: sequence where rests are added to previous beat duration
    """
    result = []
    i = 0
    while i < len(sequence):
        if sequence[i] == 1:
            count = 1
            # Count consecutive zeros after this beat
            while i + count < len(sequence) and sequence[i + count] == 0:
                count += 1
            result.append(count)
            i += count
        else:
            i += 1  # Skip initial rests
    
    return result

