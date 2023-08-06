import mysql.connector
from google.cloud import firestore

def get(db, buffered=True, dictionary=False):
    schema = firestore.Client().collection("db_schema").document(db).get().to_dict()
    cnx = mysql.connector.connect(
        user=schema['user'],
        password=schema['password'],
        host=schema['host'],
        database=schema['database']
    )
    cur = cnx.cursor(buffered=buffered, dictionary=dictionary)
    return cnx, cur