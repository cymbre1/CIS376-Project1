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



#testing area
mat = GameMath.Matrix()
mat2 = GameMath.Matrix()
lst = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

mat.set_single_matrix(-543)
#mat.set_list_matrix(lst)
mat2.set_list_matrix(lst)



mat.print_matrix()
mat2.print_matrix()

mat = mat.multiply(mat2)
mat.print_matrix()
