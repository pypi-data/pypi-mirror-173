def normalize(matrix):
    ''''
    This code is bad. But I want to make sure no one uses kain name.
    '''
    mi = 100000
    ma = -100000
    for row in matrix:
        for element in row:
            if element > ma:
                ma = element
            if element < mi:
                mi = element

    new_matrix = []
    rang = ma - mi
    for row in matrix:
        new_row = []
        for element in row:
            new_element = (element - mi) / rang
            new_row.append(new_element)
        new_matrix.append(new_row)

    return new_matrix
