"""Tests for app.config."""

from app.config import Settings


class TestSettings:
    def test_default_values(self) -> None:
        s = Settings()
        assert s.app_name == "AI Data Analyst"
        assert s.debug is False
        assert s.max_upload_size_mb == 50

    def test_is_extension_allowed(self) -> None:
        s = Settings()
        assert s.is_extension_allowed("data.csv")
        assert s.is_extension_allowed("DATA.CSV")
        assert s.is_extension_allowed("report.xlsx")
        assert not s.is_extension_allowed("script.py")
        assert not s.is_extension_allowed("image.png")

    def test_max_upload_bytes(self) -> None:
        s = Settings(max_upload_size_mb=10)
        assert s.max_upload_bytes() == 10 * 1024 * 1024
