import com.precisely.apis
from com.precisely.apis.api import schools_service_api
from com.precisely.apis.api import addresses_service__api
import os

configuration = com.precisely.apis.Configuration(
    host = "https://api.precisely.com"
)

def schoolAPI(api_client, addy):
    # Create an instance of the API class
    api_instance = schools_service_api.SchoolsServiceApi(api_client)

    # example passing only required values which don't have defaults set
    try:
        # Search Nearby Schools by Address
        api_response = api_instance.get_schools_by_address(addy)
        #school_names = [school.name for school in api_response.school]
        return api_response.school
    
    except com.precisely.apis.ApiException as e:
        print("Exception when calling SchoolsServiceApi->get_schools_by_address: %s\n" % e)

def addressesAPI(api_client, city="", postal=""):
    api_instance = addresses_service__api.AddressesServiceApi(api_client)
    try:
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


with com.precisely.apis.ApiClient(configuration) as api_client:
    api_client.oAuthApiKey = os.getenv("PRECISELY_KEY")
    api_client.oAuthSecret = os.getenv("PRECISELY_SECRET")
    api_client.generateAndSetToken()
    address = addressesAPI(api_client, postal="94305")
    response = schoolAPI(api_client, address)
    #schools = json.loads(str(response))
    print(response)

    