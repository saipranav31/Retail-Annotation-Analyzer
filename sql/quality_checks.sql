-- 1. Count records by suggested category
SELECT suggested_label, COUNT(*) AS product_count
FROM annotations
GROUP BY suggested_label
ORDER BY product_count DESC;

-- 2. Records requiring manual review
SELECT i.item_id, i.product_name, a.suggested_label, a.review_reason
FROM items i
JOIN annotations a ON a.item_id = i.item_id
WHERE a.needs_review = 1
ORDER BY i.item_id;

-- 3. Compare suggestions with reference labels
SELECT i.item_id, i.product_name, a.suggested_label, g.gold_label,
       CASE WHEN a.suggested_label = g.gold_label THEN 'MATCH' ELSE 'MISMATCH' END AS result
FROM items i
JOIN annotations a ON a.item_id = i.item_id
JOIN gold g ON g.item_id = i.item_id
ORDER BY i.item_id;

-- 4. Reference-set match rate by reference category
SELECT g.gold_label,
       COUNT(*) AS reference_count,
       SUM(CASE WHEN a.suggested_label = g.gold_label THEN 1 ELSE 0 END) AS matches,
       ROUND(100.0 * SUM(CASE WHEN a.suggested_label = g.gold_label THEN 1 ELSE 0 END) / COUNT(*), 2) AS match_pct
FROM gold g
JOIN annotations a ON a.item_id = g.item_id
GROUP BY g.gold_label
ORDER BY match_pct;

-- 5. Product IDs with no reference label
SELECT i.item_id, i.product_name
FROM items i
LEFT JOIN gold g ON g.item_id = i.item_id
WHERE g.item_id IS NULL;
