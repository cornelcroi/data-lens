import pytest
import pandas as pd
import duckdb

from data_lens.database import DuckDBClient
from data_lens.services import FileLoaderService, SchemaService, QueryService


@pytest.fixture
def client():
    """Create a DuckDBClient instance."""
    client = DuckDBClient()
    yield client
    client.close()


class TestEndToEndWorkflow:
    """Integration tests for complete workflows."""

    def test_csv_load_and_query(self, tmp_path, client):
        csv_file = tmp_path / "sales.csv"
        csv_file.write_text("product,revenue,region\nWidget,1200,North\nGadget,890,South")

        loader = FileLoaderService(client.connection)
        schema_service = SchemaService(client.connection)
        query_service = QueryService(client.connection)

        tables = loader.load_file(str(csv_file))
        assert "sales" in tables

        schema = schema_service.get_table_schema("sales")
        assert "product" in schema.columns

        result = query_service.execute_query("SELECT * FROM sales WHERE region = 'North'")
        assert result.success is True
        assert len(result.rows) == 1

    def test_excel_multi_sheet_workflow(self, tmp_path, client):
        excel_file = tmp_path / "report.xlsx"

        with pd.ExcelWriter(excel_file) as writer:
            pd.DataFrame({"product": ["A", "B"], "price": [10, 20]}).to_excel(
                writer, sheet_name="Products", index=False
            )
            pd.DataFrame({"region": ["North", "South"], "sales": [100, 200]}).to_excel(
                writer, sheet_name="Sales", index=False
            )

        loader = FileLoaderService(client.connection)
        schema_service = SchemaService(client.connection)
        query_service = QueryService(client.connection)

        tables = loader.load_file(str(excel_file))
        assert len(tables) == 2

        all_tables = schema_service.list_tables()
        assert "products" in all_tables
        assert "sales" in all_tables

        result = query_service.execute_query("SELECT COUNT(*) FROM products")
        assert result.rows[0][0] == "2"

    def test_parquet_analytics_workflow(self, tmp_path, client):
        parquet_file = tmp_path / "data.parquet"

        df = pd.DataFrame({
            "customer": ["Alice", "Bob", "Charlie", "Alice", "Bob"],
            "amount": [100, 200, 150, 300, 250],
            "date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03"])
        })
        df.to_parquet(parquet_file)

        loader = FileLoaderService(client.connection)
        query_service = QueryService(client.connection)

        loader.load_file(str(parquet_file))

        result = query_service.execute_query(
            "SELECT customer, SUM(amount) as total "
            "FROM data GROUP BY customer ORDER BY total DESC"
        )

        assert result.success is True
        assert len(result.rows) == 3


class TestDatabaseReset:
    """Tests for database reset functionality."""

    def test_reset_clears_data(self, tmp_path, client):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("id,value\n1,100\n2,200")

        loader = FileLoaderService(client.connection)
        schema_service = SchemaService(client.connection)

        loader.load_file(str(csv_file))
        assert len(schema_service.list_tables()) == 1

        client.reset()

        loader_new = FileLoaderService(client.connection)
        schema_new = SchemaService(client.connection)
        assert len(schema_new.list_tables()) == 0

    def test_reset_clears_active_files(self, tmp_path, client):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("id,value\n1,100")

        client.active_files = [str(csv_file)]
        assert len(client.active_files) == 1

        client.reset()
        assert len(client.active_files) == 0


class TestMultipleFileLoads:
    """Tests for loading multiple files sequentially."""

    def test_load_second_file_replaces_first(self, tmp_path, client):
        csv1 = tmp_path / "file1.csv"
        csv1.write_text("id,name\n1,Alice")

        csv2 = tmp_path / "file2.csv"
        csv2.write_text("product,price\nWidget,100")

        loader = FileLoaderService(client.connection)
        schema_service = SchemaService(client.connection)

        loader.load_file(str(csv1))
        assert "file1" in schema_service.list_tables()

        client.reset()
        loader_new = FileLoaderService(client.connection)
        schema_new = SchemaService(client.connection)

        loader_new.load_file(str(csv2))
        tables = schema_new.list_tables()

        assert "file2" in tables
        assert "file1" not in tables


class TestSchemaInspectionWorkflow:
    """Tests for schema inspection workflow."""

    def test_complete_schema_inspection(self, tmp_path, client):
        csv_file = tmp_path / "customers.csv"
        csv_file.write_text(
            "id,name,email,active\n"
            "1,Alice,alice@example.com,true\n"
            "2,Bob,bob@example.com,false\n"
            "3,Charlie,charlie@example.com,true"
        )

        loader = FileLoaderService(client.connection)
        schema_service = SchemaService(client.connection)

        loader.load_file(str(csv_file))

        tables = schema_service.list_tables()
        assert "customers" in tables

        columns = schema_service.list_columns("customers")
        assert len(columns) == 4

        preview = schema_service.preview_rows("customers", limit=2)
        assert len(preview["rows"]) == 2

        full_schema = schema_service.get_all_schemas()
        assert "customers" in full_schema.schemas
        assert len(full_schema.schemas["customers"].sample_values["name"]) == 3


class TestErrorRecovery:
    """Tests for error recovery in workflows."""

    def test_query_after_failed_query(self, tmp_path, client):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("value\n100\n200")

        loader = FileLoaderService(client.connection)
        query_service = QueryService(client.connection)

        loader.load_file(str(csv_file))

        bad_result = query_service.execute_query("SELECT * FROM nonexistent")
        assert bad_result.success is False

        good_result = query_service.execute_query("SELECT * FROM data")
        assert good_result.success is True

    def test_load_after_failed_load(self, tmp_path, client):
        bad_file = tmp_path / "bad.txt"
        bad_file.write_text("not a csv")

        good_csv = tmp_path / "good.csv"
        good_csv.write_text("id\n1")

        loader = FileLoaderService(client.connection)

        with pytest.raises(Exception):
            loader.load_file(str(bad_file))

        tables = loader.load_file(str(good_csv))
        assert "good" in tables


class TestDataTypes:
    """Tests for different data types."""

    def test_integer_types(self, client):
        loader = FileLoaderService(client.connection)
        query_service = QueryService(client.connection)

        client.connection.execute("CREATE TABLE numbers (small TINYINT, big BIGINT)")
        client.connection.execute("INSERT INTO numbers VALUES (1, 9999999999)")

        result = query_service.execute_query("SELECT * FROM numbers")
        assert result.success is True

    def test_date_types(self, client):
        query_service = QueryService(client.connection)

        client.connection.execute("CREATE TABLE dates (dt DATE, ts TIMESTAMP)")
        client.connection.execute("INSERT INTO dates VALUES ('2024-01-01', '2024-01-01 12:00:00')")

        result = query_service.execute_query("SELECT * FROM dates")
        assert result.success is True

    def test_boolean_types(self, client):
        query_service = QueryService(client.connection)

        client.connection.execute("CREATE TABLE flags (active BOOLEAN)")
        client.connection.execute("INSERT INTO flags VALUES (true), (false)")

        result = query_service.execute_query("SELECT * FROM flags WHERE active = true")
        assert result.success is True
        assert len(result.rows) == 1
