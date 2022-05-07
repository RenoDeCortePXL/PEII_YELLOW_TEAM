import requests

def main():
    print("YELLOW LAB - HACS (HIGHLY ADVANCED CLIENT SYSTEM)")
    print("------------------------------------------------\n\n")
    print("Welcome to our 2022 interface!")
    print("You can now query our web api directly from the command line!")
    print("To  get started, type out the name, or areacode of the city you would like to know more about")
    print("To quit, type exit\n")

    # token opvragen van de identity server, client credentials wordt in de body gezet.
    token_url = "http://localhost:5002/connect/token"
    params = {"client_id": "CloudMaarten", "client_secret": "spruitjes", "grant_type": "client_credentials",
              "scope": "krc-genk"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post(token_url, data=params, headers=headers)
    token = r.text.split(':')[1].split(',')[0][1:-1]

    # met de token heeft de applicatie nu toegang tot alle seatholders
    token_url = "http://localhost:5000/api/seatholders"
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(token_url, headers=headers)  # get request sturen met Bearer token

    # Data wordt als 1 grote string terug gestuurd, dit omvormen naar een list met dictionaries
    suscribers = r.text[2:-2].split("},{")
    suscribers_dict = []
    for s in suscribers:
        suscribers_dict.append(eval("{" + s + "}"))

    # City of area code opvragen tot de gebruiker 'exit' invoert
    name_or_code = input("Enter city or areacode: ")
    while not (name_or_code == "exit"):
        people = 0

        # bepalen invoer city of area code
        if (name_or_code.isnumeric()):
            for suscriber in suscribers_dict:
                if suscriber['areaCode'] == int(name_or_code):
                    people += 1
        else:
            for suscriber in suscribers_dict:
                if str.upper(suscriber['city']) == str.upper(name_or_code):
                    people += 1

        # Resultaten afprinten
        print("There are", people, "suscribed from", name_or_code)
        name_or_code = input("Enter city or areacode: ")

if __name__ == '__main__':
    main()
