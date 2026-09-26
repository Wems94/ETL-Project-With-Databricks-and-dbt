"""Testes para a conversão CSV -> Parquet, preservando tudo como string."""

from pathlib import Path

import pyarrow.parquet as pq

from taxi_pipeline.csv_to_parquet import convert_csv_to_parquet


def _write_sample_csv(path: Path) -> None:
    path.write_text(
        "VendorID,pickup_datetime,trip_distance\n"
        "1,2016-03-01 00:00:00,2.50\n"
        "2,2016-03-01 00:05:00,19.98\n"
        "1,2016-03-01 00:10:00,0.00\n"
    )


def test_convert_preserves_row_count(tmp_path: Path) -> None:
    src = tmp_path / "sample.csv"
    dst = tmp_path / "sample.parquet"
    _write_sample_csv(src)

    rows = convert_csv_to_parquet(src, dst)

    assert rows == 3


def test_convert_writes_all_columns_as_string(tmp_path: Path) -> None:
    src = tmp_path / "sample.csv"
    dst = tmp_path / "sample.parquet"
    _write_sample_csv(src)

    convert_csv_to_parquet(src, dst)

    schema = pq.ParquetFile(dst).schema_arrow
    assert schema.names == ["VendorID", "pickup_datetime", "trip_distance"]
    assert {str(t) for t in schema.types} == {"string"}


def test_convert_creates_destination_parent_dir(tmp_path: Path) -> None:
    src = tmp_path / "sample.csv"
    dst = tmp_path / "nested" / "sample.parquet"
    _write_sample_csv(src)

    convert_csv_to_parquet(src, dst)

    assert dst.exists()