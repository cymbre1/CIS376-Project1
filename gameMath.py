import math
class GameMath():

     # Has 3 coordinates, where w is the homogenous value and x and y are the coordinates of the vector
    class Vector2():
        def __init__(self, w = 0, x = 0, y = 0):
            self.w = w
            self.x = x
            self.y = y

        # Calculate the dot product between the current vector and another vector and return a scalar value
        # Params:
        # Vector2 vec2
        # Returns a scalar value
        def dotProduct(self, vec2):
            return (self.x * vec2.x) + (self.y * vec2.y)
        
        #find the magnitude of a vector
        def magnitude(self):
            if self.w == 1:
                return 0
            return math.sqrt((self.x * self.x) + (self.y * self.y))
        
        #add two vectors
        def v_add(self, v):
            return GameMath.Vector2((self.w + v.w) % 2 ,self.x + v.x, self.y + v.y)
        #subtract two vectors
        def v_sub(self, v):
            return GameMath.Vector2((self.w - v.w) % 2 ,self.x - v.x , self.y - v.y)

        # Is this possible?
        def crossProduct(self, v):
            return GameMath.Vector2(self.w * v.w, self.x * v.x, self.y * v.y)
        
        def v_is_equal(self, v):
            return self.w == v.w and self.x == v.x and self.y == v.y

    # Has 4 coordinates, where w  is the homogenous value and x,y, and z are the coordinates of the vector.
    class Vector3(): 
        def __init__(self, w = 0, x = 0, y = 0, z = 0):
            self.w = w
            self.x = x
            self.y = y
            self.z = z

        # Calculate the dot product and return a scalar value
        # Params:
        # Vector3 vec2
        # Returns a scalar value
        def dotProduct(self, vec2):
            return (self.x * vec2.x) + (self.y * vec2.y) + (self.z * vec2.z)

        def crossProduct(self, v2):
            return GameMath.Vector3(0,(self.x * v2.y) - (self.y * v2.x), (self.y * v2.z) - (self.z * v2.y), (self.z * v2.x) - (self.x * v2.z))

    
    # Data structure for 4x4 matrix of numbers
    class Matrix():

        # Constructor for Matrix
        def __init__(self):
            self.matrix = []
            for index in range(4):
                self.matrix.append([])
                for num in range(4):
                    if index == num:
                        self.matrix[index].append(1)
                    else:
                        self.matrix[index].append(0)
        
        # This function sets the matrix based on a 16 length list.
        # Parameters:
        # List lst is the list the matrix is constructed on 
        def set_list_matrix(self, lst):
            for index in range(len(lst)):
                self.set_item(index // 4, index % 4, lst[index])

        # This function sets a matrix of all the same number
        # Parameters:
        # Numerical num is the number that the matrix will contain
        def set_single_matrix(self, num):
            for row in range(4):
                for col in range(4):
                    self.set_item(row, col, num)

        # This function copies a given matrix
        # Parameters:
        # Matrix m is the matrix to be copied
        def copy_matrix(self, m):
            for row in range(4):
                for col in range(4):
                    self.set_item(row, col, m.get_item(row, col))

        # This function prints the current matrix in a more readable format
        '''Weird bug????  sometimes doesn't populate the 3rd row'''
        def print_matrix(self):
            pLine = ''
            for row in range(4):
                for col in range(4):
                    pLine += str(self.get_item(row, col)) + ", "
                pLine += "\n"
            print(pLine)

        # Changes the value at a given matrix location
        # Parameters:
        # int row is the row index of the matrix
        # int col is the column index of the matrix
        # numerical item is the value that the location should become
        def set_item(self, row, col, item):
            self.matrix[row][col] = item

        # Returns the value at a given row and column
        # Parameters:
        # int row is the row index of the matrix
        # int col is the column index of the matrix
        # Returns value contained in matrix row and column number
        def get_item(self, row, col):
            return self.matrix[row][col]

        # Determines if two matrices are the same
        # Parameters:
        # Matrix m is the matrix that we are comparing to
        # Returns bool whether matrices are equal
        def is_equal(self, m):
            for row in range(4):
                for col in range(4):
                    if self.get_item(row, col) != m.get_item(row, col):
                        return False
            return True

        # Multiplies the current matrix by a given matrix
        # Parameters:
        # Matrix m is the matrix that we are multiplying by
        # Retruns a new matrix with multiplied values
        def multiply(self, m):
            newM = GameMath.Matrix()
            for row in range(4):
                for col in range(4):
                    total = 0
                    for index in range(4):
                        total += self.get_item(row, index) * m.get_item(index, col)
                    newM.set_item(row, col, total)
            return newM

        # Adds a matrix to another matrix
        # Parameters:
        # Matrix m is the matrix being added
        # Returns a new matrix with the added values
        def add(self, m):
            newM = GameMath.Matrix()
            for row in range(4):
                for col in range(4):
                    newM.set_item(row, col, (self.get_item(row, col) + (m.get_item(row, col))))
            return newM

        # Subtracts a matrix from another matrix
        # Parameters:
        # Matrix m is the matrix that is subtracted
        # Returns a new matrix with subtracted values
        def sub(self, m):
            newM = GameMath.Matrix()
            for row in range(4):
                for col in range(4):
                    newM.set_item(row, col, (self.get_item(row, col) - m.get_item(row, col)))
            return newM

    # Calculate the cross product and return a vector
    # Params:
    # Vector2 or Vector3 vec1
    # Vector2 or Vector3 vec2
    # Returns a Vector
    # def crossProduct(self, v1, v2):
    #     return self.Vector3(0,(v1.x * v2.y) - (v1.y * v2.x), (v1.y * v2.z) - (v1.z * v2.y), (v1.z * v2.x) - (v1.x * v2.z))


    #determine if two vectors have the same values
    def v_is_equal(self, v1, v2):
        return v1.w == v2.w and v1.x == v2.x and v1.y == v2.y

    #find the magnitude of a vector
    def magnitude(self, v):
        return math.sqrt((v.w * v.w) + (v.x * v.x) + (v.y * v.y))
        

    #normalize a vector
    def normalize(self, v):
        vector_magnitude = self.magnitude(v)
        return self.Vector3(v.w/vector_magnitude, v.x/vector_magnitude, v.y/vector_magnitude, v.z/vector_magnitude) if hasattr(v, 'z') else self.Vector2(v.w/vector_magnitude, v.x/vector_magnitude, v.y/vector_magnitude)

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

