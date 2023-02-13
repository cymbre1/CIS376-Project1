import gameMath
import unittest
import math

class TestVectors(unittest.TestCase):
    game_math = gameMath.GameMath()

    # Vector Constructor Tests
    def test_vector2_constructor(self):
        vector = self.game_math.Vector2()
        self.assertTrue(vector.w == 0)
        self.assertTrue(vector.x == 0)
        self.assertTrue(vector.y == 0)

    def test_vector2_constructor_nonDefaultArgs(self):
        vector = self.game_math.Vector2(2, 3, 1)
        self.assertTrue(vector.w == 1)
        self.assertTrue(vector.x == 2)
        self.assertTrue(vector.y == 3)

    def test_vector3_constructor(self):
        vector = self.game_math.Vector3()
        self.assertTrue(vector.w == 0)
        self.assertTrue(vector.x == 0)
        self.assertTrue(vector.y == 0)
        self.assertTrue(vector.z == 0)

    def test_vector3_constructor_nonDefaultArgs(self):
        vector = self.game_math.Vector3(2,3,4, 1)
        self.assertTrue(vector.w == 1)
        self.assertTrue(vector.x == 2)
        self.assertTrue(vector.y == 3)
        self.assertTrue(vector.z == 4)
    
    # Cross Product Tests
    def test_crossProduct_betweenTwo_vector2(self):
        vec1 = self.game_math.Vector3(1,2,3,0)
        vec2 = self.game_math.Vector3(4,5,6,0)
        result_vector = vec1.crossProduct(vec2)
        self.assertTrue(result_vector.is_equal(self.game_math.Vector3( -3, 6, -3, 1)))

    def test_crossProduct_betweenTwo_vector2_2(self):
        vec1 = self.game_math.Vector3(-1, -2, 3, 0)
        vec2 = self.game_math.Vector3(4, 0, -8, 0)
        result_vector = vec1.crossProduct(vec2)
        self.assertTrue(result_vector.is_equal(self.game_math.Vector3(16, 4, 8, 0)))

    def test_crossProduct_betweenTwo_vector2_ignoresLastCoordinateOfVector3(self):
        vec1 = self.game_math.Vector3(-1,-2,3,0)
        vec2 = self.game_math.Vector3(0,-8,2,4)
        result_vector = vec1.crossProduct(vec2)
        self.assertTrue(result_vector.is_equal(self.game_math.Vector3(20, 2, 8, 0)))

    # Dot Product Tests
    def test_dotproduct_betweenTwo_vector2(self):
        vec1 = self.game_math.Vector2(1,2,0)
        vec2 = self.game_math.Vector2(3,4,0)
        result = vec1.dotProduct(vec2)
        self.assertTrue(11, result)

    def test_dotproduct_betweenTwo_vector2_2(self):
        vec1 = self.game_math.Vector2(-1,-2,0)
        vec2 = self.game_math.Vector2(0,-8,0)
        result = vec1.dotProduct(vec2)
        self.assertTrue(-16, result)

    def test_dotproduct_between_vector2AndVector3_ignoresLastCoordinateOfVector3(self):
        vec1 = self.game_math.Vector2(-2,3,-1)
        vec2 = self.game_math.Vector3(0,-8,2,4)
        result = vec1.dotProduct(vec2)
        self.assertTrue(-16, result)

    def test_dotproduct_betweenTwo_vector3(self):
        vec1 = self.game_math.Vector3(1,2,3,0)
        vec2 = self.game_math.Vector3(3,4,5,0)
        result = vec1.dotProduct(vec2)
        self.assertTrue(26, result)

    # Vector Is Equal Tests
    def test_is_equal_whereVectorsAreEqual_returnsTrue(self):
        vec1 = self.game_math.Vector2(1,2,3)
        vec2 = self.game_math.Vector2(1,2,3)
        self.assertTrue(vec1.is_equal(vec2))

    def test_is_equal_whereVectorsAreEqualAndAreVector3_returnsTrue(self):
        vec1 = self.game_math.Vector3(1,2,3,4)
        vec2 = self.game_math.Vector3(1,2,3,4)
        self.assertTrue(vec1.is_equal(vec2))
    
    def test_is_equal_whereVectorsAreNotEqual_returnsFalse(self):
        vec1 = self.game_math.Vector2(1,2,3)
        vec2 = self.game_math.Vector2(4,5,6)
        self.assertFalse(vec1.is_equal(vec2))

    def test_is_equal_whereVectorsAreDefaultConstructed_returnsTrue(self):
        vec1 = self.game_math.Vector2()
        vec2 = self.game_math.Vector2()
        self.assertTrue(vec1.is_equal(vec2))

    # Magnitude Tests
    def test_magnitude_willReturn_correctMagnitude_vector2(self):
        vector = self.game_math.Vector2(4,-2,0)
        expected_result = 2 * math.sqrt(5)
        self.assertEqual(expected_result, vector.magnitude())

    def test_magnitude_willReturn_correctMagnitude_vector2_2(self):
        vector = self.game_math.Vector2(0,-3, 0)
        self.assertEqual(3, vector.magnitude())

    def test_magnitude_willReturn_correctMagnitude_vector3(self):
        vector = self.game_math.Vector3(2,4,-2, 0)
        expected_result = math.sqrt(24)
        blah = vector.magnitude()
        self.assertEqual(expected_result, blah)

    def test_magnitude_willReturn_correctMagnitude_vector3_2(self):
        vector = self.game_math.Vector3(1,0,-3,0)
        expected_result = math.sqrt(10)
        self.assertEqual(expected_result, vector.magnitude())

    # Magnitude Without Square Root Tests
    def test_large_magnitude_willReturn_correctMagnitude_vector2(self):
        vector = self.game_math.Vector2(4,-2,0)
        expected_result = 20
        self.assertEqual(expected_result, vector.large_magnitude())

    def test_large_magnitude_willReturn_correctMagnitude_vector2_2(self):
        vector = self.game_math.Vector2(0,-3, 0)
        self.assertEqual(9, vector.large_magnitude())

    def test_large_magnitude_willReturn_correctMagnitude_vector3(self):
        vector = self.game_math.Vector3(2,4,-2, 0)
        expected_result = 24
        blah = vector.large_magnitude()
        self.assertEqual(expected_result, blah)

    def test_large_magnitude_willReturn_correctMagnitude_vector3_2(self):
        vector = self.game_math.Vector3(1,0,-3,0)
        expected_result = 10
        self.assertEqual(expected_result, vector.large_magnitude())

    # Normalize Tests
    def test_normalize_3d_vector(self):
        vector = self.game_math.Vector3(3,2,-1,1)
        expected_result = self.game_math.Vector3(3/math.sqrt(14), math.sqrt(2/7), -1/math.sqrt(14), 1)
        result = vector.normalize()
        self.assertTrue(expected_result.is_equal(result))

    def test_normalize_3d_vector_2(self):
        vector = self.game_math.Vector3(4,5,6,1)
        expected_result = self.game_math.Vector3(4/math.sqrt(77), 5/math.sqrt(77), 6/math.sqrt(77),1)
        result = vector.normalize()
        self.assertTrue(expected_result.is_equal(result))

    def test_normalize_2d_vector(self):
        vector = self.game_math.Vector2(1,2,1)
        expected_result = self.game_math.Vector2( 1/math.sqrt(5), 2/math.sqrt(5),1)
        result = vector.normalize()
        self.assertTrue(expected_result.is_equal(result))

    def test_normalize_2d_vector_2(self):
        vector = self.game_math.Vector2(4,5,1)
        expected_result = self.game_math.Vector2(4/math.sqrt(41), 5/math.sqrt(41),1)
        result = vector.normalize()
        self.assertTrue(expected_result.is_equal(result))

    # Addition Tests
    def test_add_vector2(self):
        vec1 = self.game_math.Vector2(2,3,1)
        vec2 = self.game_math.Vector2(3,4,1)
        expected_result = self.game_math.Vector2(5,7,0)
        result = vec1.add(vec2)
        self.assertTrue(expected_result.is_equal(result))

    def test_add_vector2_2(self):
        vec1 = self.game_math.Vector2(4,5,1)
        vec2 = self.game_math.Vector2(3,-2,1)
        expected_result = self.game_math.Vector2(7,3,0)
        result = vec1.add(vec2)
        self.assertTrue(expected_result.is_equal(result))

    def test_add_vector3(self):
        vec1 = self.game_math.Vector3(2,3,4,1)
        vec2 = self.game_math.Vector3(3,4,5,1)
        expected_result = self.game_math.Vector3(5,7,9,0)
        result = vec1.add(vec2)
        self.assertTrue(expected_result.is_equal(result))

    def test_add_vector3_2(self):
        vec1 = self.game_math.Vector3(4,5,10,1)
        vec2 = self.game_math.Vector3(12,-2,100,1)
        expected_result = self.game_math.Vector3(16,3,110,0)
        result = vec1.add(vec2)
        self.assertTrue(expected_result.is_equal(result))

    # Subtraction Tests
    def test_sub_vector2(self):
        vec1 = self.game_math.Vector2(2,3,1)
        vec2 = self.game_math.Vector2(3,4,1)
        expected_result = self.game_math.Vector2(-1,-1,0)
        result = vec1.sub(vec2)
        self.assertTrue(expected_result.is_equal(result))

    def test_sub_vector2_2(self):
        vec1 = self.game_math.Vector2(4,5,1)
        vec2 = self.game_math.Vector2(3,-2,1)
        expected_result = self.game_math.Vector2(1,7,0)
        result = vec1.sub(vec2)
        self.assertTrue(expected_result.is_equal(result))

    def test_sub_vector3(self):
        vec1 = self.game_math.Vector3(2,3,4,1)
        vec2 = self.game_math.Vector3(3,4,5,1)
        expected_result = self.game_math.Vector3(-1,-1,-1,0)
        result = vec1.sub(vec2)
        self.assertTrue(expected_result.is_equal(result))

    def test_sub_vector3_2(self):
        vec1 = self.game_math.Vector3(4,5,10,1)
        vec2 = self.game_math.Vector3(12,-2,100,1)
        expected_result = self.game_math.Vector3(-8,7,-90,0)
        result = vec1.sub(vec2)
        self.assertTrue(expected_result.is_equal(result))

    # Cross Multiply Tests
    def test_crossMultiply(self):
        mat = self.game_math.Matrix()
        lst = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        mat.set_list_matrix(lst)
        vec1 = self.game_math.Vector3(2,3,4,1)
        expected_result = self.game_math.Vector3(24,64,104,144)
        result = vec1.cross_multiply(mat)
        self.assertTrue(expected_result.is_equal(result))

    # Angle between vectors Tests
    def test_angleBetween2dVectors(self):
        vec1 = self.game_math.Vector2(2,3,1)
        vec2 = self.game_math.Vector2(4,5,1)
        expected_result = 0.087
        self.assertEqual(expected_result, math.ceil(vec1.find_angle(vec2)*1000)/1000)

    def test_angleBetween3dVectors(self):
        vec1 = self.game_math.Vector3(2,3,4,1)
        vec2 = self.game_math.Vector3(4,5,6,1)
        expected_result = 0.104
        self.assertAlmostEqual(expected_result, math.ceil(vec1.find_angle(vec2)*1000)/1000)



if __name__ == 'main':
    unittest.main()