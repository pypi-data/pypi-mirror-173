"""ABCClassifier testing"""
import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from abc_classification.abc_classifier import ABCClassifier


class Test(unittest.TestCase):
    """Class for ABCClassifier testing."""

    def setUp(self) -> None:
        self.abc_classifier = ABCClassifier(pd.read_csv('sales.txt'))
        self.true_abc = pd.read_csv('true_abc_sales.txt')
        self.true_brief_abc = pd.read_csv('true_brief_abc.txt')

    def test_classify(self):
        """Test ABCClassifier.classify()."""
        assert_frame_equal(self.abc_classifier.classify('product', 'total_sold'),
                           self.true_abc)
        self.assertRaises(ValueError, self.abc_classifier.classify, 0, 1)
        self.assertRaises(ValueError, ABCClassifier, 'data')

    def test_brief(self):
        """Test ABCClassifier.brief_abc()."""
        classified = self.abc_classifier.classify('product', 'total_sold')
        assert_frame_equal(self.abc_classifier.brief_abc(classified),
                           self.true_brief_abc)
        self.assertRaises(ValueError, self.abc_classifier.brief_abc, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
