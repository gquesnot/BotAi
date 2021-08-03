import os
import json


def getJson(name, directory=""):
    directory = "json/" + directory
    files = os.listdir(directory)
    for file in files:
        if name + ".json" in file:
            with open(os.path.join(directory, file)) as jsonFile:
                data = json.load(jsonFile)
            return data
    return []


def applyJsonConfig(obj, name, directory=""):
    for k, v in getJson(name, directory=directory).items():
        setattr(obj, k, v)


def toJson(name, data, directory=""):
    directory = "json/" + directory
    with open(os.path.join(directory, name + ".json"), 'w') as f:
        json.dump(data, f, indent=2)


def appendJson(name, data, directory=""):
    datastore = getJson(directory, name)
    if name == "verifiedLol":
        del data['birthdate']
        del data['confirm_password']
        mail = data['email'][0] + "@" + data['email'][1]
        data['email'] = mail

    datastore.append(data)
    directory = "json/" + directory
    with open(os.path.join(directory, name + ".json"), 'w') as f:
        json.dump(datastore, f, indent=2)


def jsonPrint(dataName, data):
    print(dataName + ":", json.dumps(data, indent=2))
