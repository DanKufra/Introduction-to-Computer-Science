# import the turtle module
import turtle


def draw_tree(length=200):
    """
    Function the receives a parameter "length" ( the default is 200) and
    draws a recursive tree with the turtle function where each branch is .6
    the size of the previous one.
    :param length: the length of the first branch
    :return: None
    """
    # our base case where the recursive function is stopped
    if length < 10:
        return
    # our main tree branch drawer, we move forward the size of the current
    # branch and turn 30 degrees right
    turtle.forward(length)
    turtle.right(30)
    # we call the function again with a smaller length until we reach a
    # branch that is too small
    draw_tree(length * 0.6)
    # when we reach the branch that is too small, we turn 60 degrees left
    turtle.left(60)
    # if the branch is still too small, this function returns nothing and we
    #  turn 30 degrees right and start moving backwards up the tree.
    draw_tree(0.6 * length)
    turtle.right(30)
    turtle.backward(length)
