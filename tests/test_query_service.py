import pytest
import pandas as pd
import duckdb

from data_lens.services.query_service import QueryService
from data_lens.models.query import QueryResult


@pytest.fixture
def db_connection():
    """Create a DuckDB connection with test data."""
    con = duckdb.connect(":memory:")

    df = pd.DataFrame({
        "product": ["Widget", "Gadget", "Tool", "Widget", "Gadget"],
        "revenue": [1200.50, 890.00, 450.25, 1100.00, 920.75],
        "region": ["North", "South", "East", "West", "North"],
        "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"])
    })
    con.execute("CREATE TABLE sales AS SELECT * FROM df")

    yield con
    con.close()


@pytest.fixture
def query_service(db_connection):
    """Create a QueryService instance."""
    return QueryService(db_connection)


class TestSafetyChecks:
    """Tests for SQL safety checks."""

    def test_safe_select_queries(self, query_service):
        assert query_service.is_safe_query("SELECT * FROM sales") is True
        assert query_service.is_safe_query("SELECT COUNT(*) FROM sales") is True
        assert query_service.is_safe_query("SELECT product, SUM(revenue) FROM sales GROUP BY product") is True

    def test_unsafe_drop_queries(self, query_service):
        assert query_service.is_safe_query("DROP TABLE sales") is False
        assert query_service.is_safe_query("drop table customers") is False
        assert query_service.is_safe_query("DROP DATABASE test") is False

    def test_unsafe_delete_queries(self, query_service):
        assert query_service.is_safe_query("DELETE FROM sales") is False
        assert query_service.is_safe_query("DELETE FROM sales WHERE id = 1") is False

    def test_unsafe_update_queries(self, query_service):
        assert query_service.is_safe_query("UPDATE sales SET revenue = 0") is False
        assert query_service.is_safe_query("UPDATE sales SET product = 'test' WHERE id = 1") is False

    def test_unsafe_alter_queries(self, query_service):
        assert query_service.is_safe_query("ALTER TABLE sales ADD COLUMN test VARCHAR") is False
        assert query_service.is_safe_query("ALTER TABLE sales DROP COLUMN revenue") is False

    def test_unsafe_create_table_queries(self, query_service):
        assert query_service.is_safe_query("CREATE TABLE test (id INTEGER)") is False
        assert query_service.is_safe_query("CREATE TABLE IF NOT EXISTS test (id INTEGER)") is False

    def test_safe_cte_queries(self, query_service):
        query = "WITH top_products AS (SELECT product FROM sales) SELECT * FROM top_products"
        assert query_service.is_safe_query(query) is True


class TestQueryExecution:
    """Tests for query execution."""

    def test_simple_select(self, query_service):
        result = query_service.execute_query("SELECT * FROM sales LIMIT 2")

        assert result.success is True
        assert result.error is None
        assert len(result.columns) == 4
        assert len(result.rows) == 2
        assert "product" in result.columns
        assert "revenue" in result.columns

    def test_aggregation_query(self, query_service):
        result = query_service.execute_query("SELECT COUNT(*) as count FROM sales")

        assert result.success is True
        assert result.columns == ["count"]
        assert len(result.rows) == 1
        assert result.rows[0][0] == "5"

    def test_group_by_query(self, query_service):
        result = query_service.execute_query(
            "SELECT product, SUM(revenue) as total FROM sales GROUP BY product ORDER BY total DESC"
        )

        assert result.success is True
        assert "product" in result.columns
        assert "total" in result.columns
        assert len(result.rows) == 3

    def test_where_clause(self, query_service):
        result = query_service.execute_query("SELECT * FROM sales WHERE region = 'North'")

        assert result.success is True
        assert len(result.rows) == 2

    def test_order_by(self, query_service):
        result = query_service.execute_query("SELECT product FROM sales ORDER BY revenue DESC LIMIT 1")

        assert result.success is True
        assert len(result.rows) == 1

    def test_date_extraction(self, query_service):
        result = query_service.execute_query(
            "SELECT EXTRACT(month FROM date) as month FROM sales LIMIT 1"
        )

        assert result.success is True
        assert "month" in result.columns

    def test_values_as_strings(self, query_service):
        result = query_service.execute_query("SELECT revenue FROM sales LIMIT 1")

        assert result.success is True
        for row in result.rows:
            for value in row:
                assert isinstance(value, str)


class TestQueryErrors:
    """Tests for query error handling."""

    def test_unsafe_query_error(self, query_service):
        result = query_service.execute_query("DROP TABLE sales")

        assert result.success is False
        assert "Unsafe SQL detected" in result.error
        assert result.columns is None
        assert result.rows is None

    def test_syntax_error(self, query_service):
        result = query_service.execute_query("SELECT * FORM sales")

        assert result.success is False
        assert result.error is not None

    def test_table_not_found(self, query_service):
        result = query_service.execute_query("SELECT * FROM nonexistent_table")

        assert result.success is False
        assert result.error is not None

    def test_column_not_found(self, query_service):
        result = query_service.execute_query("SELECT nonexistent_column FROM sales")

        assert result.success is False
        assert result.error is not None

    def test_type_mismatch(self, query_service):
        result = query_service.execute_query("SELECT * FROM sales WHERE revenue = 'not_a_number'")

        assert result.success is False
        assert result.error is not None


class TestQueryResultModel:
    """Tests for QueryResult model."""

    def test_success_property(self):
        success_result = QueryResult(columns=["id"], rows=[["1"]])
        assert success_result.success is True

        error_result = QueryResult(error="Something went wrong")
        assert error_result.success is False

    def test_model_dump_success(self, query_service):
        result = query_service.execute_query("SELECT * FROM sales LIMIT 1")
        data = result.model_dump(exclude_none=True)

        assert "columns" in data
        assert "rows" in data
        assert "error" not in data

    def test_model_dump_error(self, query_service):
        result = query_service.execute_query("DROP TABLE sales")
        data = result.model_dump(exclude_none=True)

        assert "error" in data
        assert "columns" not in data
        assert "rows" not in data


class TestComplexQueries:
    """Tests for complex SQL queries."""

    def test_join_query(self):
        con = duckdb.connect(":memory:")

        df_products = pd.DataFrame({"id": [1, 2], "name": ["Widget", "Gadget"]})
        df_sales = pd.DataFrame({"product_id": [1, 2, 1], "amount": [100, 200, 150]})

        con.execute("CREATE TABLE products AS SELECT * FROM df_products")
        con.execute("CREATE TABLE sales_data AS SELECT * FROM df_sales")

        service = QueryService(con)
        result = service.execute_query(
            "SELECT p.name, SUM(s.amount) as total "
            "FROM products p JOIN sales_data s ON p.id = s.product_id "
            "GROUP BY p.name"
        )

        assert result.success is True
        assert len(result.rows) == 2

        con.close()

    def test_window_function(self, query_service):
        result = query_service.execute_query(
            "SELECT product, revenue, "
            "ROW_NUMBER() OVER (ORDER BY revenue DESC) as rank "
            "FROM sales"
        )

        assert result.success is True
        assert "rank" in result.columns

    def test_case_statement(self, query_service):
        result = query_service.execute_query(
            "SELECT product, "
            "CASE WHEN revenue > 1000 THEN 'High' ELSE 'Low' END as category "
            "FROM sales"
        )

        assert result.success is True
        assert "category" in result.columns
