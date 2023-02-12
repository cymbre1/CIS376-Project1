import gameMath
import unittest
import math

class TestGameMath(unittest.TestCase):
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
        vec1 = self.game_math.Vector2(1,2,3)
        vec2 = self.game_math.Vector2(4,5,6)
        result_vector = self.game_math.crossProduct(vec1,vec2)
        self.assertTrue(self.game_math.v_is_equal(self.game_math.Vector2(-3, 6, -3), result_vector))

    def test_crossProduct_betweenTwo_vector2_2(self):
        vec1 = self.game_math.Vector2(-1,-2,3)
        vec2 = self.game_math.Vector2(4,0,-8)
        result_vector = self.game_math.crossProduct(vec1,vec2)
        self.assertTrue(self.game_math.v_is_equal(self.game_math.Vector2(16, 4, 8), result_vector))

    def test_crossProduct_betweenTwo_vector2_ignoresLastCoordinateOfVector3(self):
        vec1 = self.game_math.Vector2(-1,-2,3)
        vec2 = self.game_math.Vector3(4,0,-8,2)
        result_vector = self.game_math.crossProduct(vec1,vec2)
        self.assertTrue(self.game_math.v_is_equal(self.game_math.Vector2(16, 4, 8), result_vector))

    # Dot Product Tests
    def test_dotproduct_betweenTwo_vector2(self):
        vec1 = self.game_math.Vector2(1,2,3)
        vec2 = self.game_math.Vector2(4,5,6)
        result = self.game_math.dotProduct(vec1,vec2)
        self.assertTrue(32, result)

    def test_dotproduct_betweenTwo_vector2_2(self):
        vec1 = self.game_math.Vector2(-1,-2,3)
        vec2 = self.game_math.Vector2(4,0,-8)
        result = self.game_math.dotProduct(vec1,vec2)
        self.assertTrue(-28, result)

    def test_dotproduct_between_vector2AndVector3_ignoresLastCoordinateOfVector3(self):
        vec1 = self.game_math.Vector2(-1,-2,3)
        vec2 = self.game_math.Vector3(4,0,-8,2)
        result = self.game_math.dotProduct(vec1,vec2)
        self.assertTrue(-28, result)

    # Vector Is Equal Tests
    def test_v_is_equal_whereVectorsAreEqual_returnsTrue(self):
        vec1 = self.game_math.Vector2(1,2,3)
        vec2 = self.game_math.Vector2(1,2,3)
        self.assertTrue(self.game_math.v_is_equal(vec1, vec2))

    def test_v_is_equal_whereVectorsAreEqualAndAreVector3_returnsTrue(self):
        vec1 = self.game_math.Vector3(1,2,3,4)
        vec2 = self.game_math.Vector3(1,2,3,4)
        self.assertTrue(self.game_math.v_is_equal(vec1, vec2))
    
    def test_v_is_equal_whereVectorsAreNotEqual_returnsFalse(self):
        vec1 = self.game_math.Vector2(1,2,3)
        vec2 = self.game_math.Vector2(4,5,6)
        self.assertFalse(self.game_math.v_is_equal(vec1, vec2))

    def test_v_is_equal_whereVectorsAreDefaultConstructed_returnsTrue(self):
        vec1 = self.game_math.Vector2()
        vec2 = self.game_math.Vector2()
        self.assertTrue(self.game_math.v_is_equal(vec1, vec2))

    def test_v_is_equal_whereVectorsAreDefaultConstructedButOneIsVector3_returnsFalse(self):
        vec1 = self.game_math.Vector2()
        vec2 = self.game_math.Vector3()
        self.assertFalse(self.game_math.v_is_equal(vec1, vec2))

    def test_v_is_equal_whereVectorsAreNotEqualButOneIsVector3_returnsFalse(self):
        vec1 = self.game_math.Vector2(1,2,3)
        vec2 = self.game_math.Vector3(1,2,3,4)
        self.assertFalse(self.game_math.v_is_equal(vec1, vec2))

    def test_magnitude_willReturn_correctMagnitude_vector2(self):
        vector = self.game_math.Vector2(2,4,-2)
        expected_result = 2 * math.sqrt(6)
        self.assertAlmostEquals(expected_result, self.game_math.magnitude(vector))

    def test_magnitude_willReturn_correctMagnitude_vector2_2(self):
        vector = self.game_math.Vector2(1,0,-3)
        expected_result = math.sqrt(10)
        self.assertAlmostEquals(expected_result, self.game_math.magnitude(vector))

if __name__ == 'main':
    unittest.main()