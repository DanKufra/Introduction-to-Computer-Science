#############################################################
# FILE : ex5.py
# WRITER : Dan Kufra , dan_kufra ,
# EXERCISE : intro2cs ex5
# DESCRIPTION:
# The function receives a data set, and a label categorizing it and returns
# a linear separator for that data set.
#############################################################
"""
implement the methods below (replace the pass statement with the code),
and add their docstrings.
"""


def find_sign(number):
    """Function that receives a number as a parameter (usually the dot
    function of two lists) and decides whether it is negative or positive"""
    if number > 0:
        return 1.0
    elif number < 0:
        return -1.0
    else:
        return 0


def dot(A, B):
    """Function that finds the sum of the multiplication of 2 lists of 2
    vectors"""
    dot_total = 0
    for j in range(len(A)):
        dot_total += A[j]*B[j]
    return dot_total


def perceptron(data, labels):
    """ Function that finds the linear separator of a list of points on a graph
    using the perceptron algorithm. It receives as parameters the list of
    points and their corresponding labels"""
    # set two variables w = our weighted vector, and b = our bias
    w = [0 for x in range(len(data[0]))]
    b = 0
    # counter set to 0,if over maximum allowed iterations no separator exists
    iteration_counter = 0
    # set our variable found_linear to a boolean value of False
    found_linear = False
    # Loop that runs our algorithm until the linear separator is found or
    # iterations pass the allowed amount.
    while (not found_linear) and (iteration_counter != 10 * len(data)):
        # set our found_linear to True, if one isn't found it changes to False
        found_linear = True
        # for loop that runs the perceptron algorithm
        for i in range(len(data)):
            #clause that decides whether label matches our dot function - b
            if find_sign(dot(data[i], w) - b) != float(labels[i]):
                # if an error is found set the found_linear value to False
                found_linear = False
                # loop that updates our weight vector
                for k in range(len(w)):
                    w[k] = w[k] + (labels[i] * data[i][k])
                # update our bias
                b -= labels[i]
        # add 1 to our iteration counter
        iteration_counter += 1
    # if/elif decide what to return based on if a linear separator was found
    if found_linear:
        return w, b

    elif not found_linear:
        return None, None


def generalization_error(data, labels, w, b):
    """Function that recieves a data set, label, a weight and a bias for a
    linear separator and returns a list of errors that this separator finds"""
    # set an empty list
    errors = []
    # loop that goes over the list, runs our algorithm and appends 1 for an
    # error and 0 for a correct point to the list.
    for i in range(len(data)):
        if find_sign(dot(data[i], w) - b) != labels[i]:
            errors.append(1)
        else:
            errors.append(0)
    return errors


def vector_to_matrix(vec):
    """function that receives a vector and returns a matrix of lists from
    that vector."""
    # set the desired length of each list in the matrix
    desired_length = int(len(vec) ** .5)
    # set the matrix to be a list of empty lists
    matrix = [[] for x in range(desired_length)]
    # set the starting matrix index to 0
    matrix_index = 0
    # loop that goes over the inputted vector, and appends the matrix's lists
    for i in range(len(vec)):
            matrix[matrix_index].append(vec[i])
            if len(matrix[matrix_index]) == desired_length:
                matrix_index += 1
    return matrix


def classifier_4_7(data, labels):
    """Function that receives a data list and label list and calls the
    perceptron function. It returns a list w of 784 vectors and a bias."""
    return perceptron(data, labels)


def test_4_7(train_data, train_labels, test_data, test_labels):
    """Function that receives as parameters our training data and labels,
    saves the result as our weight and bias. Runs our generaliztion_error
    function using that w and b and our test data and test labels. And
    finally returns the w, b and how many errors occurred."""
    w, b = classifier_4_7(train_data, train_labels)
    errors = generalization_error(test_data, test_labels, w, b)
    if w is not None and b is not None:
        return errors
    elif w is None and b is None:
        return None, None, None


