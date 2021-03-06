import sys
from app import db

if len(sys.argv) < 2:
    print("Usage: python3 -m spider.spdump http://some.doma.in")
    quit()
domain = sys.argv[1]

res = db.session.execute("SELECT id FROM webs where url = :wu", {"wu": domain})
try:
    web_id = next(res)[0]
except StopIteration:
    print(f"No such domain found in database: {domain}")
    quit()

res = db.session.execute(
    '''SELECT COUNT(from_id) AS inbound, old_rank, new_rank, id, url
    FROM pages JOIN links ON pages.id = links.to_id
    WHERE html IS NOT NULL AND pages.web_id = :wi
    GROUP BY id ORDER BY inbound DESC''',
    {"wi": web_id}
)

count = 0
for row in res:
    if count < 50 : print(row)
    count = count + 1
print((count, 'rows.'))
