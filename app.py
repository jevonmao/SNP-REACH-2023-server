from flask import Flask, jsonify, request
import os
import openai
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests

app = Flask(__name__)

def get_state(zip_string):
    if not isinstance(zip_string, str):
        print('Must pass the zipcode as a string.')
        return
    if len(zip_string) != 5:
        print('Must pass a 5-digit zipcode.')
        return
    zipcode = int(zip_string)
    st = None
    state = None
    if 35000 <= zipcode <= 36999:
        st = 'AL'
        state = 'Alabama'
    elif 99500 <= zipcode <= 99999:
        st = 'AK'
        state = 'Alaska'
    elif 85000 <= zipcode <= 86999:
        st = 'AZ'
        state = 'Arizona'
    elif 71600 <= zipcode <= 72999:
        st = 'AR'
        state = 'Arkansas'
    elif 90000 <= zipcode <= 96699:
        st = 'CA'
        state = 'California'
    elif 80000 <= zipcode <= 81999:
        st = 'CO'
        state = 'Colorado'
    elif (6000 <= zipcode <= 6389) or (6500 <= zipcode <= 6999):
        st = 'CT'
        state = 'Connecticut'
    elif 19700 <= zipcode <= 19999:
        st = 'DE'
        state = 'Delaware'
    elif 32000 <= zipcode <= 34999:
        st = 'FL'
        state = 'Florida'
    elif 30000 <= zipcode <= 31999:
        st = 'GA'
        state = 'Georgia'
    elif 96700 <= zipcode <= 96999:
        st = 'HI'
        state = 'Hawaii'
    elif 83200 <= zipcode <= 83999:
        st = 'ID'
        state = 'Idaho'
    elif 60000 <= zipcode <= 62999:
        st = 'IL'
        state = 'Illinois'
    elif 46000 <= zipcode <= 47999:
        st = 'IN'
        state = 'Indiana'
    elif 50000 <= zipcode <= 52999:
        st = 'IA'
        state = 'Iowa'
    elif 66000 <= zipcode <= 67999:
        st = 'KS'
        state = 'Kansas'
    elif 40000 <= zipcode <= 42999:
        st = 'KY'
        state = 'Kentucky'
    elif 70000 <= zipcode <= 71599:
        st = 'LA'
        state = 'Louisiana'
    elif 3900 <= zipcode <= 4999:
        st = 'ME'
        state = 'Maine'
    elif 20600 <= zipcode <= 21999:
        st = 'MD'
        state = 'Maryland'
    elif 1000 <= zipcode <= 2799:
        st = 'MA'
        state = 'Massachusetts'
    elif 48000 <= zipcode <= 49999:
        st = 'MI'
        state = 'Michigan'
    elif 55000 <= zipcode <= 56999:
        st = 'MN'
        state = 'Minnesota'
    elif 38600 <= zipcode <= 39999:
        st = 'MS'
        state = 'Mississippi'
    elif 63000 <= zipcode <= 65999:
        st = 'MO'
        state = 'Missouri'
    elif 59000 <= zipcode <= 59999:
        st = 'MT'
        state = 'Montana'
    elif 27000 <= zipcode <= 28999:
        st = 'NC'
        state = 'North Carolina'
    elif 58000 <= zipcode <= 58999:
        st = 'ND'
        state = 'North Dakota'
    elif 68000 <= zipcode <= 69999:
        st = 'NE'
        state = 'Nebraska'
    elif 88900 <= zipcode <= 89999:
        st = 'NV'
        state = 'Nevada'
    elif 3000 <= zipcode <= 3899:
        st = 'NH'
        state = 'New Hampshire'
    elif 7000 <= zipcode <= 8999:
        st = 'NJ'
        state = 'New Jersey'
    elif 87000 <= zipcode <= 88499:
        st = 'NM'
        state = 'New Mexico'
    elif 10000 <= zipcode <= 14999:
        st = 'NY'
        state = 'New York'
    elif 43000 <= zipcode <= 45999:
        st = 'OH'
        state = 'Ohio'
    elif 73000 <= zipcode <= 74999:
        st = 'OK'
        state = 'Oklahoma'
    elif 97000 <= zipcode <= 97999:
        st = 'OR'
        state = 'Oregon'
    elif 15000 <= zipcode <= 19699:
        st = 'PA'
        state = 'Pennsylvania'
    elif 300 <= zipcode <= 999:
        st = 'PR'
        state = 'Puerto Rico'
    elif 2800 <= zipcode <= 2999:
        st = 'RI'
        state = 'Rhode Island'
    elif 29000 <= zipcode <= 29999:
        st = 'SC'
        state = 'South Carolina'
    elif 57000 <= zipcode <= 57999:
        st = 'SD'
        state = 'South Dakota'
    elif 37000 <= zipcode <= 38599:
        st = 'TN'
        state = 'Tennessee'
    elif 75000 <= zipcode <= 79999:
        st = 'TX'
        state = 'Texas'
    elif 84000 <= zipcode <= 84999:
        st = 'UT'
        state = 'Utah'
    elif 5000 <= zipcode <= 5999:
        st = 'VT'
        state = 'Vermont'
    elif 22000 <= zipcode <= 24699:
        st = 'VA'
        state = 'Virginia'
    elif 20000 <= zipcode <= 20599:
        st = 'DC'
        state = 'Washington DC'
    elif 98000 <= zipcode <= 99499:
        st = 'WA'
        state = 'Washington'
    elif 24700 <= zipcode <= 26999:
        st = 'WV'
        state = 'West Virginia'
    elif 53000 <= zipcode <= 54999:
        st = 'WI'
        state = 'Wisconsin'
    elif 82000 <= zipcode <= 83199:
        st = 'WY'
        state = 'Wyoming'
    else:
        print('Invalid zipcode.')
        return
    return st, state

