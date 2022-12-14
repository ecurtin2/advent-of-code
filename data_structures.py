from typing import Any
from itertools import product


class Grid:
    def __init__(self):
        # Column major sparse dict
        # Key = (col_i, row_i)
        self._data: dict = dict()
        self.min_row: None | int = None
        self.max_row: None | int = None
        self.min_col: None | int = None
        self.max_col: None | int = None
        self.empty_repr: str = " "

    @property
    def span(self):
        return ((self.min_col, self.max_col), (self.min_row, self.max_row))

    def update_span(self, row_i: int, col_i: int):
        self.max_row = max(self.max_row if self.max_row is not None else row_i, row_i)
        self.min_row = min(self.min_row if self.min_row is not None else row_i, row_i)
        self.max_col = max(self.max_col if self.max_col is not None else col_i, col_i)
        self.min_col = min(self.min_col if self.min_col is not None else col_i, col_i)

    def __setitem__(self, idx: tuple[slice | int, slice | int], val: Any):
        col_idx, row_idx = idx
        # Early exit simple case
        if isinstance(row_idx, int) and isinstance(col_idx, int):
            self._data[(col_idx, row_idx)] = val
            self.update_span(row_idx, col_idx)
            return
        if isinstance(row_idx, int):
            row_idxs = [row_idx]
        else:
            step = 1 if row_idx.stop > row_idx.start else -1
            if step == 0:
                row_idxs = [row_idx.start]
            else:
                row_idxs = range(row_idx.start, row_idx.stop + step, step)
        if isinstance(col_idx, int):
            col_idxs = [col_idx]
        else:
            step = 1 if col_idx.stop > col_idx.start else -1
            if step == 0:
                col_idxs = [col_idx.start]
            else:
                col_idxs = range(col_idx.start, col_idx.stop + step, step)

        for r, c in product(row_idxs, col_idxs):
            self[(c, r)] = val

    def __getitem__(self, key):
        return self._data[key]

    def __contains__(self, key):
        return key in self._data

    def value_counts(self):
        counts = {}
        for v in self._data.values():
            counts[v] = counts.setdefault(v, 0) + 1
        return counts

    def __str__(self):
        ridxs = range(self.min_row or 0, (self.max_row or 0) + 1)
        cidxs = range(self.min_col or 0, (self.max_col or 0) + 1)
        return "\n".join(
            "".join(self._data.get((ic, ir), self.empty_repr) for ic in cidxs)
            for ir in ridxs
        )
