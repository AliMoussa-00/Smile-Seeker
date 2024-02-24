"""init file to choose the storage type and get the data"""

from os import getenv

storage_type = getenv("SS_DB_TYPE")

if storage_type == "db":
    from models.engine.db_storage import DBStorage

    storage = DBStorage()

else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()

storage.reload()
