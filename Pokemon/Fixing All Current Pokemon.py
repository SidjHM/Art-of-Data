import csv
import requests

class Pokemon:
    def __init__(self, id, name, height, weight, type1, type2):
        self.id = id
        self.name = name
        self.height = height
        self.weight = weight
        self.type1 = type1
        self.type2 = type2

    @classmethod
    def from_api(cls, name):
        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            id = data['id']
            height = data['height']
            weight = data['weight']
            types = [t['type']['name'] for t in data['types']]
            type1 = types[0] if len(types) > 0 else ""
            type2 = types[1] if len(types) > 1 else ""
            return cls(id, name.lower(), height, weight, type1, type2)
        else:
            return None

    def __str__(self):
        return f"{self.id},{self.name},{self.height},{self.weight},{self.type1},{self.type2}"

def clean_pokemon_csv(input_filename, output_filename):
    pokemon_list = []

    with open(input_filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader, None)

        for row in reader:
            name = row[1].strip()
            pokemon = Pokemon.from_api(name)

            if pokemon is None:
                if name.lower() == "mr. mime":
                    pokemon = Pokemon.from_api("mr-mime")
                elif name.lower() == "zygarde":
                    pokemon = Pokemon.from_api("718")

            if pokemon:
                pokemon_list.append(pokemon)
            else:
                print(f"Error retrieving data for {name}")

    pokemon_list.sort(key=lambda p: p.id)

    with open(output_filename, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["id", "name", "height (m)", "weight (kg)", "type1", "type2"])

        for pokemon in pokemon_list:
            writer.writerow(str(pokemon).split(','))

clean_pokemon_csv('pokemon_mess.csv', 'pokemon.csv')
