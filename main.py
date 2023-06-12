def load_grid(file_path):
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('LIGNES'):
                rows = int(line.split()[1])
                grid = [[False] * rows for _ in range(rows)]
            elif line.startswith('COLONNES'):
                columns = int(line.split()[1])
                if len(grid) != 0:
                    for row in grid:
                        row.extend([False] * (columns - len(row)))
            elif line.startswith('CIBLE'):
                _, x, y = line.split()
                grid[int(x)][int(y)] = 'CIBLE'
            elif line.startswith('OBSTACLE'):
                _, x, y = line.split()
                grid[int(x)][int(y)] = 'OBSTACLE'
    return grid

def place_guards(grid):
    guards = []
    rows = len(grid)
    columns = len(grid[0])
    for x in range(rows):
        for y in range(columns):
            if grid[x][y] == 'CIBLE':
                for i in range(y, columns):
                    if grid[x][i] == 'OBSTACLE':
                        break
                    grid[x][i] = True
                for i in range(y, -1, -1):
                    if grid[x][i] == 'OBSTACLE':
                        break
                    grid[x][i] = True
                guards.append((x, y))
    return guards

"""
# Exemple d'utilisation
file_path = 'Instances-20230612/gr1.txt'
grid = load_grid(file_path)
guards = place_guards(grid)
print("Coordonnées des gardiens :")
for guard in guards:
    print(guard)

# Enregistrement des positions des gardiens dans le fichier sol1.txt
with open('sol1.txt', 'w') as file:
    for guard in guards:
        file.write(f"{guard[0]} {guard[1]}\n")

print("Positions des gardiens enregistrées dans sol1.txt.")
"""

# Boucle pour traiter toutes les instances
for i in range(1, 17):
    instance_path = f'Instances-20230612/gr{i}.txt'
    solution_path = f'res{i}.txt'

    # Chargement de la grille
    grid = load_grid(instance_path)

    # Placement des gardiens
    guards = place_guards(grid)

    # Enregistrement des positions des gardiens dans le fichier de solution
    with open(solution_path, 'w') as file:
        file.write("EQUIPE lionel pepsi\n")
        file.write(f"INSTANCE {i}\n")
        for guard in guards:
            file.write(f"{guard[0]} {guard[1]}\n")

    print(f"Solution pour l'instance {instance_path} enregistrée dans {solution_path}.")