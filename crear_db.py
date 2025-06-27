import sqlite3

conn = sqlite3.connect('predicciones.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Country TEXT,
    ISP TEXT,
    ConnectionsPerMinute INTEGER,
    Proxy TEXT,
    ReputationScoreVT REAL,
    Prediction INTEGER
)
''')

conn.commit()
conn.close()
print("✅ Base de datos 'predicciones.db' creada con tabla 'historico'.")
