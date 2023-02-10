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
        matrix = []
        def __init__(self):
            for index in range(4):
                self.matrix.append([])
                for num in range(4):
                    self.matrix[index].append(0)
        def set_list_matrix(self, lst):
            for index in range(len(lst)):
                self.set_item(index // 4, index % 4, lst[index])

        def set_single_matrix(self, num):
            for row in range(4):
                for col in range(4):
                    self.set_item(row, col, num)
        def set_item(self, row, col, item):
            self.matrix[row][col] = item
        def get_item(self, row, col):
            return self.matrix[row][col]

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
        return

    #find the magnitude of a vector
    def magnitude(self, v1):
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

    #determine if two matrices are the same
    def m_is_equal(self, m1, m2):
        return

    #multipy a matrix by a matrix.  Return the matrix
    def m_multiply(self, m1, m2):
        return

    #multiply a vector by a matrix and return the vector
    def cross_multiply(self, v, m):
        return

    #add matrices and return a matrix
    def m_add(self, m1, m2):
        return

    #subtract matrices and return a matrix
    def m_sub(self, m1, m2):
        return