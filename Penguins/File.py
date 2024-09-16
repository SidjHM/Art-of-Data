import pandas as pd

penguins = pd.read_csv("penguins_size.csv")

average_bill_length = penguins.groupby("species")["culmen_length_mm"].mean()
longest_bill_species = average_bill_length.idxmax()
longest_bill_value = average_bill_length.max()

print(f"The species with the longest bills on average is {longest_bill_species} with an average bill length of {longest_bill_value:.2f} mm.")

average_body_mass = penguins.groupby("species")["body_mass_g"].mean()

most_massive_species = average_body_mass.idxmax()
most_massive_value = average_body_mass.max()

print(f"The most massive species on average is {most_massive_species} with an average body mass of {most_massive_value:.2f} grams.")

chinstrap_dream_island = penguins[(penguins["species"] == "Chinstrap") & (penguins["island"] == "Dream")]

num_chinstrap_dream = chinstrap_dream_island.shape[0]

print(f"The number of Chinstrap penguins on Dream Island is {num_chinstrap_dream}.")
