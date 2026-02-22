from pathlib import Path
from typing import Any

from neo4j import AsyncSession, Record

QUERIES_DIR = Path(__file__).parent.parent / "queries"


class CypherLoader:
    """Loads and caches .cypher query files."""

    _cache: dict[str, str] = {}

    @classmethod
    def load(cls, name: str) -> str:
        if name not in cls._cache:
            path = QUERIES_DIR / f"{name}.cypher"
            if not path.exists():
                msg = f"Query file not found: {path}"
                raise FileNotFoundError(msg)
            cls._cache[name] = path.read_text().strip()
        return cls._cache[name]

    @classmethod
    def clear_cache(cls) -> None:
        cls._cache.clear()


async def execute_query(
    session: AsyncSession,
    query_name: str,
    parameters: dict[str, Any] | None = None,
) -> list[Record]:
    """Execute a named .cypher query with parameter binding."""
    cypher = CypherLoader.load(query_name)
    result = await session.run(cypher, parameters or {})
    return [record async for record in result]


async def execute_query_single(
    session: AsyncSession,
    query_name: str,
    parameters: dict[str, Any] | None = None,
) -> Record | None:
    """Execute a named query and return a single record."""
    cypher = CypherLoader.load(query_name)
    result = await session.run(cypher, parameters or {})
    return await result.single()
