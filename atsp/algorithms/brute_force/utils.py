def permutations(elements):
    size = len(elements)
    if size <= 1:
        yield elements
    else:
        first_element, rest = elements[0], elements[1:]
        for permutation in permutations(rest):
            yield from _single_permutation(permutation, first_element)


def _single_permutation(elements, item):
    for i in range(len(elements) + 1):
        yield elements[:i] + [item] + elements[i:]
