import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="monitoraggio hotel",
    user="postgres",
    password="osteria2015"
)

print("Connessione riuscita!")

conn.close()