import requests

from dotenv import dotenv_values

config = {
    **dotenv_values('.env')
}

sheet_url = config['sheety_url']

print("Welcome to Cyrus's Flight club ")
print("We find the best flight deals for you and email you")
f_name = input("What is your first name?\n")
l_name = input("What is your last name?\n")
email = input("what is your email?\n")
r_email = input("Type your email again\n")

params = {
    "user": {
        "firstName": f_name.title(),
        "lastName": l_name.title(),
        "email": email

    }
}

if email == r_email:
    print("You're in the club!")
    try:
        result = requests.post(url=f"{sheet_url}/users",
                               json=params).json()

    except ConnectionError:
        print("request failed")
    else:
        print("Success!You're email has been added.")
else:
    print("password doesn't match")
