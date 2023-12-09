import requests
import os

def send_payment_req(amount, serial, servicename):
    data = {
        "success": False 
    }
    # convert to cents
    amountcents  = int(amount) * 100
    # Replace these values with your actual URL, authorization token, and payload
    url = 'https://payments.yoco.com/api/checkouts'
    authorization_token = 'Bearer ' + str(os.environ.get("YOCO_TEST_KEY"))
    payload = {'amount': amountcents, 'servicename': servicename, "currency": "ZAR"}
    print(payload)

    # Define headers with Authorization
    headers = {
        'Authorization': authorization_token,
        'Content-Type': 'application/json',  # Adjust the content type according to your payload
    }

    # Make a POST request with headers and payload
    response = requests.post(url, headers=headers, json=payload)

    # Check the response status code
    if response.status_code == 200:
        print("Request successful!")
        print("Response:")
        print(response.json())
        data["success"] = True
        data["yoco"] = response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response:")
        print(response.text)
        data["yoco"] = response.text
    return data
