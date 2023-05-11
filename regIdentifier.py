import requests
import json

url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

reg="AA19AAA"
payload = "{\n\t\"registrationNumber\": \" "+reg+"\"\n}"

headers = {
  'x-api-key': 'INSERT DVLA KEY HERE FOR UK PLATES',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)
data = json.loads(response.text)
#Info available: reggistrationNumber, taxStatus, taxDueDate,motStatus,make,yearOfManfacture,engineCapacity,
#co2Emissions,fuelType,markedForExport,colour,typeApproval,revenueWeight,euroStatus,dateOfLastV5CIssued,motExpiryDate,wheelplan,monthOfFirstRegistration
print(data)
