def check_index(y):
    """
    Helper recursive function that finds that receives as an input
    the string, and finds the first point where it became imbalanced.
    It returns the index of that point.
    :param y: our list
    :return: the place of the index that causes the first imbalance
    """
    if not is_balanced(y):
        return check_index(y[0:-1])
    return len(y)


def is_balanced(s):
    """This function checks whether a string is balanced (has proper
    parentheses). It receives a string as an input and returns True if
    it is balanced, False if it isn't.
    :param s: Our string
    :return: True or False
    """
    # set our variables to recognize open and closed parentheses
    opened = "("
    closed = ")"
    # set our counter that counts the parentheses
    open_counter = 0
    closed_counter = 0
    # for loop that goes over each character and updates our counter if it
    # finds a parentheses.
    for i in s:
        if i == opened:
            open_counter += 1
        elif i == closed:
            closed_counter += 1
        # if clause that checks whether there are more closed than open
        # and returns false, before going over all of them
        if closed_counter > open_counter:
            return False
    # if clause that checks at the end if there are unmatched parentheses
    # and returns false
    if open_counter != closed_counter:
        return False
    # if none of the previous cases were found, the function returns True
    return True


def violated_balanced(s):
    """Function that receives a string and checks whether it is balanced,
    and if it isn't, checks whether it is fixable. It returns -1 for a
    balanced string. It returns the length of the string if it is possible
    to completely balance it. And it returns an index number if it is
    possible to balance it up to that index.

    :param s: our string
    :return: -1 if balanced, index of imbalance or length of string if not
    """

    # Set our variables to recognize parentheses
    opened = "("
    closed = ")"

    # clause that checks if the string is balanced,if it already is returns -1
    if is_balanced(s):
        return -1

    # call the check_index function and save it into the variable place
    place = check_index(s)

    # clauses that check which character caused the imbalance and returns
    # either the index of that place or the length of the list
    if s.find(opened) > s.find(closed) and s.find(closed) != -1:
        return place
    elif s[place] == opened:
        return len(s)
    elif s[place] == closed:
        if s[0:place + 1].count(opened) > s[0:place + 1].count(closed):
            return len(s)
        elif s[0:place + 1].count(opened) < s[0:place + 1].count(closed):
            return place


def match_brackets(s):
    """Function that checks whether the string is balanced, if it isn't
    returns an empty list. If it is balanced then for every pair of
    parentheses returns the difference of their indexes."""
    # set our variables to recognize open and closed parentheses
    opened = "("
    closed = ")"
    # set the variable of characters that aren't parentheses
    not_closer = 0
    # create a list that has 0's the length of the string
    result = [not_closer] * len(s)
    # set our counter variable
    place_counter = -1
    # check if string is not balanced. It it isn't, returns an empty list
    if not is_balanced(s):
        return []


    def seperate(s, p):
        """
        Recursive helper function that receives a string and our counter
        and runs a recursive algorithm that updates our list to include the
        right numbers based on the indexes it finds. It returns the list
        :param s: our string
        :param p: counter for iterations
        :return: our finished list : result
        """
        # our base case when the string is empty, return 0
        if len(s) == 0:
            return result
        # raise our counter by 1, and restart our in function counters
        p += 1
        close_count, open_count = 0, 0
        # for loop the length of our string, that counts open and closed
        # parentheses
        for i in range(len(s)):
            if s[i] == opened:
                open_count += 1
            elif s[i] == closed:
                close_count += 1
                # if it finds a closed parentheses before a closed, recall
                # the function without the first character
            if close_count > open_count:
                return seperate(s[1:], p)
            # if we find a pair of matched parentheses, updates our list and
            #  calls the function without the first character.
            elif close_count == open_count:
                if s[0] == opened:
                    result[p] = i
                    result[i+p] = -i
                return seperate(s[1:], p)
    # call and return our helper function seperate().
    return seperate(s, place_counter)




