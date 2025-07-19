
def get_rhythmic_resultant_from_generators(*generators: int, cp: int): 
    """
    This method creates arrays of '0' (rests) and '1' (beats) for multiple monomial periodicities.
    Then combines all rhythmic patterns dropping them perpendicularly
    Args:
        *generators: variable number of integer generators
        cp (int): common period
    Returns:
        array: rhythmic resultant of all periodicities
    """
    arrays = [generate_rhythm_str(gen, cp) for gen in generators]
    return merge_rhythmical_strings(arrays);

def merge_rhythmical_strings(*rhythms):
    return [1 if any(x == 1 for x in values) else 0 
            for values in zip(*rhythms)]

def generate_rhythm_str(gen: int, cp: int):
    return [int(i % gen == 0) for i in range(cp)]
    
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

def generate_fractioning_from_min_gen(a: int, b: int, indexes: list):
    arr = []
    max_len = a * a
    rhythm_len = a * b

    for index in indexes:
        group = [0] * index if index != 0 else []
        group[index:index] = generate_rhythm_str(b, rhythm_len)
        
        if len(group) > max_len: break

        group += [0] * (max_len - len(group))  #adds '0' until end of sequence if needed
        arr.append(group)

    return arr