import os
from uuid import uuid4

def rename_imagefile_to_uuid(instance, filename):
        upload_to = f'article/'
        ext = filename.split('.')[-1]
        uuid = uuid4().hex

        filename = f'article_{instance}_{uuid}.{ext}'
        
        return os.path.join(upload_to, filename)