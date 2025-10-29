"""Tests for correlation module."""

import numpy as np
import pandas as pd

from src.vn50.features.corr import distance_from_corr


def test_distance_from_corr():
    """Test Mantegna distance calculation."""
    # Create test correlation matrix
    corr = pd.DataFrame(
        [[1.0, 0.5, 0.3], [0.5, 1.0, 0.2], [0.3, 0.2, 1.0]],
        index=["A", "B", "C"],
        columns=["A", "B", "C"],
    )

    distance = distance_from_corr(corr)

    # Check diagonal is zero
    np.testing.assert_array_almost_equal(np.diag(distance.values), [0, 0, 0])

    # Check symmetry
    np.testing.assert_array_almost_equal(distance.values, distance.values.T)

    # Check non-negative
    assert (distance.values >= 0).all()
