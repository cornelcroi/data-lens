import pytest
import pandas as pd
import duckdb

from data_lens.services.schema_service import SchemaService
from data_lens.models.schema import ColumnInfo, TableSchema


@pytest.fixture
def db_connection():
    """Create a DuckDB connection with test data."""
    con = duckdb.connect(":memory:")

    df_sales = pd.DataFrame({
        "product": ["Widget", "Gadget", "Tool"],
        "revenue": [1200.50, 890.00, 450.25],
        "region": ["North", "South", "East"]
    })
    con.execute("CREATE TABLE sales AS SELECT * FROM df_sales")

    df_customers = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "active": [True, False, True]
    })
    con.execute("CREATE TABLE customers AS SELECT * FROM df_customers")

    yield con
    con.close()


@pytest.fixture
def schema_service(db_connection):
    """Create a SchemaService instance."""
    return SchemaService(db_connection)


class TestListTables:
    """Tests for listing tables."""

    def test_list_all_tables(self, schema_service):
        tables = schema_service.list_tables()

        assert len(tables) == 2
        assert "sales" in tables
        assert "customers" in tables

    def test_empty_database(self):
        con = duckdb.connect(":memory:")
        service = SchemaService(con)

        tables = service.list_tables()
        assert len(tables) == 0

        con.close()


class TestListColumns:
    """Tests for listing columns."""

    def test_list_sales_columns(self, schema_service):
        columns = schema_service.list_columns("sales")

        assert len(columns) == 3
        assert any(c.name == "product" and c.type == "VARCHAR" for c in columns)
        assert any(c.name == "revenue" and c.type == "DOUBLE" for c in columns)
        assert any(c.name == "region" and c.type == "VARCHAR" for c in columns)

    def test_list_customers_columns(self, schema_service):
        columns = schema_service.list_columns("customers")

        assert len(columns) == 3
        column_names = [c.name for c in columns]
        assert "id" in column_names
        assert "name" in column_names
        assert "active" in column_names

    def test_column_info_model(self, schema_service):
        columns = schema_service.list_columns("sales")

        for col in columns:
            assert isinstance(col, ColumnInfo)
            assert isinstance(col.name, str)
            assert isinstance(col.type, str)


class TestGetTableSchema:
    """Tests for getting table schema with samples."""

    def test_get_sales_schema(self, schema_service):
        schema = schema_service.get_table_schema("sales")

        assert isinstance(schema, TableSchema)
        assert "product" in schema.columns
        assert "revenue" in schema.columns
        assert "region" in schema.columns

        assert "product" in schema.sample_values
        assert len(schema.sample_values["product"]) == 3
        assert "Widget" in schema.sample_values["product"]

    def test_sample_values_count(self, schema_service):
        schema = schema_service.get_table_schema("customers")

        for col, values in schema.sample_values.items():
            assert len(values) == 3

    def test_sample_values_as_strings(self, schema_service):
        schema = schema_service.get_table_schema("customers")

        for col, values in schema.sample_values.items():
            for value in values:
                assert isinstance(value, str)


class TestGetAllSchemas:
    """Tests for getting all schemas."""

    def test_get_all_schemas(self, schema_service):
        response = schema_service.get_all_schemas()

        assert len(response.tables) == 2
        assert "sales" in response.tables
        assert "customers" in response.tables

        assert "sales" in response.schemas
        assert "customers" in response.schemas

        sales_schema = response.schemas["sales"]
        assert isinstance(sales_schema, TableSchema)
        assert "product" in sales_schema.columns

    def test_schema_response_serialization(self, schema_service):
        response = schema_service.get_all_schemas()
        data = response.model_dump()

        assert "tables" in data
        assert "schemas" in data
        assert isinstance(data["tables"], list)
        assert isinstance(data["schemas"], dict)


class TestPreviewRows:
    """Tests for previewing table rows."""

    def test_preview_default_limit(self, schema_service):
        preview = schema_service.preview_rows("sales")

        assert preview["table"] == "sales"
        assert preview["limit"] == 5
        assert len(preview["columns"]) == 3
        assert len(preview["rows"]) == 3

    def test_preview_custom_limit(self, schema_service):
        preview = schema_service.preview_rows("customers", limit=2)

        assert preview["limit"] == 2
        assert len(preview["rows"]) == 2

    def test_preview_columns_order(self, schema_service):
        preview = schema_service.preview_rows("sales")

        assert preview["columns"] == ["product", "revenue", "region"]

    def test_preview_row_values(self, schema_service):
        preview = schema_service.preview_rows("sales", limit=1)

        assert len(preview["rows"]) == 1
        row = preview["rows"][0]
        assert len(row) == 3
        assert row[0] == "Widget"

    def test_preview_values_as_strings(self, schema_service):
        preview = schema_service.preview_rows("customers")

        for row in preview["rows"]:
            for value in row:
                assert isinstance(value, str)


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_table(self):
        con = duckdb.connect(":memory:")
        con.execute("CREATE TABLE empty (id INTEGER, name VARCHAR)")
        service = SchemaService(con)

        schema = service.get_table_schema("empty")
        assert len(schema.columns) == 2
        assert len(schema.sample_values["id"]) == 0

        preview = service.preview_rows("empty")
        assert len(preview["rows"]) == 0

        con.close()

    def test_large_preview_limit(self, schema_service):
        preview = schema_service.preview_rows("sales", limit=1000)

        assert len(preview["rows"]) == 3

    def test_single_column_table(self):
        con = duckdb.connect(":memory:")
        df = pd.DataFrame({"value": [1, 2, 3, 4, 5]})
        con.execute("CREATE TABLE single AS SELECT * FROM df")
        service = SchemaService(con)

        schema = service.get_table_schema("single")
        assert len(schema.columns) == 1
        assert "value" in schema.columns

        con.close()
