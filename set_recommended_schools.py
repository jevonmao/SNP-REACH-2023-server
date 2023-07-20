import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('credential.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://neurodiversityprojectgroupa-default-rtdb.firebaseio.com/'
})

ref = db.reference("schools")
result = ref.get()

school_ids = []
for school_id, school_info in result.items():
    if school_info.get("accommodations") is not None:
        school_ids.append(school_id)

recommended_ref = db.reference("recommended_schools")
recommended_ref.set(school_ids)
