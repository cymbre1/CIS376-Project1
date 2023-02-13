import math
class GameMath():

     # Has 3 coordinates, where w is the homogenous value and x and y are the coordinates of the vector
    class Vector2():
        def __init__(self, x = 0, y = 0 , w = 0):
            self.w = w
            self.x = x
            self.y = y

        # Calculate the dot product between the current vector and another vector and return a scalar value
        # Params:
        # Vector2 vec
        # Returns a scalar value that represents the dotproduct between the given vector and the one passed in
        def dotProduct(self, vec):
            return (self.x * vec.x) + (self.y * vec.y)
        
        # Calculate the magnitude of the given vector
        # Returns a float representing the magnitude of the vector
        def magnitude(self):
            return math.sqrt((self.x * self.x) + (self.y * self.y))

        # Calculate the magnitude of the given vector without the square root, only to determine which magnitude is larger.
        # Returns a float representing the magnitude of the vector before you would take the square root.
        def large_magnitude(self):
            return (self.x * self.x) + (self.y * self.y)
        
        # Adds two vectors and returns another vector that represents the sum of the two
        # Params
        # Vector2 v - vector to add to current vector
        # Returns a new vector that represents the current vector added with the given vector.
        def add(self, v):
            return GameMath.Vector2(self.x + v.x, self.y + v.y, (self.w + v.w) % 2)

        # Subtracts two vectors and returns another vector that represents the sum of the two
        # Params
        # Vector2 v - vector to subtract frp, current vector
        # Returns a new vector that represents the current vector subtracted from the given vector.
        def sub(self, v):
            return GameMath.Vector2(self.x - v.x , self.y - v.y, (self.w - v.w) % 2)

        # Calculates the cross product of two 2d vectors
        # Params
        # Vector2 v that is the vector that should be crossed with the current vector.
        # Returns a new vector that represents the cross product of the two vectors
        def crossProduct(self, v):
            return GameMath.Vector2(self.x * v.x, self.y * v.y, self.w * v.w)
        
        # Checks to see if two vectors are equal
        # Params
        # Vector2 v that is the vector that should be compared with the current vector.
        # Returns boolean value that represents whether or not the two vectors are equal
        def is_equal(self, v):
            return self.w == v.w and self.x == v.x and self.y == v.y
        
        # Finds the angle in radians between two vectors
        # Params
        # Vector2 v that is the vector that the angle is being found between the current vector
        # Returns float value representing the angle between the two vectors
        def find_angle(self, v):
            step1 = self.dotProduct(v)
            step2 = step1 / (self.magnitude() * v.magnitude()) 
            return math.acos(step2)

        # Normalizes the current vector
        # Returns a new array that is the normalized version of the current array.
        def normalize(self):
            vector_magnitude = self.magnitude()
            return GameMath.Vector2(self.x/vector_magnitude,  self.y/vector_magnitude, 1)

    # Has 4 coordinates, where w  is the homogenous value and x,y, and z are the coordinates of the vector.
    class Vector3():
        # Constructor for Vector 3.  Values default to 0
        def __init__(self, x = 0, y = 0, z = 0, w = 0):
            self.w = w
            self.x = x
            self.y = y
            self.z = z

        # This function returns the vector as an iterable list
        def iterable_vec(self):
            return [self.x, self.y, self.z, self.w]

        # Calculates the dot product and return a scalar value
        # Params:
        # Vector3 vec is the vector that is multiplied into the dot product
        # Returns a scalar value
        def dotProduct(self, vec):
            return (self.x * vec.x) + (self.y * vec.y) + (self.z * vec.z)
        
        # Calculates the cross product and returns the vector
        # Params
        # Vector3 v is the vector that is multiplied
        # Returns a Vector3
        def crossProduct(self, v):
            return GameMath.Vector3((self.y * v.z) - (self.z * v.y), (self.z * v.x) - (self.x * v.z), (self.x * v.y) - (self.y * v.x), 0)

        # Determines if two vectors are the same
        # Parameters:
        # Vector3 v is the vector being compared to
        # Returns bool whether vectors are equal
        def is_equal(self, v):
            return self.x == v.x and self.y == v.y and self.z == v.z and self.w == self.w

        # finds the precise magnitude of the vector
        def magnitude(self):
            return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))

        # finds the magnitude without square root
        def large_magnitude(self):
            return (self.x * self.x) + (self.y * self.y) + (self.z * self.z)

        # normalizes the vector
        # Returns a new Vector3 as the normalized vector
        def normalize(self):
            vector_magnitude = self.magnitude()
            return GameMath.Vector3(self.x/vector_magnitude,  self.y/vector_magnitude, self.z/vector_magnitude, 1)

        # Adds two vectors
        # Parameters:
        # Vector3 v is the vector being added
        # Returns a new vector with added values
        def add(self, v):
            return GameMath.Vector3(self.x + v.x, self.y + v.y, self.z + v.z, (self.w + v.w) % 2)

        # Subtracts two vectors
        # Parameters:
        # Vector3 v is the vector being subtracted
        # Returns a new vector with subtracted values
        def sub(self, v):
            return GameMath.Vector3(self.x - v.x , self.y - v.y, self.z - v.z, (self.w - v.w) % 2)

        # Finds the angle between 2 vectors
        # Parameters:
        # Vector3 v is the vector we find the angle between
        # returns an angle measurement in radians
        def find_angle(self, v):
            step1 = self.dotProduct(v)
            step2 = step1 / (self.magnitude() * v.magnitude() )
            return math.acos(step2)
        
        # Multiplies the vector by a transformation matrix
        # Parameters:
        # Matrix m is the matrix multiplying the vector
        # Returns a new vector with multiplied
        def cross_multiply(self, m):
            result_list = [0,0,0,0]
            usable_vector = self.iterable_vec()
            for row in range (4):
                result = 0
                for col in range(4):
                    result += usable_vector[col] * m.get_item(row, col)
                result_list[row] = result
            return GameMath.Vector3(result_list[0], result_list[1], result_list[2], result_list[3])


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

        # This function sets the matrix to the identity matrix
        def set_identity_matrix(self):
            for row in range(4):
                for col in range(4):
                    if row == col:
                        self.set_item(row,col, 1)
                        continue
                    self.set_item(row, col, 0)


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
