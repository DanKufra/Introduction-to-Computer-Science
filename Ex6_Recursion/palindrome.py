def is_palindrome_1(s):
    """
    Function that receives a string and checks whether it is a
    palindrome. It returns True if it is, false if it isn't.
    :param s: our string
    :return: True or False
    """
    # Our base case, if we finish running over the whole string then it is a
    #  palindrome and returns True
    if len(s) < 2:
        return True
    elif s[0] == s[-1]:
        # if the index at the beginning of the string and the end are equal,
        #  we return the function without it's first and last index
        return is_palindrome_1(s[1:-1])
    else:
        # if they don't match we know it isn't a palindrome and return False
        return False


def is_palindrome_2(s, i, j):
    """
    Our function receives a string and 2 indexes and checks whether the sub
    string inside those indexes is a palindrome. If it is it returns True,
    if not : False.
    :param s: our string
    :param i: our first
    index
    :param j: our second index
    :return: True or False
    """

    # clause that checks whether the string is empty
    if s == "":
        return True

    # base clause that checks whether the difference between our indexes is
    # greater than 1.
    elif abs(j-i) > 1:
        # if the index difference is greater than 1, and the indexes are
        # equal it returns the function with the next indexes depending on
        # the size of i and j.
        if s[j] == s[i]:
            if j > i:
                return is_palindrome_2(s, i + 1, j - 1)
            else:
                return is_palindrome_2(s, i - 1, j + 1)
        # if the indexes aren't equal, returns False
        else:
            return False
    # if the function went over the whole substring and the last pair of
    # indexes are equal, returns True. Otherwise returns False
    elif s[i] == s[j]:
        return True
    else:
        return False
