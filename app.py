from flask import Flask, jsonify, request
import os
import openai
import com.precisely.apis
from com.precisely.apis.api import schools_service_api
from com.precisely.apis.api import addresses_service__api
import json

app = Flask(__name__)
precisely_client = None

def fetchBoundaryAddress(api_client, city="", postal=""):
    api_instance = addresses_service__api.AddressesServiceApi(api_client)
    try:
        if not city and not postal:
            return None
        
        # Addresses Count by Boundary Name.
        api_response = api_instance.get_addressesby_boundary_name(country="USA",
                                                                         area_name3=city,
                                                                         post_code=postal)
        addresses = api_response.address_list

        residential_addresses = [address for address in api_response.address_list if address.property_type == "X"]
        if residential_addresses:
            residential_address = residential_addresses[0]
        else:
            residential_address = addresses[0]

        address_str = f"{residential_address.address_number} {residential_address.street_name}, {residential_address.post_code}"
        return address_str

    except com.precisely.apis.ApiException as e:
        print("Exception when calling AddressesServiceApi->get_addresses_count_by_boundary_name: %s\n" % e)

def fetchSchools(api_client, addy):
    # Create an instance of the API class
    api_instance = schools_service_api.SchoolsServiceApi(api_client)

    # example passing only required values which don't have defaults set
    try:
        # Search Nearby Schools by Address
        api_response = api_instance.get_schools_by_address(addy)
        #school_names = [school.name for school in api_response.school]
        response = str(api_response.school)
        # single to double quotes
        return response.replace("'", '"')
    
    except com.precisely.apis.ApiException as e:
        print("Exception when calling SchoolsServiceApi->get_schools_by_address: %s\n" % e)

@app.route("/api/v1/parseRaw", methods=['POST'])
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


@app.route("/api/v1/getNearbySchools", methods=['GET'])
def getNearbySchools():
    params = request.args
    zip = str(params.get("zip") or "")
    city = str(params.get("city") or "")
    address = fetchBoundaryAddress(precisely_client, city, zip)
    schools = fetchSchools(precisely_client, address)
    return schools

openai.api_key = os.getenv("OPENAI_API_KEY")

configuration = com.precisely.apis.Configuration(
    host = "https://api.precisely.com"
)

with com.precisely.apis.ApiClient(configuration) as api_client:
    api_client.oAuthApiKey = os.getenv("PRECISELY_KEY")
    api_client.oAuthSecret = os.getenv("PRECISELY_SECRET")
    api_client.generateAndSetToken()
    precisely_client = api_client


if __name__ == "__main__":
    app.run()