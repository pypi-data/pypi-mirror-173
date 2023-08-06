# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import ipywidgets as widgets

from pysparkgui.helper import (
    Transformation,
    list_to_string,
    DF_OLD,
    DF_NEW,
    PysparkguiError,
    string_to_code,
)

from pysparkgui.widgets import Multiselect, Singleselect, Text

from pysparkgui.transformations.base_components import (
    SelectorGroupMixin,
    SelectorMixin,
    SingleColumnSelector,
)

AGGREGATION_OPTIONS = [
    ("Count", "count"),
    ("Count distinct values", "countDistinct"),
    ("Sum", "sum"),
    ("Mean/Average", "mean"),
    ("Min", "min"),
    ("Max", "max"),
    ("Variance", "variance"),
    ("Standard deviation", "stddev"),
    ("First value", "first"),
    ("Last value", "last"),
    # TBD: median and other percentile values
    # https://stackoverflow.com/questions/46845672/median-quantiles-within-pyspark-groupby
    
    # TBD: count missing values
    # https://sparkbyexamples.com/pyspark/pyspark-find-count-of-null-none-nan-values/

    # ("Count (size)", "size"),  # with missing values
    # ("Count (excl. missings)", "count"),
    # ("Median", "median"),
    # distribution metrics
    # ("Standard error of the mean - sem", "sem"),
    # ("Mean absolute deviation - mad", "mad"),
    # ("Skew", "skew"),
]

class AggregationSelector(SelectorMixin, widgets.HBox):
    """
    Manages one (<column to aggregate>, <aggregation function>, <new column name>) group plus the
    delete button to remove itself.
    """

    def __init__(self, df_columns, show_delete_button=True, **kwargs):
        super().__init__(show_delete_button=show_delete_button, **kwargs)

        self.aggregation_dropdown = Singleselect(
            options=AGGREGATION_OPTIONS,
            focus_after_init=show_delete_button,
            placeholder="Choose aggregation",
            set_soft_value=True,
            width="sm",
        )

        self.column_dropdown = SingleColumnSelector(options=df_columns, width="md")

        self.new_column_name = Text(
            placeholder="Column name (optional)",
            execute=self.selector_group,
            width="md",
        )

        self.children = [
            self.aggregation_dropdown,
            widgets.VBox(
                [
                    widgets.HBox([widgets.HTML(" of "), self.column_dropdown]),
                    widgets.HBox([widgets.HTML("as"), self.new_column_name]),
                ]
            ),
            self.delete_selector_button,
        ]

    def has_valid_value(self):
        column_is_missing = not self.column_dropdown.value
        aggregation_function_is_missing = not self.aggregation_dropdown.value
        if column_is_missing:
            raise PysparkguiError(
                """You didn't specify a <b>column</b> what you want to aggregate.
                Please select a column to aggregate."""
            )
        elif aggregation_function_is_missing:
            raise PysparkguiError(
                """You didn't specify an <b>aggregation function</b> (e.g. sum or mean)
                for your column(s)."""
            )
        else:
            return True

    def get_aggregation_code(self):
        # e.g. f.sum("n").alias("n_sum")
        aggregation = self.aggregation_dropdown.value
        column = self.column_dropdown.value

        code = f"f.{aggregation}({string_to_code(column)})"
        
        new_column_name = self.new_column_name.value
        if new_column_name:
            code += f".alias({string_to_code(new_column_name)})"
        return code

    # def test_select_aggregation_functions(
    #     self, aggregation_function: str, column_name: str, new_column_name: str
    # ):
    #     self.aggregation_dropdown.value = aggregation_function
    #     self.column_dropdown.value = column_name
    #     self.new_column_name.value = new_column_name


