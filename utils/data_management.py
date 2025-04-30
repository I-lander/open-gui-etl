import numpy as np
import pandas as pd


def filter_rows(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Filters the input DataFrame based on a dictionary of column-specific conditions.

    Arguments:
    - df (pd.DataFrame): The input DataFrame to filter.
    - filters (dict): A dictionary where each key is a column name and each value is a function (usually a lambda)
                      that returns True or False. Only rows for which all conditions are met are retained.

    Returns:
    - pd.DataFrame: The filtered DataFrame with only rows that satisfy all conditions.
    """
    for column, condition in filters.items():
        df = df[df[column].apply(condition)]
    return df


def aggregate_input(
    df: pd.DataFrame, GROUP_COLUMNS: dict, AMOUNT_COLUMN: dict
) -> pd.DataFrame:
    """
    Aggregates a DataFrame by grouping on specified columns and summing a designated amount column.

    Arguments:
    - df (pd.DataFrame): The input DataFrame to group and aggregate.
    - GROUP_COLUMNS (list[str]): List of column names to group the DataFrame by.
    - AMOUNT_COLUMN (str): The name of the column containing numeric values to be summed for each group.

    Returns:
    - pd.DataFrame: A new DataFrame grouped by GROUP_COLUMNS where all non-aggregated columns keep their first value,
                    and the amount column is summed.
    """
    # Create an aggregation dictionary: "first" for all columns except the amount column
    agg_dict = {col: "first" for col in df.columns if col != AMOUNT_COLUMN}
    agg_dict[AMOUNT_COLUMN] = "sum"

    # Group by the specified columns and apply the aggregation
    grouped_df = df.groupby(GROUP_COLUMNS, as_index=False).agg(agg_dict)
    return grouped_df


def fill_empty_fields(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Fills "" values in a DataFrame with a specified fill value.

    Arguments:
    - df (pd.DataFrame): The input DataFrame with potential "" values.
    - fill_value (str): The value to replace "" values with.

    Returns:
    - pd.DataFrame: The DataFrame with "" values replaced by the specified fill value.
    """
    df[column_name] = df[column_name].replace("", np.nan)
    df[column_name] = df[column_name].ffill()
    return df


def map_fields(df: pd.DataFrame, FIELD_MAPPING: dict) -> pd.DataFrame:
    """
    Maps fields in a DataFrame based on a provided mapping dictionary.

    Arguments:
    - df (pd.DataFrame): The input DataFrame to map.
    - FIELD_MAPPING (dict): A dictionary where each key is the name of the new column and each value is a function
                            (usually a lambda) that takes a row and returns the value for that new column.

    Returns:
    - pd.DataFrame: A new DataFrame with the mapped fields.
    """

    class OutputRow:
        def __init__(self, input_row: pd.Series, row_index: int, FIELD_MAPPING: dict):
            self.data = {}

            for field_name, transformation in FIELD_MAPPING.items():
                self.data[field_name] = transformation(input_row, row_index)

        def to_dict(self):
            return self.data

    output_rows = []
    for row_index, row in df.iterrows():
        output_rows.append(OutputRow(row, row_index, FIELD_MAPPING).to_dict())
    df_out = pd.DataFrame(output_rows)
    return df_out
