"""init file to choose the storage type and get the data"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
