"""Tests for app.data_ingestion.service – IngestionService."""

import pytest

from app.data_ingestion.service import IngestionService


@pytest.fixture()
def svc() -> IngestionService:
    return IngestionService()


class TestIngest:
    def test_csv_ingest(self, svc: IngestionService, sample_csv_bytes: bytes) -> None:
        record, report = svc.ingest("data.csv", sample_csv_bytes)
        assert record.dataset_id == "ds_000001"
        assert record.filename == "data.csv"
        assert record.row_count == 3
        assert report.row_count == 3

    def test_json_ingest(self, svc: IngestionService, sample_json_bytes: bytes) -> None:
        record, _ = svc.ingest("data.json", sample_json_bytes)
        assert record.row_count == 2

    def test_unsupported_extension_raises(self, svc: IngestionService) -> None:
        with pytest.raises(ValueError, match="Unsupported file type"):
            svc.ingest("data.txt", b"hello")

    def test_get_dataframe(self, svc: IngestionService, sample_csv_bytes: bytes) -> None:
        record, _ = svc.ingest("test.csv", sample_csv_bytes)
        df = svc.get_dataframe(record.dataset_id)
        assert df is not None
        assert len(df) == 3

    def test_get_missing_dataset(self, svc: IngestionService) -> None:
        assert svc.get_dataframe("nonexistent") is None

    def test_list_datasets(self, svc: IngestionService, sample_csv_bytes: bytes) -> None:
        svc.ingest("a.csv", sample_csv_bytes)
        svc.ingest("b.csv", sample_csv_bytes)
        datasets = svc.list_datasets()
        assert len(datasets) == 2
