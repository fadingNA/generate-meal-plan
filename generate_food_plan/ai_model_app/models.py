from typing import Any
from django.db import models

# Create your models here.

class TextGenerateLoader(models.Model):
    def __init__(self) -> None:
         self.loader = None

    
    def set_loader(self,file_path,**kwargs):
        if file_path.endswith('.csv'):
            self.loader = DirectoryLoader(file_path, glob="**/*.csv", show_progress=True, use_multithreading=True)
        else:
            self.loader = DirectoryLoader(file_path, glob="**/*.txt", show_progress=True, use_multithreading=True)
        return self.loader

    def load(self, file_path, **kwargs):
        self.set_loader(file_path, **kwargs)
        return self.set_loader.load()