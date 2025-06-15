import psycopg2
from faker import Faker
import random

fake = Faker()
N_COLLECTIONS = 10000
N_CONTAINERS = 90000
TAGS = ['test', 'prod', 'demo', 'ci', 'secure']

def seed():
    conn = psycopg2.connect(
        dbname="search_engine", user="postgres", password="password", host="localhost", port=5432
    )
    cur = conn.cursor()

    print("Seeding tags...")
    tag_ids = {}
    for tag in TAGS:
        cur.execute("INSERT INTO tags (name) VALUES (%s) RETURNING id", (tag,))
        tag_ids[tag] = cur.fetchone()[0]
    conn.commit()

    print("Seeding collections...")
    for _ in range(N_COLLECTIONS):
        name = fake.catch_phrase() + " Collection"
        cur.execute("INSERT INTO collections (name) VALUES (%s) RETURNING id", (name,))
        cid = cur.fetchone()[0]

        for _ in range(random.randint(1, 3)):
            tag = random.choice(TAGS)
            cur.execute("INSERT INTO collection_tags (collection_id, tag_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (cid, tag_ids[tag]))
    conn.commit()

    print("Seeding containers...")
    for _ in range(N_CONTAINERS):
        name = fake.bs().capitalize() + " Container"
        collection_id = random.randint(1, N_COLLECTIONS)
        cur.execute("INSERT INTO containers (name, collection_id) VALUES (%s, %s)", (name, collection_id))
    conn.commit()

    cur.close()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    seed()
