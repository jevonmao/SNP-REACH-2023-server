import os
from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch(os.getenv("GOOGLE_API_KEY"), "c6bcf034c91f74116")
_search_params = {
    'q': 'palo alto high school',
    'img_type': 'photo',
    'img_size': 'medium'
}

gis.search(search_params=_search_params)
print(gis.results()[0].url)