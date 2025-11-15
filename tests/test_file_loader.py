import pytest
import pandas as pd
import duckdb

from data_lens.services.file_loader import FileLoaderService
from data_lens.errors import FileLoadError, UnsupportedFormatError


@pytest.fixture
def db_connection():
    """Create a fresh DuckDB connection for each test."""
    con = duckdb.connect(":memory:")
    yield con
    con.close()


@pytest.fixture
def loader(db_connection):
    """Create a FileLoaderService instance."""
    return FileLoaderService(db_connection)


class TestSanitizeTableName:
    """Tests for table name sanitization."""

    def test_basic_sanitization(self):
        assert FileLoaderService.sanitize_table_name("sales_data.xlsx") == "sales_data"
        assert FileLoaderService.sanitize_table_name("customer-info.csv") == "customer_info"

    def test_special_characters(self):
        assert FileLoaderService.sanitize_table_name("my@file#name.parquet") == "my_file_name"
        assert FileLoaderService.sanitize_table_name("data (2024).xlsx") == "data__2024_"

    def test_spaces(self):
        assert FileLoaderService.sanitize_table_name("Sales Data 2024.xlsx") == "sales_data_2024"
        assert FileLoaderService.sanitize_table_name("Q1 Report.csv") == "q1_report"

    def test_lowercase(self):
        assert FileLoaderService.sanitize_table_name("SALES.xlsx") == "sales"
        assert FileLoaderService.sanitize_table_name("MyFile.csv") == "myfile"

    def test_sheet_names(self):
        assert FileLoaderService.sanitize_table_name("Q1 Sales") == "q1_sales"
        assert FileLoaderService.sanitize_table_name("Summary (Final)") == "summary__final_"


class TestLoadCSV:
    """Tests for CSV file loading."""

    def test_load_simple_csv(self, tmp_path, loader, db_connection):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age\nAlice,30\nBob,25")

        tables = loader.load_file(str(csv_file))

        assert len(tables) == 1
        assert tables[0] == "test"

        result = db_connection.execute("SELECT * FROM test").fetchall()
        assert len(result) == 2
        assert result[0] == ("Alice", 30)
        assert result[1] == ("Bob", 25)

    def test_load_csv_with_numbers(self, tmp_path, loader, db_connection):
        csv_file = tmp_path / "sales.csv"
        csv_file.write_text("product,revenue\nWidget,1200.50\nGadget,890.00")

        tables = loader.load_file(str(csv_file))
        result = db_connection.execute("SELECT product, revenue FROM sales").fetchall()

        assert len(result) == 2
        assert result[0][0] == "Widget"
        assert float(result[0][1]) == 1200.50

    def test_load_tsv(self, tmp_path, loader, db_connection):
        tsv_file = tmp_path / "data.tsv"
        tsv_file.write_text("id\tname\n1\tAlice\n2\tBob")

        tables = loader.load_file(str(tsv_file))

        assert len(tables) == 1
        result = db_connection.execute("SELECT * FROM data").fetchall()
        assert len(result) == 2


class TestLoadExcel:
    """Tests for Excel file loading."""

    def test_load_single_sheet_excel(self, tmp_path, loader, db_connection):
        excel_file = tmp_path / "test.xlsx"

        df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})
        df.to_excel(excel_file, index=False, sheet_name="Sheet1")

        tables = loader.load_file(str(excel_file))

        assert len(tables) == 1
        assert "sheet1" in tables
        result = db_connection.execute("SELECT * FROM sheet1").fetchall()
        assert len(result) == 2

    def test_load_multi_sheet_excel(self, tmp_path, loader, db_connection):
        excel_file = tmp_path / "multi.xlsx"

        with pd.ExcelWriter(excel_file) as writer:
            pd.DataFrame({"product": ["A", "B"], "price": [10, 20]}).to_excel(
                writer, sheet_name="Products", index=False
            )
            pd.DataFrame({"region": ["North", "South"], "sales": [100, 200]}).to_excel(
                writer, sheet_name="Sales", index=False
            )

        tables = loader.load_file(str(excel_file))

        assert len(tables) == 2
        assert "products" in tables
        assert "sales" in tables

        products = db_connection.execute("SELECT * FROM products").fetchall()
        sales = db_connection.execute("SELECT * FROM sales").fetchall()

        assert len(products) == 2
        assert len(sales) == 2

    def test_sheet_name_sanitization(self, tmp_path, loader, db_connection):
        excel_file = tmp_path / "report.xlsx"

        with pd.ExcelWriter(excel_file) as writer:
            pd.DataFrame({"value": [1, 2]}).to_excel(
                writer, sheet_name="Q1 Sales (Final)", index=False
            )

        tables = loader.load_file(str(excel_file))

        assert "q1_sales__final_" in tables


class TestLoadParquet:
    """Tests for Parquet file loading."""

    def test_load_parquet(self, tmp_path, loader, db_connection):
        parquet_file = tmp_path / "data.parquet"

        df = pd.DataFrame({"id": [1, 2, 3], "value": [10.5, 20.3, 30.7]})
        df.to_parquet(parquet_file)

        tables = loader.load_file(str(parquet_file))

        assert len(tables) == 1
        assert "data" in tables

        result = db_connection.execute("SELECT * FROM data").fetchall()
        assert len(result) == 3
        assert result[0][0] == 1


class TestErrorHandling:
    """Tests for error handling."""

    def test_file_not_found(self, loader):
        with pytest.raises(FileLoadError, match="File not found"):
            loader.load_file("/nonexistent/file.csv")

    def test_unsupported_format(self, tmp_path, loader):
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("some text")

        with pytest.raises(UnsupportedFormatError, match="Unsupported file format: txt"):
            loader.load_file(str(txt_file))

    def test_directory_instead_of_file(self, tmp_path, loader):
        directory = tmp_path / "mydir"
        directory.mkdir()

        with pytest.raises(FileLoadError, match="Not a file"):
            loader.load_file(str(directory))

    def test_invalid_excel(self, tmp_path, loader):
        fake_excel = tmp_path / "fake.xlsx"
        fake_excel.write_text("not an excel file")

        with pytest.raises(Exception):
            loader.load_file(str(fake_excel))
