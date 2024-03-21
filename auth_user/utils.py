from pymongo import MongoClient
def get_db_handle(db_name, host, port, username, password):
 client = MongoClient(host="localhost",
                      port=int(27017),
                     )
 db_handle = client['drr']
 return db_handle, client