def fetchSchools(api_client, addy):
    # Create an instance of the API class
    api_instance = schools_service_api.SchoolsServiceApi(api_client)

    # example passing only required values which don't have defaults set
    try:
        # Search Nearby Schools by Address
        api_response = api_instance.get_schools_by_address(addy)
        return api_response        
    
    except com.precisely.apis.ApiException as e:
        print("Exception when calling SchoolsServiceApi->get_schools_by_address: %s\n" % e)

@app.route("/api/v1/parseRaw", methods=[''])
def parseRawText():
    rawContent = request.form.get("content")
    systemPrompt = """
    summarize this content into an overall summary, and a bullet list of special need accommodations, and whether it is TRUE available or FALSE unavailable at this school. make the list comprehensive, not just ones at the school. Always output in JSON format
    """
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": rawContent}
    ]
    )
    response = completion.choices[0].message.content
    return response

def queryAccomodations(schools):
    ref = db.reference("schools")
    ref.set({school["schoolid"] : {"info" : school} for school in schools})


@app.route("/api/v1/getNearbySchools", methods=['GET'])
def getNearbySchools():
    params = request.args
    zip = str(params.get("zip") or "")
    city = str(params.get("city") or "")
    state = str(params.get("state") or "")
    devMode = params.get("devMode")

    '''
    Sort list. Values are: schoolname, distance, rank. For descending order, precede with '-' i.e. -schoolname (optional, default: schoolname)
    '''
    sortBy = str(params.get("sortBy") or "")

    if not zip and not city and not state:
        return jsonify({"error" : "No query parameters provided."})
    if city and zip:
        return jsonify({"error" : "Too many query parameters provided."})
    if city and not state:
        return jsonify({"error" : "Must provide state in parameters."})
    if zip:
        state = get_state(zip)

    if devMode == True or devMode == None:
        mock_json = open("mock.json", "r").read()
        return json.loads(mock_json)
    
    headers = {
    "Accept": "application/json",
    }
    params = {
        "st": state,
        "zip": zip,
        "city": city,
        "appID": os.getenv("APP_ID"),
        "perPage": "50",
        "sortBy": sortBy,
        "appKey": os.getenv("APP_KEY"),
        "level": "public"
    }

    response = requests.get("https://api.schooldigger.com/v2.0/schools", params=params, headers=headers).json()
    print(response["numberOfPages"])
    queryAccomodations(response["schoolList"])
    return response["schoolList"]

openai.api_key = os.getenv("OPENAI_API_KEY")
cred = credentials.Certificate('credential.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://neurodiversityprojectgroupa-default-rtdb.firebaseio.com/'
})

if __name__ == "__main__":
    app.run()