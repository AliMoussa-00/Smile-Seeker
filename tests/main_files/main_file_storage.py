"""main file to test file storage"""
from models.base_model import BaseModel
import models

b1 = BaseModel()
b2 = BaseModel({"name": "Ali", "age": 23})

models.storage.new(b1)
models.storage.new(b2)
models.storage.save()
print(models.storage.all())
print("--" * 20)
print(models.storage.all(BaseModel))

models.storage.delete(b2)
models.storage.save()