class AggregationSection(SelectorGroupMixin, widgets.VBox):
    """Manages a group of `AggregationSelector`s."""

    def __init__(self, transformation):
        super().__init__()
        self.transformation = transformation
        self.df_columns = list(self.transformation.get_df().columns)

        self.init_selector_group("add calculation")

        self.children = [
            widgets.HTML("Calculate"),
            self.selector_group,
            self.add_selector_button,
        ]

    def create_selector(self, show_delete_button=None, **kwargs):
        return AggregationSelector(
            self.df_columns, selector_group=self, show_delete_button=show_delete_button
        )

    def get_aggregation_code(self):
        return ", ".join([selector.get_aggregation_code() for selector in self.get_selectors() if selector.has_valid_value()])

    def execute(self):
        self.transformation.execute()

    # def test_select_aggregation_functions(
    #     self, aggregation_function: str, column_name: str, new_column_name: str
    # ):
    #     self.get_selectors()[-1].test_select_aggregation_functions(
    #         aggregation_function, column_name, new_column_name
    #     )


class SparkGroupbyWithRename(Transformation):
    """
    Group rows by columns and calculate a SINGLE aggregation that can be named.

    Manages the whole transformation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.groupby_columns = Multiselect(
            options=list(self.get_df().columns),
            placeholder="Choose column(s) - optional",
            focus_after_init=False,
            width="long-column-name",
        )

        self.aggregation_section = AggregationSection(self)

        self.merge_result = Singleselect(
            placeholder="Choose style",
            options=[("New Table", False), ("New Columns", True)],
            set_soft_value=True,
            width="md",
        )

    def render(self):
        self.set_title("Calculate column summaries (aggregations)")
        self.set_content(
            widgets.VBox(
                [
                    self.aggregation_section,
                    widgets.HTML("Group By"),
                    self.groupby_columns,
                    widgets.HTML("Store result as"),
                    self.merge_result,
                    self.rename_df_group,
                ]
            )
        )

    def get_description(self):
        columns_list = list_to_string(self.groupby_columns.value, quoted=False)
        description = (
            f"<b>Group by</b> {columns_list} <b>and calculate new column(s)</b>"
        )

        if self.merge_result.value:
            description = f"<b>Add new column(s)</b> based on {description}"
        return description

    def is_valid_transformation(self):
        if (len(self.groupby_columns.value) == 0) and self.merge_result.value:
            raise PysparkguiError(
                """
                This combination is not supported yet.<br>
                You need to either add a groupby column or store the result as a new table.<br>
                If you want support for calculating new aggregated columns without groupby, please reach out.
                """
            )
        return True

    def get_code(self):
        aggregations_code = self.aggregation_section.get_aggregation_code()
        groupby_columns = self.groupby_columns.value

        potential_groupby_code = f".groupby({groupby_columns})" if len(groupby_columns) >= 1 else ""
        df_expression = f"{DF_OLD}{potential_groupby_code}.agg({aggregations_code})"

        if self.merge_result.value and (len(groupby_columns) >= 1):
            return f"""{DF_NEW} = {DF_OLD}.join({df_expression}, on={groupby_columns}, how='left')"""
        else:
            return f"""{DF_NEW} = {df_expression}"""

    def get_pyspark_chain_code(self):
        if self.merge_result.value:
            return None  # this statement cannot be expressed in chain style as far as Flo knows as of 2022-10-20
        else:
            groupby_columns = self.groupby_columns.value
            potential_groupby_code = f".groupby({groupby_columns})" if len(groupby_columns) >= 1 else ""
            return f"{potential_groupby_code}.agg({self.aggregation_section.get_aggregation_code()})"

    # def get_metainfos(self):
    #     return {
    #         "groupby_type": self.merge_result.label,
    #         "groupby_columns_count": len(self.groupby_columns.value),
    #     }

    # def reset_preview_columns_selection(self):
    #     if self.merge_result.value:
    #         return False
    #     else:  # create new table
    #         return True

    # def test_select_groupby_columns(self, groupby_columns: list):
    #     self.groupby_columns.value = groupby_columns
    #     return self  # allows method chaining

    # def test_select_aggregation(
    #     self,
    #     aggregation_function: str = "",
    #     column_name: str = "",
    #     new_column_name: str = "",
    # ):
    #     self.aggregation_section.test_select_aggregation_functions(
    #         aggregation_function, column_name, new_column_name
    #     )

    # def test_select_merge_result(self, merge_result: bool):
    #     self.merge_result.value = merge_result
