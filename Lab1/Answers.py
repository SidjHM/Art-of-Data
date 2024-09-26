import csv

def load_digimon_data(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

digimon_data = load_digimon_data('digimon.csv')

def average_hp(digimon_data):
    return sum(int(digimon['HP']) for digimon in digimon_data) / len(digimon_data)

print(f"Average HP of all Digimon: {average_hp(digimon_data)}")

def count_digimon(attribute, value):
    return sum(1 for digimon in digimon_data if digimon[attribute] == value)

print(f"Number of Vaccine-type Digimon: {count_digimon('Type', 'Vaccine')}")

def find_team(digimon_data, memory_limit=15, min_total_atk=300):
    teams = [(d1['Digimon'], d2['Digimon'], d3['Digimon'],
              int(d1['Atk']) + int(d2['Atk']) + int(d3['Atk']),
              int(d1['Memory']) + int(d2['Memory']) + int(d3['Memory']))
             for d1 in digimon_data for d2 in digimon_data for d3 in digimon_data
             if d1 != d2 != d3 and int(d1['Memory']) + int(d2['Memory']) + int(d3['Memory']) <= memory_limit
             and int(d1['Atk']) + int(d2['Atk']) + int(d3['Atk']) >= min_total_atk]
    return teams

team = find_team(digimon_data)
if team:
    t = team[0]  # Print the first team found
    print(f"Team: {t[0]}, {t[1]}, {t[2]} | Total Atk: {t[3]}, Total Memory: {t[4]}")
else:
    print("No team found.")
