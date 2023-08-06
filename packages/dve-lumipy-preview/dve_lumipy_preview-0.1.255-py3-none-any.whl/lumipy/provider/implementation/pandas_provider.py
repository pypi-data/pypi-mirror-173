import inspect
import io
import os
from typing import List, Dict, Optional, Union, Iterable, Any

import numpy as np
import pandas as pd
from pandas import DataFrame, isna, Series, merge, CategoricalDtype, to_datetime

from lumipy.provider.common import table_dict_to_df
from lumipy.provider.metadata import ColumnMeta, ParamMeta
from lumipy.provider.base_provider import BaseProvider
from lumipy.query.expression.sql_value_type import SqlValType
from lumipy.common.string_utils import indent_str


def _df_size_summary(d):
    mem_use = pd.DataFrame.memory_usage(d, deep=True)
    max_col_len = max(len(k) for k in mem_use.keys())
    divider = '―' * (max_col_len + 11)

    def format_size(x):

        units = [['TB😱', 1e12], ['GB', 1e9], ['MB', 1e6], ['KB', 1e3], ['B ', 1e0]]

        for upper, lower in zip(units[:-1], units[1:]):
            if upper[1] > x >= lower[1]:
                vstr = f'{x / lower[1]:6.1f}'
                return f'{vstr:6} {lower[0]}'

    strs = [divider]
    for k, v in mem_use.items():
        strs.append(f'{k:{max_col_len}}  {format_size(v)}')

    strs.append(divider)
    strs.append(f'{"Total":{max_col_len}}  {format_size(mem_use.sum())}')
    strs.append(divider)

    return '\n'.join(map(lambda x: f'│ {x} │', strs))


REGEX_ESCAPES = {
    '.': '||DOT||',
    '-': '||HYPHEN||',
    '\\': '||BACKSLASH||',
    '|': '||BAR||',
    '^': '||CARET||',
    '$': '||DOLLAR||',
    '=': '||EQUALS||',
    '!': '||EXCLAIMATION||',
    '?': '||QUESTION||',
    '<': '||LESSTHAN||',
    '>': '||GREATERTHAN||',
    ':': '||COLON||',
    '*': '||STAR||',
    '+': '||PLUS||',
    '{': '||CURLYLEFT||',
    '}': '||CURLYRIGHT||',
    '[': '||SQUARELEFT||',
    ']': '||SQUARERIGHT||',
    '(': '||ROUNDLEFT||',
    ')': '||ROUNDRIGHT||',
}


def _like(series: Series, pattern: str) -> Series:
    """Apply a like expression in pandas using regex and Series.str.match.
    
    Args:
        series (Series): the pandas series to apply the like pattern to.
        pattern (str): the like pattern string.

    Returns:
        Series: pandas series of boolean values representing the like result.
    """
    for k, v in REGEX_ESCAPES.items():
        pattern = pattern.replace(k, v)

    regex_str = pattern.replace('_', '.')
    regex_str = regex_str.replace('%', '.*')
    regex_str = f'\\A{regex_str}\\Z'

    for k, v in REGEX_ESCAPES.items():
        regex_str = regex_str.replace(v, f'\\{k}')

    # filter nans because missing string value should be considered a non-match
    return (~series.isna()) & series.str.match(regex_str, case=True)


def _glob(series: Series, pattern: str) -> Series:
    """Apply a glob expression in pandas using regex and Series.str.match.

    Args:
        series (Series): the pandas series to apply the like pattern to.
        pattern (str): the glob pattern string.

    Returns:
        Series: pandas series of boolean values representing the glob result.
    """
    for k, v in REGEX_ESCAPES.items():
        pattern = pattern.replace(k, v)

    regex_str = pattern.replace('?', '.')
    regex_str = regex_str.replace('*', '.*')
    regex_str = f'\\A{regex_str}\\Z'

    for k, v in REGEX_ESCAPES.items():
        regex_str = regex_str.replace(v, f'\\{k}')

    # filter nans because missing string value should be considered a non-match
    return (~series.isna()) & series.str.match(regex_str, case=True)


