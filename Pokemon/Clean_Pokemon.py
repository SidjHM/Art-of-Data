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
    def from_api(cls, identifier):
        url = f"https://pokeapi.co/api/v2/pokemon/{identifier}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            id = data['id']
            name = data['name']
            height = data['height']
            weight = data['weight']
            types = [t['type']['name'] for t in data['types']]
            type1 = types[0] if len(types) > 0 else ""
            type2 = types[1] if len(types) > 1 else ""
            return cls(id, name, height, weight, type1, type2)
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
            name = row[1].strip().lower()  # Normalize name to lowercase
            pokemon = Pokemon.from_api(name)

            if pokemon is None:
                if name == "mr. mime":
                    pokemon = Pokemon.from_api("mr-mime")
                elif name == "zygarde":
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

def fetch_all_pokemon(output_filename):
    all_pokemon_list = []

    for id in range(1, 1026):
        pokemon = Pokemon.from_api(id)
        if pokemon:
            all_pokemon_list.append(pokemon)
        else:
            print(f"Error retrieving data for Pokemon ID {id}")

    all_pokemon_list.sort(key=lambda p: p.id)

    with open(output_filename, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["id", "name", "height (m)", "weight (kg)", "type1", "type2"])

        for pokemon in all_pokemon_list:
            writer.writerow(str(pokemon).split(','))

# Run the functions to clean existing data and fetch all Pokemon data
clean_pokemon_csv('pokemon_mess.csv', 'cleaned_pokemon.csv')
fetch_all_pokemon('all_pokemon.csv')
