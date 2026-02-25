"""ETL pipeline for TSE Filiados (party membership) data.

Data source: BigQuery table basedosdados.br_tse_filiacao_partidaria.microdados
Pre-exported to CSV via download script.

Limitation: TSE filiados data does NOT contain CPF. Matching to existing
Person nodes is done by exact normalized name + UF, which is inherently
imprecise for common names. A match_method property is stored on the
relationship to make this limitation transparent.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd

from icarus_etl.base import Pipeline

if TYPE_CHECKING:
    from neo4j import Driver
from icarus_etl.loader import Neo4jBatchLoader
from icarus_etl.transforms import (
    deduplicate_rows,
    normalize_name,
    parse_date,
)

logger = logging.getLogger(__name__)


def _membership_id(name: str, party: str, uf: str, affiliation_date: str) -> str:
    """Deterministic ID from name + party + UF + date."""
    raw = f"{name}|{party}|{uf}|{affiliation_date}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class TseFiliadosPipeline(Pipeline):
    """ETL pipeline for TSE party membership (filiacao partidaria)."""

    name = "tse_filiados"
    source_id = "tse_filiados"

    def __init__(
        self,
        driver: Driver,
        data_dir: str = "./data",
        limit: int | None = None,
        chunk_size: int = 50_000,
    ) -> None:
        super().__init__(driver, data_dir, limit=limit, chunk_size=chunk_size)
        self._raw: pd.DataFrame = pd.DataFrame()
        self.memberships: list[dict[str, Any]] = []
        self.person_rels: list[dict[str, Any]] = []

    def extract(self) -> None:
        filiados_dir = Path(self.data_dir) / "tse_filiados"
        csv_path = filiados_dir / "filiados.csv"

        if not csv_path.exists():
            logger.warning("[tse_filiados] filiados.csv not found at %s", csv_path)
            return

        self._raw = pd.read_csv(
            csv_path,
            dtype=str,
            keep_default_na=False,
        )
        if self.limit:
            self._raw = self._raw.head(self.limit)

        logger.info("[tse_filiados] Extracted %d raw rows", len(self._raw))

    def transform(self) -> None:
        memberships: list[dict[str, Any]] = []
        person_rels: list[dict[str, Any]] = []

        for _idx, row in self._raw.iterrows():
            nome_raw = str(row.get("nome", "")).strip()
            if not nome_raw:
                continue

            nome = normalize_name(nome_raw)
            if not nome:
                continue

            party = str(row.get("sigla_partido", "")).strip().upper()
            if not party:
                continue

            uf = str(row.get("sigla_uf", "")).strip().upper()
            affiliation_date = parse_date(str(row.get("data_filiacao", "")))
            status = str(row.get("situacao_registro", "")).strip()
            municipality_id = str(row.get("id_municipio_tse", "")).strip()

            mid = _membership_id(nome, party, uf, affiliation_date)

            memberships.append({
                "membership_id": mid,
                "name": nome,
                "party": party,
                "uf": uf,
                "affiliation_date": affiliation_date,
                "status": status,
                "municipality_id": municipality_id,
                "source": "tse_filiados",
            })

            person_rels.append({
                "source_name": nome,
                "source_uf": uf,
                "target_key": mid,
                "party": party,
                "affiliation_date": affiliation_date,
                "status": status,
            })

        self.memberships = deduplicate_rows(memberships, ["membership_id"])
        self.person_rels = person_rels

        logger.info(
            "[tse_filiados] Transformed %d PartyMembership nodes, %d person relationships",
            len(self.memberships),
            len(self.person_rels),
        )

    def load(self) -> None:
        loader = Neo4jBatchLoader(self.driver)

        if self.memberships:
            loaded = loader.load_nodes(
                "PartyMembership", self.memberships, key_field="membership_id",
            )
            logger.info("[tse_filiados] Loaded %d PartyMembership nodes", loaded)

        if self.person_rels:
            query = (
                "UNWIND $rows AS row "
                "MATCH (p:Person) "
                "WHERE p.name = row.source_name AND p.uf = row.source_uf "
                "MATCH (m:PartyMembership {membership_id: row.target_key}) "
                "MERGE (p)-[r:FILIADO_A]->(m) "
                "SET r.party = row.party, "
                "    r.affiliation_date = row.affiliation_date, "
                "    r.status = row.status, "
                "    r.match_method = 'name_uf_exact'"
            )
            loaded = loader.run_query_with_retry(query, self.person_rels)
            logger.info("[tse_filiados] Loaded %d FILIADO_A relationships", loaded)
