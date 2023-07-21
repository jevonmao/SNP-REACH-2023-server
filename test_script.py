from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import firebase_admin
cred = credentials.Certificate('credential.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://neurodiversityprojectgroupa-default-rtdb.firebaseio.com/',
    'storageBucket': 'neurodiversityprojectgroupa.appspot.com'
})
bucket = storage.bucket()
blobs = bucket.list_blobs()
image_urls = []
for blob in blobs:
    blob.make_public()
    print(blob.public_url)
