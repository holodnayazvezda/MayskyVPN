import sqlite3


async def get_inbound_id(remark: str) -> int:
    conn = sqlite3.connect('data/databases/inbounds.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM inbouds WHERE remark = ?;", (remark,))
    inbound_id = cursor.fetchone()[0]
    conn.close()
    return inbound_id
