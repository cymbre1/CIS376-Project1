import gameMath
import unittest
import math

class TestVectors(unittest.TestCase):
    game_math = gameMath.GameMath()

    # Vector Tests
    def test_vector2_constructor(self):
        vector = self.game_math.Vector2()
        self.assertTrue(vector.w == 0)
        self.assertTrue(vector.x == 0)
        self.assertTrue(vector.y == 0)

    def test_vector2_constructor_nonDefaultArgs(self):
        vector = self.game_math.Vector2(1, 2, 3)
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
        vector = self.game_math.Vector3(1,2,3,4)
        self.assertTrue(vector.w == 1)
        self.assertTrue(vector.x == 2)
        self.assertTrue(vector.y == 3)
        self.assertTrue(vector.z == 4)
    
    # Cross Product Tests
    def test_crossProduct_betweenTwo_vector2(self):
        vec1 = self.game_math.Vector3(0,1,2,3)
        vec2 = self.game_math.Vector3(0,4,5,6)
        result_vector = vec1.crossProduct(vec2)
        self.assertTrue(result_vector.is_equal(self.game_math.Vector3(1, -3, 6, -3)))

    def test_crossProduct_betweenTwo_vector2_2(self):
        vec1 = self.game_math.Vector3(0, -1, -2, 3)
        vec2 = self.game_math.Vector3(0, 4, 0, -8)
        result_vector = vec1.crossProduct(vec2)
        self.assertTrue(result_vector.is_equal(self.game_math.Vector3(0, 16, 4, 8)))

    def test_crossProduct_betweenTwo_vector2_ignoresLastCoordinateOfVector3(self):
        vec1 = self.game_math.Vector3(0,-1,-2,3)
        vec2 = self.game_math.Vector3(4,0,-8,2)
        result_vector = vec1.crossProduct(vec2)
        self.assertTrue(result_vector.is_equal(self.game_math.Vector3(0, 20, 2, 8)))

    # Dot Product Tests
    def test_dotproduct_betweenTwo_vector2(self):
        vec1 = self.game_math.Vector3(0,1,2)
        vec2 = self.game_math.Vector3(0,3,4)
        result = vec1.dotProduct(vec2)
        self.assertTrue(11, result)

    def test_dotproduct_betweenTwo_vector2_2(self):
        vec1 = self.game_math.Vector3(0,-1,-2)
        vec2 = self.game_math.Vector3(0,0,-8)
        result = vec1.dotProduct(vec2)
        self.assertTrue(-16, result)

    def test_dotproduct_between_vector2AndVector3_ignoresLastCoordinateOfVector3(self):
        vec1 = self.game_math.Vector3(-1,-2,3)
        vec2 = self.game_math.Vector3(4,0,-8,2)
        result = vec1.dotProduct(vec2)
        self.assertTrue(-16, result)

    def test_dotproduct_betweenTwo_vector3(self):
        vec1 = self.game_math.Vector3(0,1,2,3)
        vec2 = self.game_math.Vector3(0,3,4,5)
        result = vec1.dotProduct(vec2)
        self.assertTrue(26, result)

    # Vector Is Equal Tests
    def test_v_is_equal_whereVectorsAreEqual_returnsTrue(self):
        vec1 = self.game_math.Vector2(1,2,3)
        vec2 = self.game_math.Vector2(1,2,3)
        self.assertTrue(vec1.is_equal(vec2))

    def test_v_is_equal_whereVectorsAreEqualAndAreVector3_returnsTrue(self):
        vec1 = self.game_math.Vector3(1,2,3,4)
        vec2 = self.game_math.Vector3(1,2,3,4)
        self.assertTrue(vec1.is_equal(vec2))
    
    def test_v_is_equal_whereVectorsAreNotEqual_returnsFalse(self):
        vec1 = self.game_math.Vector2(1,2,3)
        vec2 = self.game_math.Vector2(4,5,6)
        self.assertFalse(vec1.is_equal(vec2))

    def test_v_is_equal_whereVectorsAreDefaultConstructed_returnsTrue(self):
        vec1 = self.game_math.Vector2()
        vec2 = self.game_math.Vector2()
        self.assertTrue(vec1.is_equal(vec2))

    def test_magnitude_willReturn_correctMagnitude_vector2(self):
        vector = self.game_math.Vector3(0, 2,4,-2)
        expected_result = math.sqrt(24)
        blah = vector.magnitude()
        self.assertEqual(expected_result, blah)

    def test_magnitude_willReturn_correctMagnitude_vector2_2(self):
        vector = self.game_math.Vector3(0, 1,0,-3)
        expected_result = math.sqrt(10)
        self.assertAlmostEquals(expected_result, vector.magnitude())

if __name__ == 'main':
    unittest.main()