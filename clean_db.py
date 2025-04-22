import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Удаляем таблицу, если она есть
cursor.execute("DROP TABLE IF EXISTS tasks_entry")

conn.commit()
conn.close()

print("✅ Таблица tasks_entry удалена (если существовала).")
