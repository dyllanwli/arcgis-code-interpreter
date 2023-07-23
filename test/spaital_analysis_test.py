import requests
import geopandas as gpd


# Here is the link https://arcgis.com/home/item.html?id=787ded9b852d4d90936e167fb5673edf
shape_file_path = "./Redlands_Parks.zip"


url = "http://localhost:3000/api/upload"

with open(shape_file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.text)