class PandasProvider(BaseProvider):
    """Provides rows of data from a Pandas DataFrame.

    """

    def __init__(
            self,
            source: Union[DataFrame, str, os.PathLike, io.IOBase],
            name: str,
            name_root: Optional[str] = 'Pandas',
            description: Optional[str] = None,
            **kwargs
    ):
        """Constructor of the PandasProvider class.

        Args:
            source (Union[DataFrame, str, os.PathLike, io.IOBase]): the dataframe or pd.read_csv-compatible source to
            serve data from. Datetime-valued columns must be timezone-aware.
            See https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
            name (str): name to give the provider. The name will be appended to name_root ('Pandas') by default to
            create the full name 'Pandas.(name)' unless the name root is overridden by supplying a value.
            name_root (Optional[str]): optional name_root value. Will override 'Pandas' if not supplied.
            description (Optional[str]): optional description string of the provider.

        Keyword Args:
            keyword args are passed down to pandas read_csv if source is not a DataFrame

        """

        self.name = f'{name_root}.{name}'

        if isinstance(source, DataFrame):
            df = source
        else:
            df = pd.read_csv(source, **kwargs)

        self.df = df.rename(
            {c: str(c).replace('.', '_').replace("'", "").strip().strip('_') for c in df.columns},
            axis=1
        )

        cols = [ColumnMeta(c, self._infer_datatype(self.df[c])) for c in self.df.columns]
        params = [ParamMeta(
            "UsePandasFilter",
            SqlValType.Boolean,
            "Whether to apply a filter within the pandas provider.",
            default_value=True
        )]

        if description is None:
            description = 'A provider that serves data from a pandas dataframe.'

        df_stats_str = '\n'.join([
            '\n',
            'DataFrame Stats',
            f'    Number of rows: {df.shape[0]}',
            f'    Number of cols: {df.shape[1]}',
            '    Memory Usage:',
            f'{indent_str(_df_size_summary(self.df), 6)}',
            '',
        ])

        super().__init__(self.name, cols, params, description=description + df_stats_str)

    def _infer_datatype(self, col: Series) -> SqlValType:
        """Map the type of a pandas Series to its corresponding SQL column type.

        Args:
            col (Series): the input series to infer the type of.

        Returns:
            SqlValType: the SQL column type.
        """
        pd_dtype = col.dtype

        if pd_dtype == int:
            return SqlValType.Int
        elif pd_dtype == float:
            return SqlValType.Double
        elif pd_dtype == bool:
            return SqlValType.Boolean
        elif isinstance(pd_dtype, CategoricalDtype):
            return SqlValType.Text
        elif isinstance(pd_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
            return SqlValType.DateTime
        elif np.issubdtype(pd_dtype, np.datetime64):
            raise ValueError(
                f"The pandas DataFrame column '{col.name}' used to build the provider {self.name} was not tz-aware. "
                f"Datetime values in pandas providers must be tz-aware.\n"
                "  Consider using the following (e.g. for the UTC timezone)\n"
                "    df['column'] = df['column'].dt.tz_localize(tz='utc')\n"
                "  to convert an existing DataFrame datetime column."
            )
        else:
            return SqlValType.Text

    def get_data(
            self,
            data_filter: Dict[str, Union[List, Dict]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        """Implementation of _get_data method for PandasProvider.

        Args:
            data_filter (Optional[Dict[str, object]]): the data filter dictionary.
            limit (Optional[int]): the limit value.
            **params: (no-op) pandas provider has no parameters.

        Returns:
            Iterable[Dict[str, Union[str, int, float]]]: iterable of dicts containing the query data.
        """
        use_filter = params['UsePandasFilter']

        if data_filter is not None and use_filter:
            pd_filter = self._translate_filter(data_filter)
            f_df = self.df[pd_filter]
        else:
            f_df = self.df

        if limit is not None and use_filter:
            f_df = f_df.head(limit)

        return f_df

    def _translate_filter(self, data_filter: Dict[str, Union[List, Dict]]) -> Series:
        """Translate data_filter dictionary into a boolean pandas series that can be used to filter a DataFrame.

        Args:
            data_filter (Dict[str, Union[List, Dict]]): the data filter dictionary.

        Returns:
            Series: pandas series with boolean values to be used to filter the dataframe.
        """

        def translate(fobj: Dict[str, Union[List, Dict]]) -> Union[Series, float, str]:

            if not isinstance(fobj, dict):
                raise TypeError(
                    f'Expect a dict when translating a filter expression: was {type(fobj).__name__}. '
                    "Provider may have received a malformed filter expression dictionary from Luminesce."
                )

            op_name, op_args = fobj['OP'], fobj['EX']

            # Arg(s) to the op being None indicate that filter translation isn't supported on the Luminesce side.
            skipped_expr = op_args is None or (hasattr(op_args, '__getitem__') and any(v is None for v in op_args))
            # If op is not in the dictionary then it's not supported in the pandas provider.
            missing_expr = op_name not in op_map.keys()

            # If in any way unsupported then the filter op is a no-op.
            fn = self._no_op if skipped_expr or missing_expr else op_map[op_name]

            # Apply the function.
            return fn(op_args) if len(inspect.signature(fn).parameters) == 1 else fn(*op_args)

        op_map = {
            'Not': lambda x: ~translate(x),
            'IsNull': lambda x: isna(translate(x)),
            'IsNotNull': lambda x: ~isna(translate(x)),
            'And': lambda x, y: translate(x) & translate(y),
            'Or': lambda x, y: translate(x) | translate(y),
            'Gt': lambda x, y: translate(x) > translate(y),
            'Lt': lambda x, y: translate(x) < translate(y),
            'Gte': lambda x, y: translate(x) >= translate(y),
            'Lte': lambda x, y: translate(x) <= translate(y),
            'In': lambda x, y: translate(x).isin(translate(y)),
            'NotIn': lambda x, y: ~translate(x).isin(translate(y)),
            'Eq': lambda x, y: translate(x) == translate(y),
            'Neq': lambda x, y: translate(x) != translate(y),
            'Add': lambda x, y: translate(x) + translate(y),
            'Subtract': lambda x, y: translate(x) - translate(y),
            'Divide': lambda x, y: translate(x) / translate(y),
            'Multiply': lambda x, y: translate(x) * translate(y),
            'Between': lambda x, a, b: translate(x).between(translate(a), translate(b), inclusive=True),
            'NotBetween': lambda x, a, b: ~(translate(x).between(translate(a), translate(b), inclusive=True)),
            'DateValue': lambda x: to_datetime(x, utc=True),
            'BoolValue': lambda x: bool(x),
            'StrValue': lambda x: str(x),
            'NumValue': lambda x: float(x),
            'ColValue': lambda x: self.df[x],
            'ListValue': lambda xs: [translate(x) for x in xs],
            'Mod': lambda x, m: translate(x) % translate(m),
            'Concatenate': lambda x, y: translate(x).astype(str) + translate(y).astype(str),
            'Like': lambda x, p: _like(translate(x), translate(p)),
            'Glob': lambda x, p: _glob(translate(x), translate(p)),
            'Regexp': lambda x, p: translate(x).str.match(translate(p)),
            'NotLike': lambda x, p: ~_like(translate(x), translate(p)),
            'NotGlob': lambda x, p: ~_glob(translate(x), translate(p)),
            'NotRegexp': lambda x, p: ~(translate(x).str.match(translate(p))),
            'RestrictionTable': lambda x: self._restriction_table(x)
        }

        pd_filter = translate(data_filter)
        # Some of the expressions can return Nan as well as True/False - map these to False as trying to use these
        # values in a dataframe filter will return an error.
        # Condition on it being a series b/c the no-op 'slice(None)' translation isn't a series and will end up erroring
        if isinstance(pd_filter, Series):
            pd_filter = pd_filter.fillna(False)
        return pd_filter

    # noinspection PyUnusedLocal
    def _no_op(self, *args):
        return [True] * self.df.shape[0]

    def _restriction_table(self, restriction_dict: Dict[str, List[Any]]):
        # Parse restriction table into a dataframe and then build a filter for which columns pass
        res_df = table_dict_to_df(restriction_dict)
        on_cols = res_df.columns.tolist()
        merge_df = merge(self.df, res_df, how='left', on=on_cols, indicator=True)
        return merge_df['_merge'] == 'both'
