#############################################################
# FILE : ex7.py
# WRITER : Dan Kufra , dan_kufra ,
# EXERCISE : intro2cs ex7
# DESCRIPTION:
# This program receives two images, a number of frames and the size of an
# image and morphs them from the first image to the second.
#############################################################

from SolveLinear3 import solve_linear_3


def is_point_inside_triangle(point, v1, v2, v3):
    """
    This function receives a point and the three vertices of a triangle and
    calls the solve_linear_3() function to find out if the point is inside
    the triangle or outside.
    :param point: coordinate we want to check
    :param v1: first vertex of the triangle
    :param v2: second vertex of the triangle
    :param v3: third vertex of the triangle
    :return: True if point is inside the triangle, False if outside
    """
    # set our coefficient variable to make a list of 3 lists, with each list
    # including the parameters of a linear equation.
    # set 2 variables to represent the different coordinate indexes
    X_CORD = 0
    Y_CORD = 1
    coefficients = [[v1[X_CORD], v2[X_CORD], v3[X_CORD]], [v1[Y_CORD],
                    v2[Y_CORD], v3[Y_CORD]], [1, 1, 1]]
    # set a list of 3 parameters that represent the answer to each equation
    right_hand = [point[X_CORD], point[Y_CORD], 1]
    # set our variables a, b ,c to be the elements of the tuple returned by
    # the solve_linear_3 function
    a, b, c = solve_linear_3(coefficients, right_hand)
    # check whether the point is inside the triangle, returns False if not,
    # True if yes.
    if a < 0 or b < 0 or c < 0:
        return False, (a, b, c)
    else:
        return True, (a, b, c)


def create_triangles(list_of_points):
    """
    Function that receives a list of points and converts each point to a
    list of triangles. By deciding whether a point is in an existing
    triangle, and if it is splits it into 3 triangles and deletes it.
    :param list_of_points: A list that contains tuples of 2 elements which
    represent the coordinates of triangle vertices.
    :return: A list of tuples, with each tuple containing 3 tuples that
    represent the vertices of triangles. Each vertex is a tuple with 2
    elements representing the coordinates.
    """
    # append our first 2 triangles to a list. These triangles are the ones
    # created by the corners of the image.
    triangles = [(list_of_points[0], list_of_points[1], list_of_points[2]),
                 (list_of_points[0], list_of_points[2], list_of_points[3])]
    num_point_default = 4
    length_coordinates = len(list_of_points)
    length_list = len(triangles)


    # for loop that goes over the rest of the coordinates in the given list.
    for i in range(num_point_default, length_coordinates):
        # for loop that takes a coordinate in the given list, and checks
        # whether it is inside a triangle in the list we created
        for j in range(length_list):
            # if it is inside the list, appends the new triangles created to
            # our list and removes the old one
            if is_point_inside_triangle(list_of_points[i], triangles[j][0],
                                        triangles[j][1], triangles[j][2])[0]:
                triangles.append((list_of_points[i], triangles[j][0],
                                  triangles[j][1]))
                triangles.append((list_of_points[i], triangles[j][1],
                                  triangles[j][2]))
                triangles.append((list_of_points[i], triangles[j][0],
                                  triangles[j][2]))
                triangles.pop(j)
                break
    # The function returns our list of triangles when we are done
    return triangles


def get_triangle_of_point(point, triangles_list):
    """
    Function that finds the triangle that a point is in.
    :param point: tuple containing coordinates of a point
    :param triangles_list: list containing tuples of 3 triangle vertexes
    with each vertex tuple containing tuples of 2 that represent their
    coordinates
    :return: the index of the triangle the point is in, and a, b, c found
    from calling is_point_inside_triangle()
    """
    length_list = len(triangles_list)
    # Loop that goes over triangles list and finds the triangle the point is in
    for i in range(length_list):
        # set variable result to be the parameters returned by
        # is_point_inside_triangle()
        result = is_point_inside_triangle(point, triangles_list[i][0],
                                          triangles_list[i][1],
                                          triangles_list[i][2])
        # check whether the zero index in result is True, if it is return a
        # tuple containing the index of the triangle the point is in, and a,
        # b,c from the is_point_inside_triangle()
        if result[0]:
            return i, result[1][0], result[1][1], result[1][2]


