import json


def load():
    try:
        with open("data.json", "r") as file:
            model = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        model = []

    return model


def add(data: dict):
    model = load()
    model.append(data)

    with open("data.json", "w") as file:
        json.dump(model, file, indent=4, default=str)
