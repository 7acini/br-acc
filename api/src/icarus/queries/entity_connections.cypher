MATCH (e)-[r]-(connected)
WHERE elementId(e) = $entity_id
RETURN e, r, connected,
       labels(e) AS source_labels,
       labels(connected) AS target_labels,
       type(r) AS rel_type,
       elementId(e) AS source_id,
       elementId(connected) AS target_id,
       elementId(r) AS rel_id