def do_triangle_lists_match(list_of_points1, list_of_points2):
    """
    Function that checks whether all the triangles created by 2 list of points
    match .
    :param list_of_points1: List of points marked in image 1
    :param list_of_points2: List of points marked in image 2
    :return: True if their indexes match, False if they don't
    """
    length = len(list_of_points1)
    # create 2 lists, one for each list of points given by using our
    # create_triangles_for_one_image() function
    triangle_list1 = create_triangles(list_of_points1)
    triangle_list2 = create_triangles(list_of_points2)
    # loop over the indexes in the lists and check whether they match using
    # our get_triangle_of_point function
    for i in range(length):
        # if they don't match at any point return False
        if get_triangle_of_point(list_of_points1[i], triangle_list1)[0] != \
                get_triangle_of_point(list_of_points2[i], triangle_list2)[0]:
            return False
    # if they all match, return True
    return True


def get_point_in_segment(p1, p2, alpha):
    """
    Function receives 2 points and a float and finds the point on the line
    segment between the 2 points using the float
    :param p1: First point
    :param p2: Second Point
    :param alpha: divider
    :return: v: the dividing point
    """
    X_CORD = 0
    Y_CORD = 1
    # set our coordinates to the proper value
    v1 = ((1 - alpha) * p1[X_CORD]) + (alpha * p2[X_CORD])
    v2 = ((1 - alpha) * p1[Y_CORD]) + (alpha * p2[Y_CORD])
    v = (v1, v2)
    return v


def get_intermediate_triangles(source_triangles_list, target_triangles_list,
                               alpha):
    """
    Function receives 2 lists of triangles and finds the intermediate
    triangles between them by using a given dividing point.
    :param source_triangles_list: list of tuples of 3 tuples with each one
    representing a pair of coordinates in a triangle
    :param target_triangles_list: list of tuples of 3 tuples with each one
    representing a pair of coordinates in a triangle
    :param alpha: our divider on the segments between each point
    :return: list of middle triangles between our source and target triangles
    """
    # create an empty list we will append to
    length = len(source_triangles_list)
    middle_triangle_list = []
    # loop that iterates over the triangle lists and finds the middle triangles
    for i in range(length):
        # set our points by calling the get_point_in_segment() function to
        # the appropriate index.
        point1 = get_point_in_segment(source_triangles_list[i][0],
                                      target_triangles_list[i][0], alpha)
        point2 = get_point_in_segment(source_triangles_list[i][1],
                                      target_triangles_list[i][1], alpha)
        point3 = get_point_in_segment(source_triangles_list[i][2],
                                      target_triangles_list[i][2], alpha)
        # set the intermediate triangle to be the 3 points found
        intermediate_triangle = (point1, point2, point3)
        # append the triangle to our list
        middle_triangle_list.append(intermediate_triangle)
    # return our list of intermediate triangles.
    return middle_triangle_list


# until here should be submitted by next week - 18.12.2014


def get_array_of_matching_points(size, triangles_list,
                                 intermediate_triangles_list):
    """
    Function receives a size and 2 lists of triangles, and creates an array
    of points that match the triangles in both list.
    :param size: size of our array
    :param triangles_list: list of tuples of 3 elements with each tuple
    being a vertex of a triangle holding coordinates to that vertex
    :param intermediate_triangles_list: list of tuples of 3 elements with each
    tuple being a vertex of a triangle holding coordinates to that vertex
    :return: array : an array of tuples which include (x_tag,y_tag) coordinates
    """
    # set our length variables to the size of the array
    length_x = size[0]
    length_y = size[1]
    # set 2 variables to represent the different coordinate indexes
    X_CORD = 0
    Y_CORD = 1

    # create our empty array
    array = [[] for k in range(length_x)]
    # set our counter to 0 for the first iteration
    first_iteration = True
    # for loop that goes over every point in our array and appends the right
    # numbers to each point
    for i in range(length_x):
        # loop within our main loop that goes over each column in the row
        for j in range(length_y):
            # set our point to be a tuple of (row, column)
            point = (i, j)
            # check whether this is the first iteration we are doing,
            # if it is then find the index and a, b, c of the point in the
            # intermediate triangles
            if first_iteration:
                index_of_triangle, a, b, c = get_triangle_of_point(point,
                                                intermediate_triangles_list)
                first_iteration = False
            # if it isn't the first iteration, but the point is in a new
            # triangle, find the new index and a,b ,c
            elif not is_point_inside_triangle(point, old[0], old[1],
                                              old[2])[0]:
                index_of_triangle, a, b, c = get_triangle_of_point(point,
                                            intermediate_triangles_list)
            # if it is in the previous triangle, keep the index and find the
            #  a, b, c without going over the whole list.
            else:
                result = is_point_inside_triangle(point,
                        intermediate_triangles_list[index_of_triangle][0],
                        intermediate_triangles_list[index_of_triangle][1],
                        intermediate_triangles_list[index_of_triangle][2])[1]
                a, b, c = result[0], result[1], result[2]

            # set our vertex coordinates to be the coordinates of the
            # vertices in the matching triangle in triangles_list
            v1x = triangles_list[index_of_triangle][0][X_CORD]
            v2x = triangles_list[index_of_triangle][1][X_CORD]
            v3x = triangles_list[index_of_triangle][2][X_CORD]
            v1y = triangles_list[index_of_triangle][0][Y_CORD]
            v2y = triangles_list[index_of_triangle][1][Y_CORD]
            v3y = triangles_list[index_of_triangle][2][Y_CORD]
            # set x_tag and y_tag to be the correct points using our equation
            x_tag = (a * v1x) + (b * v2x) + (c * v3x)
            y_tag = (a * v1y) + (b * v2y) + (c * v3y)
            # array_point is a tuple of x_tag and y_tag
            array_point = (x_tag, y_tag)
            # we insert the tuple into the proper spot in the array
            array[i].insert(j, array_point)
            # save our old triangle so we can be more efficient in iterations
            old = intermediate_triangles_list[index_of_triangle]
    return array


