import unittest
import numpy as np
import pandas as pd

from toad import IV, WOE, gini, gini_cond, entropy_cond, quality
from toad.stats import _IV
from toad.utils import feature_splits

np.random.seed(1)

feature = np.random.rand(500)
target = np.random.randint(2, size = 500)
A = np.random.randint(100, size = 500)
B = np.random.randint(100, size = 500)
df = pd.DataFrame({
    'feature': feature,
    'target': target,
    'A': A,
    'B': B,
})

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_woe(self):
        value = WOE(0.2, 0.3)
        self.assertEqual(value, -0.4054651081081643)

    def test_iv_priv(self):
        value = _IV(df['feature'], df['target'])
        self.assertEqual(value, 0.010385942643745353)

    def test_iv(self):
        value = IV(df['feature'], df['target'])
        self.assertEqual(value, 0.5313391779453922)

    def test_gini(self):
        value = gini(df['target'])
        self.assertEqual(value, 0.499352)

    def test_feature_splits(self):
        value = feature_splits(df['feature'], df['target'])
        self.assertEqual(len(value), 243)

    def test_gini_cond(self):
        value = gini_cond(df['feature'], df['target'])
        self.assertEqual(value, 0.4970162601626016)

    def test_entropy_cond(self):
        value = entropy_cond(df['feature'], df['target'])
        self.assertEqual(value, 0.6924990371522171)

    def test_quality(self):
        result = quality(df, 'target')
        self.assertEqual(result.loc['feature', 'iv'], 0.5313391779453922)
        self.assertEqual(result.loc['A', 'gini'], 0.49284164671885444)
        self.assertEqual(result.loc['B', 'entropy'], 0.6924956879070063)
        self.assertEqual(result.loc['feature', 'unique'], 500)

    def test_quality_iv_only(self):
        result = quality(df, 'target', iv_only = True)
        self.assertEqual(result.loc['feature', 'gini'], '--')

    def test_quality_object_type_array_with_nan(self):
        mask = np.random.randint(8, size = 500)
        feature = np.array([np.nan, 'A', 'B', 'C', 'D', 'E', 'F', 'G'], dtype = 'O')[mask]

        df = pd.DataFrame({
            'feature': feature,
            'target': target,
        })
        result = quality(df)
        self.assertEqual(result.loc['feature', 'iv'], 0.03443287832743326)