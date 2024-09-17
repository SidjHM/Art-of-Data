import csv

# Initialize variables for grouping and calculations
species_data = {}
species_mass = {}
chinstrap_dream_island_count = 0

# Read the data from the CSV file
with open("penguins_size.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        species = row['species']
        culmen_length = row['culmen_length_mm']
        body_mass = row['body_mass_g']
        island = row['island']

        if culmen_length != 'NA' and body_mass != 'NA':
            culmen_length = float(culmen_length)
            body_mass = float(body_mass)

            if species not in species_data:
                species_data[species] = {'total_bill_length': 0, 'count': 0}
                species_mass[species] = {'total_mass': 0, 'count': 0}

            species_data[species]['total_bill_length'] += culmen_length
            species_data[species]['count'] += 1

            species_mass[species]['total_mass'] += body_mass
            species_mass[species]['count'] += 1

        if species == 'Chinstrap' and island == 'Dream':
            chinstrap_dream_island_count += 1

average_bill_length = {species: data['total_bill_length'] / data['count'] for species, data in species_data.items()}

longest_bill_species = max(average_bill_length, key=average_bill_length.get)
longest_bill_value = average_bill_length[longest_bill_species]

print(
    f"The species with the longest bills on average is {longest_bill_species} with an average bill length of {longest_bill_value:.2f} mm.")

average_body_mass = {species: data['total_mass'] / data['count'] for species, data in species_mass.items()}

most_massive_species = max(average_body_mass, key=average_body_mass.get)
most_massive_value = average_body_mass[most_massive_species]

print(
    f"The most massive species on average is {most_massive_species} with an average body mass of {most_massive_value:.2f} grams.")

print(f"The number of Chinstrap penguins on Dream Island is {chinstrap_dream_island_count}.")
