from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import pandas as pd
from pydantic.dataclasses import dataclass
from pyfedappwrap.learning.app_types import BasePrePostProcessApp
from pyfedappwrap.learning.run_runfig import AppConfig, AppInputConfig, AppOutputConfig
from typing_extensions import override


@dataclass
class BranchMergeConfig(AppConfig):
    mode: str = "concat_columns"
    key: str | None = None
    how: str = "inner"


@dataclass
class BranchMergeOutput(AppOutputConfig):
    output: Any | None = None


@dataclass
class BranchMergeInput(AppInputConfig):
    left: Any = None
    right: Any = None


class BranchMergeApp(
    BasePrePostProcessApp[BranchMergeConfig, BranchMergeInput, BranchMergeOutput]
):

    def __init__(self):
        super().__init__()

    def run_process(self, data: BranchMergeInput) -> BranchMergeOutput:
        if data.left is None or data.right is None:
            raise ValueError("BranchMergeInput.left and BranchMergeInput.right must not be None.")
        if not isinstance(data.left, pd.DataFrame) or not isinstance(data.right, pd.DataFrame):
            raise TypeError(
                "BranchMergeInput.left and BranchMergeInput.right must be pandas DataFrames.")

        left = data.left
        right = data.right
        mode = self.config.mode or "concat_columns"
        how = self.config.how or "inner"
        key = self.config.key

        if mode == "concat_rows":
            merged = pd.concat([left, right], axis=0, ignore_index=True)
        elif mode == "concat_columns":
            merged = pd.concat(
                [
                    left.reset_index(drop=True).add_suffix("_left"),
                    right.reset_index(drop=True).add_suffix("_right"),
                ],
                axis=1,
            )
        elif mode == "merge_on_key":
            if not key:
                raise ValueError("BranchMergeConfig.key is required when mode='merge_on_key'.")
            if key not in left.columns or key not in right.columns:
                raise ValueError(f"Merge key '{key}' must be present in both inputs.")
            merged = pd.merge(left, right, on=key, how=how)
        else:
            raise ValueError(
                "BranchMergeConfig.mode must be one of: 'concat_rows', 'concat_columns', 'merge_on_key'."
            )

        return BranchMergeOutput(output=merged)

    @override
    def get_test_data(self) -> Optional[dict[str, Path]]:
        return {
            "left": Path("data/left.csv"),
            "right": Path("data/right.csv"),
        }

    @override
    def get_test_hyperparams(self) -> Optional[dict[str, Any]]:
        return {
            "mode": "concat_columns",
            "key": "",
            "how": "inner",
        }