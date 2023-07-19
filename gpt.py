import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('credential.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://neurodiversityprojectgroupa-default-rtdb.firebaseio.com/'
})

ref = db.reference('')
ref = ref.child('schools')
