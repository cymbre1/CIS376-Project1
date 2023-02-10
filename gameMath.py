class GameMath():

     # Has 3 coordinates
    class Vector2():
        w = 0
        x = 0
        y = 0

    # Has 4 coordinates
    class Vector3(): 
        w = 0
        x = 0
        y = 0
        z = 0
    
    # Data structure for 4x4 matrices
    class Matrix():
        def __init__(self):
            self.matrix = []
            for index in range(4):
                self.matrix.append([])
                for num in range(4):
                    if index == num:
                        self.matrix[index].append(1)
                    else:
                        self.matrix[index].append(0)
        def set_list_matrix(self, lst):
            for index in range(len(lst)):
                self.set_item(index // 4, index % 4, lst[index])

        def set_single_matrix(self, num):
            for row in range(4):
                for col in range(4):
                    self.set_item(row, col, num)

        def copy_matrix(self, m):
            for row in range(4):
                for col in range(4):
                    self.set_item(row, col, m.get_item(row, col))

        def set_item(self, row, col, item):
            self.matrix[row][col] = item

        def get_item(self, row, col):
            return self.matrix[row][col]

        # determine if two matrices are the same
        def is_equal(self, m):
            for row in range(4):
                for col in range(4):
                    if self.get_item(row, col) != m.get_item(row, col):
                        return False
            return True

        # multipy a matrix by a matrix.  Return the matrix
        def multiply(self, m):
            newM = Matrix()
            for row in range(4):
                for col in range(4):
                    total = 0
                    for index in range(4):
                        total += self.get_item(row, index) * m.get_item(index, col)
                    newM.set_item(row, col, total)
            return newM

        # add matrices and return a matrix
        def m_add(self, m):
            newM = Matrix()
            for row in range(4):
                for col in range(4):
                    newM.set_item(row, col, (self.get_item(row, col) + (m.get_item(row, col))))
            return newM

        # subtract matrices and return a matrix
        def m_sub(self, m):
            newM = Matrix()
            for row in range(4):
                for col in range(4):
                    newM.set_item(row, col, (self.get_item(row, col) - m.get_item(row, col)))
            return newM

    # Calculate the cross product and return a vector
    # Params:
    # Vector2 or Vector3 vec1
    # Vector2 or Vector3 vec2
    # Returns a Vector
    def crossProduct(self, vec1, vec2):
        lastParam = (vec1.z * vec2.z) if hasattr(vec1, 'z') and hasattr(vec2, 'z') else 0
        print("filler")


    # Calculate the dot product and return a scalar value
    # Params:
    # Vector2 or Vector3 vec1
    # Vector2 or Vector3 vec2
    # Returns a scalar value
    def dotProduct(self, vec1, vec2):
        lastParam = (vec1.z * vec2.z) if hasattr(vec1, 'z') and hasattr(vec2, 'z') else 0
        return (vec1.w * vec2.w) + (vec1.x * vec2.x) + (vec1.y * vec2.y) + lastParam

    #determine if two vectors have the same values
    def v_is_equal(self, v1, v2):
        if not hasattr(v1, 'z') ^ hasattr(v2, 'z'):
            if v1.w == v2.w and v1.x == v2.x and v1.y == v2.y:
                if hasattr(v1, 'z'):
                    if v1.z == v2.z:
                        return True
                    else:
                        return False
                else:
                    return True
        else:
            return False

    #find the magnitude of a vector
    def magnitude(self, v):
        (v.w * v.w).sqrt()
        return

    #normalize a vector
    def normalize(self, v):
        return

    #add two vectors
    def v_add(self, v1, v2):
        return

    #subtract two vectors
    def v_sub(self, v1, v2):
        return

    #calculate the angle between two vectors
    def find_angle(self, v1, v2):
        return


    #multiply a vector by a matrix and return the vector
    def cross_multiply(self, v, m):
        return

