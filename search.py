import psycopg2
import re
import time

def parse_query(query):
    tokens = query.strip().split()
    tags = [t[1:] for t in tokens if t.startswith('#')]
    keywords = ' '.join(t for t in tokens if not t.startswith('#'))
    return tags, keywords

def search_db(query_input):
    tags, keyword = parse_query(query_input)

    conn = psycopg2.connect(
        dbname="search_engine", user="postgres", password="password", host="localhost", port=5432
    )
    cur = conn.cursor()

    sql = f"""
    WITH tag_filter AS (
        SELECT c.id
        FROM collections c
        JOIN collection_tags ct ON c.id = ct.collection_id
        JOIN tags t ON t.id = ct.tag_id
        WHERE t.name = ANY(%s)
        GROUP BY c.id
        HAVING COUNT(DISTINCT t.name) = %s
    )
    SELECT 'collection' AS type, c.id, c.name
    FROM collections c
    WHERE (%s = '') OR (c.name ILIKE %s)
      AND (%s = 0 OR c.id IN (SELECT id FROM tag_filter))

    UNION ALL

    SELECT 'container' AS type, cn.id, cn.name
    FROM containers cn
    JOIN collections c ON c.id = cn.collection_id
    WHERE (%s = '') OR (cn.name ILIKE %s)
      AND (%s = 0 OR c.id IN (SELECT id FROM tag_filter))
    LIMIT 50;
    """

    pattern = f"%{keyword}%" if keyword else ""
    params = [tags, len(tags), keyword, pattern, len(tags), keyword, pattern, len(tags)]

    start = time.time()
    cur.execute(sql, params)
    results = cur.fetchall()
    duration = time.time() - start

    print(f"\nResults (in {duration:.3f} seconds):")
    for row in results:
        print(f"{row[0].capitalize()} - {row[2]} (ID: {row[1]})")

    cur.close()
    conn.close()

if __name__ == "__main__":
    while True:
        q = input("\nEnter search query (or 'exit'): ")
        if q.strip().lower() == "exit":
            break
        search_db(q)
