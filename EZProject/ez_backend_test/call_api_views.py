import requests

def call_signup_api(username, email, password):
    api_url = 'http://127.0.0.1:8000/signup/'

    data = {
        'username': username,
        'email': email,
        'password': password,
    }

    try:
        response = requests.post(api_url, data=data)
        
        print('Raw Response:', response.text)

        response_data = response.json()

        if response.status_code == 200:
            print('Signup successful:', response_data['message'])
        elif response.status_code == 400:
            print('Error:', response_data.get('error', 'Unknown error'))
        else:
            print('Unexpected response:', response.status_code)

    except requests.RequestException as e:
        print('Error making API request:', str(e))

def call_login_api(username, password):
    api_url = 'http://127.0.0.1:8000/login/'

    data = {
        'username': username,
        'password': password,
    }

    try:
        response = requests.post(api_url, data=data)
        response_data = response.json()

        if response.status_code == 200:
            print('Login successful:', response_data['message'])
        elif response.status_code == 400:
            print('Error:', response_data['error'])
        else:
            print('Unexpected response:', response.status_code)

    except requests.RequestException as e:
        print('Error making API request:', str(e))

def call_fetch_upload():
    api_url = 'http://127.0.0.1:8000/api/upload/'
    data = {}
    try:
        response = requests.get(api_url, data=data)
        response_data = response.json() 
        print('files', response_data)

    except requests.RequestException as e:
        print('Error making API request:', str(e))


def get_file_list():
    api_url = "http://127.0.0.1:8000/api/files/"
    response = requests.get(api_url)

    if response.status_code == 200:
        file_list = response.json()
        return file_list
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    username = 'tedh'
    email = 'vikas@gmail.com'
    password = 'secretpassword'

    #call_signup_api(username, email, password)
   # call_login_api(username, password)
    #call_fetch_upload()

    # files = get_file_list()
    # if files:
    #     for file in files:
    #         print(f"File ID: {file['id']}, File Name: {file['file']}")

if __name__ == "__main__":
    main()
