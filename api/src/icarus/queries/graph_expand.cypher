MATCH path = (center)-[*1..2]-(connected)
WHERE elementId(center) = $entity_id
WITH center, relationships(path) AS rels, nodes(path) AS path_nodes
UNWIND path_nodes AS n
WITH center, rels, COLLECT(DISTINCT n) AS unique_nodes
UNWIND unique_nodes AS node
WITH center, rels, node, labels(node) AS node_labels, elementId(node) AS node_id
WHERE $entity_types IS NULL
   OR ANY(label IN node_labels WHERE toLower(label) IN $entity_types)
RETURN DISTINCT
    node, node_labels, node_id,
    elementId(center) AS center_id
