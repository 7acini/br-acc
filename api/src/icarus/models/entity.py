from pydantic import BaseModel


class SourceAttribution(BaseModel):
    database: str
    record_id: str | None = None
    extracted_at: str | None = None


class EntityResponse(BaseModel):
    id: str
    type: str
    properties: dict[str, str | float | int | bool | None]
    sources: list[SourceAttribution]
    is_pep: bool = False


class ConnectionResponse(BaseModel):
    source_id: str
    target_id: str
    relationship_type: str
    properties: dict[str, str | float | int | bool | None]
    confidence: float = 1.0
    sources: list[SourceAttribution]


class EntityWithConnections(BaseModel):
    entity: EntityResponse
    connections: list[ConnectionResponse]
    connected_entities: list[EntityResponse]
