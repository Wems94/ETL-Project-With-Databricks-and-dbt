"""Converte o CSV bruto em Parquet, preservando todas as colunas como string."""

import argparse
from pathlib import Path

import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.parquet as pq

BLOCK_SIZE = 64 * 1024 * 1024  # 64 MB por bloco lido (evita milhares de row groups)


def convert_csv_to_parquet(src: Path, dst: Path) -> int:
    """Converte em streaming, sem carregar o CSV inteiro na memória.

    Retorna o número de linhas gravadas.
    """
    names = pacsv.open_csv(src).schema.names
    convert = pacsv.ConvertOptions(column_types={name: pa.string() for name in names})
    read = pacsv.ReadOptions(block_size=BLOCK_SIZE)
    reader = pacsv.open_csv(src, read_options=read, convert_options=convert)

    dst.parent.mkdir(parents=True, exist_ok=True)
    rows = 0
    with pq.ParquetWriter(dst, reader.schema, compression="snappy") as writer:
        for batch in reader:
            writer.write_batch(batch)
            rows += batch.num_rows
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src", type=Path, help="CSV de entrada")
    parser.add_argument("dst", type=Path, help="Parquet de saída")
    args = parser.parse_args()
    rows = convert_csv_to_parquet(args.src, args.dst)
    print(f"{rows} linhas gravadas em {args.dst}")


if __name__ == "__main__":
    main()