from typing import List, Tuple

import pytest  # type: ignore

from scripts.engine import utility
from scripts.engine.core.constants import Shape, ShapeType


class TestUtility:
    test_get_coordinates_from_shape_parameters = [
        (Shape.SQUARE, 1, (0, 0), [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]),
        (Shape.CIRCLE, 1, (0, 0), [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]),
        (Shape.CROSS, 1, (0, 0), [(0, 0), (1, -1), (-1, 1), (-1, -1), (1, 1)]),
        (Shape.TARGET, 1, (0, 0), [(0, 0)]),
        (Shape.CONE, 1, (0, 1), [(0, 0), (1, 1), (0, 1), (-1, 1)]),
        (Shape.CONE, 1, (0, -1), [(0, 0), (1, -1), (0, -1), (-1, -1)]),
        (Shape.CONE, 1, (1, 0), [(0, 0), (1, -1), (1, 1), (1, 0)]),
        (Shape.CONE, 1, (-1, 0), [(0, 0), (-1, 1), (-1, 0), (-1, -1)]),
    ]

    @pytest.mark.parametrize("shape, size, direction, expected", test_get_coordinates_from_shape_parameters)
    def test_get_coordinates_from_shape(self, shape: ShapeType, size: int, direction: Tuple[int, int],
                                        expected: List[Tuple[int, int]]):
        """
        Test get coordinates from shape returns the correct coordinates
        """
        coordinates = utility.get_coords_from_shape(shape, size, direction)
        assert set(coordinates) == set(expected)
