import gameMath
import unittest
import math

class TestMatrix(unittest.TestCase):
    game_math = gameMath.GameMath()

    def test_matrix_constructor(self):
        mat = self.game_math.Matrix()
        self.assertTrue(mat.matrix[0][0] == 1)
        self.assertTrue(mat.matrix[0][1] == 0)
        self.assertTrue(mat.matrix[0][2] == 0)
        self.assertTrue(mat.matrix[0][3] == 0)
        self.assertTrue(mat.matrix[1][0] == 0)
        self.assertTrue(mat.matrix[1][1] == 1)
        self.assertTrue(mat.matrix[1][2] == 0)
        self.assertTrue(mat.matrix[1][3] == 0)
        self.assertTrue(mat.matrix[2][0] == 0)
        self.assertTrue(mat.matrix[2][1] == 0)
        self.assertTrue(mat.matrix[2][2] == 1)
        self.assertTrue(mat.matrix[2][3] == 0)
        self.assertTrue(mat.matrix[3][0] == 0)
        self.assertTrue(mat.matrix[3][1] == 0)
        self.assertTrue(mat.matrix[3][2] == 0)
        self.assertTrue(mat.matrix[3][3] == 1)

    def test_list_set(self):
        mat = self.game_math.Matrix()
        lst = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        mat.set_list_matrix(lst)
        self.assertTrue(mat.matrix[0][0] == 1)
        self.assertTrue(mat.matrix[0][1] == 2)
        self.assertTrue(mat.matrix[0][2] == 3)
        self.assertTrue(mat.matrix[0][3] == 4)
        self.assertTrue(mat.matrix[1][0] == 5)
        self.assertTrue(mat.matrix[1][1] == 6)
        self.assertTrue(mat.matrix[1][2] == 7)
        self.assertTrue(mat.matrix[1][3] == 8)
        self.assertTrue(mat.matrix[2][0] == 9)
        self.assertTrue(mat.matrix[2][1] == 10)
        self.assertTrue(mat.matrix[2][2] == 11)
        self.assertTrue(mat.matrix[2][3] == 12)
        self.assertTrue(mat.matrix[3][0] == 13)
        self.assertTrue(mat.matrix[3][1] == 14)
        self.assertTrue(mat.matrix[3][2] == 15)
        self.assertTrue(mat.matrix[3][3] == 16)

    def test_single_set(self):
        mat = self.game_math.Matrix()
        mat.set_single_matrix(8)
        for row in range(4):
            for col in range(4):
                self.assertTrue(mat.matrix[row][col] == 8)
    
    def test_identity_set(self):
        mat = self.game_math.Matrix()
        mat.set_single_matrix(20)
        mat.set_identity_matrix()
        self.assertTrue(mat.matrix[0][0] == 1)
        self.assertTrue(mat.matrix[0][1] == 0)
        self.assertTrue(mat.matrix[0][2] == 0)
        self.assertTrue(mat.matrix[0][3] == 0)
        self.assertTrue(mat.matrix[1][0] == 0)
        self.assertTrue(mat.matrix[1][1] == 1)
        self.assertTrue(mat.matrix[1][2] == 0)
        self.assertTrue(mat.matrix[1][3] == 0)
        self.assertTrue(mat.matrix[2][0] == 0)
        self.assertTrue(mat.matrix[2][1] == 0)
        self.assertTrue(mat.matrix[2][2] == 1)
        self.assertTrue(mat.matrix[2][3] == 0)
        self.assertTrue(mat.matrix[3][0] == 0)
        self.assertTrue(mat.matrix[3][1] == 0)
        self.assertTrue(mat.matrix[3][2] == 0)
        self.assertTrue(mat.matrix[3][3] == 1)
    
    def test_is_equal_returns_false(self):
        mat = self.game_math.Matrix()
        mat2 = self.game_math.Matrix()
        mat2.set_single_matrix(0)
        self.assertFalse(mat.is_equal(mat2))

    def test_is_equal_returns_true(self):
        mat = self.game_math.Matrix()
        mat2 = self.game_math.Matrix()
        self.assertTrue(mat.is_equal(mat2))
    
    def test_copy_matrix(self):
        mat = self.game_math.Matrix()
        mat2 = self.game_math.Matrix()
        mat.set_single_matrix(7)
        mat2.copy_matrix(mat)
        self.assertTrue(mat.is_equal(mat2))
    
    def test_set_item(self):
        mat = self.game_math.Matrix()
        mat.set_item(2, 1, 58)
        self.assertTrue(mat.matrix[2][1] == 58)
    
    def test_get_item(self):
        mat = self.game_math.Matrix()
        mat.set_list_matrix([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.assertTrue(mat.get_item(3,0) == 13)

    def test_multiply(self):
        mat = self.game_math.Matrix()
        matResult = self.game_math.Matrix()
        mat.set_list_matrix([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        matResult.set_list_matrix([90,100,110,120,202,228,254,280,314,356,398,440,426,484,542,600])
        mat = mat.multiply(mat)
        self.assertTrue(mat.is_equal(matResult))

    def test_ordered_multiply(self):
        mat = self.game_math.Matrix()
        mat2 = self.game_math.Matrix()
        matResult = self.game_math.Matrix()
        mat.set_list_matrix([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        mat2.set_list_matrix([7,8,4,6,5,2,1,2,320,45,8,7,4,68,52,4])
        matResult.set_list_matrix([993,419,238,47,2337,911,498,123,3681,1403,758,199,5025,1895,1018,275])
        mat = mat.multiply(mat2)
        self.assertTrue(mat.is_equal(matResult))
