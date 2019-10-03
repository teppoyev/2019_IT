import numpy as np


def get_proper_fraction(split_ratio, eps=1e-6):

    # convert decimal fraction to proper fraction (numerator and denominator)

    is_reversed = False
    if split_ratio > 1:
        split_ratio = 1 / split_ratio
        is_reversed = True
    a = 1
    b = 1
    _a = a
    _b = b
    k = 1
    i = 0
    while i < 32768:
        _a = k * a
        _b = k * b + 1
        i += 1
        while _a / _b - split_ratio > 0:
            _b += 1
        if _a / _b - split_ratio > -eps:
            if is_reversed:
                return _b, _a
            else:
                return _a, _b
        _b -= 1
        if _a / _b - split_ratio < eps:
            if is_reversed:
                return _b, _a
            else:
                return _a, _b
        k += 1
    if is_reversed:
        return _b, _a
    else:
        return _a, _b


def get_indices(N, n_batches, split_ratio):

    # get the minimum length of the segment that we can split into subsegment with integer length

    a, b = get_proper_fraction(split_ratio)
    length = a + b
    if length < N:

        # find the integer coefficients that we will use to calculate suitable length of segment

        p_up = np.int(np.floor((N - 1) / length)) # we need this to find maximal length of segment we can use
        p_down = np.int(np.ceil((N - 1) / (length * n_batches))) # we need this to cover the whole segment using n_batches segment

        # We try to find suitable length of the segment.
        # We know that last segment ends with N - 1, so it begins with (N - 1) - (length * p_cur), where
        # length * p_cur is current length we consider.
        # As first segment begins with 0 and last segment begins with (N - 1) - (length * p_cur) and
        # the beginning of all segments is located at an equal distance from each other,
        # we know that this distance is ((N - 1) - (length * p_cur)) / (n_batches - 1) and it should be integer.
        # Therefore, we try to find p_cur so this distance is integer.

        min = n_batches
        for p_cur in range(p_down, p_up + 1):
            res = ((N - 1) - (length * p_cur)) % (n_batches - 1)
            if res < min:
                min = res

        # if minimal remainder is null then we can get absolutely correct answer,
        # Otherwise, there will be an rounding error.

        if min == 0:
            print("The exact answer: ")
        else:
            print("The approximate answer: ")

        # find all coefficient we can use to get as good the answer as possible

        p_good = []
        for p_cur in range(p_down, p_up + 1):
            res = ((N - 1) - (length * p_cur)) % (n_batches - 1)
            if res == min:
                p_good.append(p_cur)

        # I use middle element of all suitable coefficients array.
        # Obviously you can use any of them

        ind = np.int(np.ceil(len(p_good) / 2)) - 1
        length = p_good[ind] * length

    else:

        # If we have too big meaning of a + b then we can't get exact answer anyway

        coef = 0.75
        print("The approximate answer: ")
        length = np.int(np.trunc(N * coef))

    # The generator

    inds = np.array([0, length / (1 + split_ratio), length])
    for i in range(n_batches):
        yield np.array(np.rint(inds), dtype=int)
        inds += ((N - 1) - length) / (n_batches - 1)


def main():
    for inds in get_indices(100, 5, 0.25):
        print(inds)
    # expected result for (100, 5, 0.25):
    # [0, 44, 55]
    # [11, 55, 66]
    # [22, 66, 77]
    # [33, 77, 88]
    # [44, 88, 99]


if __name__ == "__main__":
    main()
