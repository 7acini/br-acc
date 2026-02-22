MATCH (a)-[r]-(b)
WHERE elementId(a) IN $node_ids AND elementId(b) IN $node_ids
RETURN DISTINCT
    elementId(r) AS rel_id,
    elementId(a) AS source_id,
    elementId(b) AS target_id,
    type(r) AS rel_type,
    properties(r) AS rel_props
