from datetime import datetime

# Get the timestamp
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Data to serve with our API
PEOPLE = {
    "Farrell":{
            "fname":"Doug",
            "lname":"Farrell",
            "timestamp":get_timestamp()
    },
    "Brockman":{
        "fname":"Kent",
        "lanme":"Brockman",
        "timestamp":get_timestamp()
    },
    "Easter":{
        "fname":"Bunny",
        "lname":"Easter",
        "timestamp":get_timestamp()
    }
}

# Method to read the data from the above dictionary
def read():
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]