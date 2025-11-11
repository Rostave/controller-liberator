from tkparam.tk_param import TkScalar, TKDataType
import unittest


def scalar(value, name="tmp"):
    scalar_type = isinstance(value, int) and TKDataType.INT or TKDataType.FLOAT
    return TkScalar(None, name, scalar_type, value ,value, value)


class TestTkScalar(unittest.TestCase):
    def setUp(self):
        self.scalar1 = scalar(10)
        self.scalar2 = scalar(2)
        self.scalar3 = scalar(10.0)

    def test_addition(self):
        self.assertEqual(self.scalar1 + 5, scalar(15), "Test failed: scalar1 + 5")
        self.assertEqual(5 + self.scalar1, scalar(15), "Test failed: 5 + scalar1")
        self.assertEqual(self.scalar1 + self.scalar2, scalar(12), "Test failed: scalar1 + scalar2")

    def test_subtraction(self):
        self.assertEqual(self.scalar1 - self.scalar2, scalar(8), "Test failed: scalar1 - scalar2")
        self.assertEqual(self.scalar2 - self.scalar1, scalar(-8), "Test failed: scalar2 - scalar1")
        self.assertEqual(10 - self.scalar1, scalar(0), "Test failed: 10 - scalar1")
        self.assertEqual(self.scalar1 - 10, scalar(0), "Test failed: scalar1 - 10")

    def test_multiplication(self):
        self.assertEqual(self.scalar1 * 3, scalar(30), "Test failed: scalar1 * 3")
        self.assertEqual(3 * self.scalar1, scalar(30), "Test failed: 3 * scalar1")
        self.assertEqual(self.scalar1 * self.scalar2, scalar(20), "Test failed: scalar1 * scalar2")

    def test_division(self):
        self.assertEqual(self.scalar1 / self.scalar2, scalar(5.0), "Test failed: scalar1 / scalar2")
        self.assertEqual(self.scalar2 / self.scalar1, scalar(0.2), "Test failed: scalar2 / scalar1")
        self.assertEqual(100 / self.scalar1, scalar(10.0), "Test failed: 100 / scalar1")
        self.assertEqual(self.scalar1 / 100, scalar(0.1), "Test failed: scalar1 / 100")

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError) as context:
            self.scalar1 / 0.0
        self.assertEqual(str(context.exception), "Divisor cannot be zero", "Test failed: scalar1 / 0")
        self.assertEqual(0.0 / self.scalar3, 0.0, "Test failed: 0.0 / scalar3")
        
    def test_comparison(self):
        self.assertTrue(self.scalar1 == self.scalar3, "Test failed: scalar1 == scalar3")
        self.assertTrue(self.scalar1 != self.scalar2, "Test failed: scalar1 != scalar2")
        self.assertTrue(self.scalar2 < self.scalar1, "Test failed: scalar2 < scalar1")
        self.assertTrue(self.scalar1 > self.scalar2, "Test failed: scalar1 > scalar2")


if __name__ == "__main__":
    unittest.main()
    print("All tests passed")
