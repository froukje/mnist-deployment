import io
import httpx
from PIL import Image

img_file = open("..data/extra/cat_01.png", "rb").read()
image = Image.open(io.BytesIO(img_file))
res = httpx.post("http://127.0.0.1:8080/predictions/CatsDogs", data=img_file)
res.json()
