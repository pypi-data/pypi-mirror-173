"""Module for ABC classification in business analysis."""
from typing import Optional
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


class ABCClassifier:
    """ABC classification class"""

    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise ValueError('Provided object is not pd.DataFrame')

        self.data = data

    def classify(self, abc_column: str, criterion: str) -> pd.DataFrame:
        """Make ABC classification for values from abc_column.
        Dataframe must be grouped by abc_column.

        Args:
            abc_column (str): column with values to classify.
            criterion (str): column with criterion for classification.

        Returns:
            abc_df (pd.DataFrame): classified dataframe.

        Raises:
            ValueError: if args are not str."""
        if not isinstance(abc_column, str):
            raise ValueError(f'Column name must be string not {type(abc_column)}')
        if not isinstance(criterion, str):
            raise ValueError(f'Column name must be string not {type(criterion)}')

        abc_df = self.data[[abc_column, criterion]].copy()
        abc_df.sort_values(by=criterion, inplace=True, ascending=False)
        total = self.data[criterion].sum()
        abc_df['percentage'] = abc_df[criterion] / total
        abc_df[f'cumulative_{criterion}'] = abc_df['percentage'].cumsum()
        conditions = [(abc_df[f'cumulative_{criterion}'] <= 0.7),
                      (abc_df[f'cumulative_{criterion}'] <= 0.9),
                      (abc_df[f'cumulative_{criterion}'] > 0.9)]
        values = ['A', 'B', 'C']
        abc_df['class'] = np.select(conditions, values)
        abc_df.drop(['percentage', f'cumulative_{criterion}'], axis=1, inplace=True)

        return abc_df

    def brief_abc(self, abc_df: pd.DataFrame) -> pd.DataFrame:
        """Aggregates dataframe by class with summarized information.

        Args:
            abc_df (pd.DataFrame): DataFrame for brief information calculation.

        Returns:
            brief_abc_df (pd.DataFrame): Dataframe with summarized info.

        Raises:
            ValueError: if abc_df is not pd.DataFrame."""
        if not isinstance(abc_df, pd.DataFrame):
            raise ValueError('Passed object is not pd.DataFrame.')
        brief_abc_df = abc_df.groupby('class').sum().reset_index()
        return brief_abc_df

    def pareto_chart(self,
                     data: pd.DataFrame,
                     values: str, labels: str,
                     title: Optional[str] = 'Pareto chart') -> None:
        """Plots pareto chart.

        Args:
            data (pd.DataFrame): abc classified dataframe.
            values (str): column of data containing values.
            labels (str): column of data containing labels.
            title (str, optional): title of plot. Defaults to 'Pareto chart'."""
        data = data.copy()
        data["cumulative_percentage"] = data[labels].cumsum() / data[labels].sum() * 100
        fig, values_axis = plt.subplots()
        plt.xticks(rotation=25)
        plt.title(title)
        values_axis.bar(data[values], data[labels])
        cumulative_percentage_axis = values_axis.twinx()
        cumulative_percentage_axis.plot(data[values],
                                        data["cumulative_percentage"],
                                        color="C1", marker="D", ms=7)
        cumulative_percentage_axis.yaxis.set_major_formatter(PercentFormatter())

        values_axis.tick_params(axis="y", colors="C0")
        cumulative_percentage_axis.tick_params(axis="y", colors="C1")
        plt.show()