def create_intermediate_image(alpha, size, source_image, target_image,
                              source_triangles_list, target_triangles_list):
    '''
    Function that takes our two images and returns an array of the
    intermediate RGB values for each pixel at a given point between them.
    :param alpha: our divider, a float between 0 and 1
    :param size: The size of our images
    :param source_image: RGB values for each pixel in the source image
    :param target_image: RGB values for each pixel in the target image
    :param source_triangles_list: list of triangles in our source image
    :param target_triangles_list: list of triangles in our target image
    :return: an array of RGB values at the intermediate points between both
    images
    '''
    # set our size variables of the array
    length_x = size[0]
    length_y = size[1]
    # create an empty array that we will append to
    image = [[] for k in range(length_x)]
    # call our get_intermediate_triangles function and get a list of
    # intermediate triangles using our source list
    inter_list = get_intermediate_triangles(source_triangles_list,
                                            target_triangles_list, alpha)
    # call our get_array_of_matching_points function and set our variables
    # to those lists
    match_source = get_array_of_matching_points(size, source_triangles_list,
                                                inter_list)
    match_target = get_array_of_matching_points(size, target_triangles_list,
                                                inter_list)
    # for loop that iterates over the lists and inserts the proper RGB
    # values into our array
    for i in range(length_x):
        for j in range(length_y):
            # set our match_point variables to the proper point in each list
            source_match_point = match_source[i][j]
            target_match_point = match_target[i][j]
            # use the source_image and target_image functions to find our
            # RGB values in each one
            source_RGB = source_image[source_match_point]
            target_RGB = target_image[target_match_point]
            # calculate the desired intermediate RGB value for the point
            image_R = int(((1 - alpha) * source_RGB[0]) + (alpha *
                                                    target_RGB[0]))
            image_G = int(((1 - alpha) * source_RGB[1]) + (alpha *
                                                    target_RGB[1]))
            image_B = int(((1- alpha) * source_RGB[2]) + (alpha *
                                                    target_RGB[2]))
            image_RGB = (image_R, image_G, image_B)
            # insert those values into the array
            image[i].insert(j, image_RGB)
    # return our completed array
    return image


def create_sequence_of_images(size, source_image, target_image,
                              source_triangles_list, target_triangles_list,
                              num_frames):
    """
    Function that creates a sequence of frames using our previous functions
    :param size: size of each image
    :param source_image: our starting image
    :param target_image: our target image
    :param source_triangles_list: list of triangles from our source image
    :param target_triangles_list: list of triangles from our target image
    :param num_frames: number of frames to create a sequence out of
    :return: image_sequence : a list of images the length of num_frames
    """
    # create an empty list
    image_sequence = []
    # iterate over the number of frames and create an image for each frame
    for i in range(num_frames):
        # set alpha to equal the proper value
        alpha = (i/(num_frames - 1))
        # create our new image using our create_intermediate_image function
        new_image = create_intermediate_image(alpha, size, source_image,
                                              target_image,
                                              source_triangles_list,
                                              target_triangles_list)
        # append the new image to the list
        image_sequence.append(new_image)
    # return the list when done iterating over the frames
    return image_sequence



# until here should be submitted by 25.12.2014


