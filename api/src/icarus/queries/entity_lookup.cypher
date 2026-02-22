MATCH (e)
WHERE (e:Person AND e.cpf = $identifier)
   OR (e:Company AND e.cnpj = $identifier)
RETURN e, labels(e) AS entity_labels, elementId(e) AS entity_id
LIMIT 1
