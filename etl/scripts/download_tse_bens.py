#!/usr/bin/env python3
"""Download TSE Bens Declarados (candidate declared assets) from Base dos Dados (BigQuery).

Streams from BigQuery table `basedosdados.br_tse_eleicoes.bens_candidato` to a local CSV.
Requires `google-cloud-bigquery` and an authenticated GCP project.

Usage:
    python etl/scripts/download_tse_bens.py --billing-project icarus-corruptos
    python etl/scripts/download_tse_bens.py --billing-project icarus-corruptos --start-year 2018
    python etl/scripts/download_tse_bens.py --billing-project icarus-corruptos --skip-existing
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BQ_TABLE = "basedosdados.br_tse_eleicoes.bens_candidato"

COLUMNS = [
    "ano",
    "tipo_eleicao",
    "sigla_uf",
    "id_municipio",
    "id_municipio_tse",
    "id_candidato_bd",
    "cpf",
    "titulo_eleitoral",
    "sequencial_candidato",
    "numero_candidato",
    "nome_candidato",
    "nome_urna_candidato",
    "numero_partido",
    "sigla_partido",
    "nome_partido",
    "tipo_bem",
    "descricao_bem",
    "valor_bem",
]

PAGE_SIZE = 100_000


@click.command()
@click.option("--billing-project", required=True, help="GCP project for BigQuery billing")
@click.option("--output-dir", default="./data/tse_bens", help="Output directory for CSV")
@click.option("--start-year", type=int, default=2002, help="Earliest election year to include")
@click.option("--skip-existing", is_flag=True, help="Skip download if CSV already exists")
def main(
    billing_project: str,
    output_dir: str,
    start_year: int,
    skip_existing: bool,
) -> None:
    """Download TSE Bens Declarados from Base dos Dados (BigQuery) to local CSV."""
    import google.auth
    from google.cloud import bigquery

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / "bens.csv"

    if skip_existing and dest.exists():
        logger.info("Skipping (exists): %s", dest)
        return

    credentials, _ = google.auth.default()
    client = bigquery.Client(
        credentials=credentials,
        project=billing_project,
        location="US",
    )

    cols = ", ".join(COLUMNS)
    query = f"SELECT {cols} FROM `{BQ_TABLE}` WHERE ano >= {start_year} ORDER BY ano, sigla_uf"  # noqa: S608

    logger.info("Running query: %s (start_year=%d)", BQ_TABLE, start_year)
    query_job = client.query(query)

    rows_written = 0
    for i, chunk_df in enumerate(query_job.result().to_dataframe_iterable()):
        chunk_df.to_csv(dest, mode="a", header=(i == 0), index=False)
        rows_written += len(chunk_df)
        if i == 0 or rows_written % (PAGE_SIZE * 5) == 0:
            logger.info("  bens: %d rows written", rows_written)

    logger.info("Done: %s (%d rows)", dest, rows_written)

    size_mb = dest.stat().st_size / 1e6
    logger.info("File size: %.1f MB", size_mb)


if __name__ == "__main__":
    main()
    sys.exit(0)
