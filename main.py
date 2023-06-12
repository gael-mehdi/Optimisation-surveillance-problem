"""
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

import random
import math

def load_grid(file_path):
    grid = []
    targets = []
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
                targets.append((int(x), int(y)))
                grid[int(x)][int(y)] = True
            elif line.startswith('OBSTACLE'):
                _, x, y = line.split()
                grid[int(x)][int(y)] = False
    return grid, targets

def place_guards(grid, targets):
    # Fonction de coût pour évaluer la qualité d'une solution
    def cost(guards):
        cost = 0
        for x, y in guards:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < columns:
                    if grid[nx][ny] and (nx, ny) not in guards:
                        cost += 1
        # Vérification de la visibilité de toutes les cibles par les gardiens
        for x, y in targets:
            if (x, y) not in guards:
                visible = False
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < columns:
                            if (nx, ny) in guards:
                                visible = True
                                break
                    if visible:
                        break
                if not visible:
                    cost += 1
        return cost

    rows = len(grid)
    columns = len(grid[0])

    # Initialisation d'une solution initiale aléatoire
    guards = random.sample(targets, math.ceil(len(targets) / 2))

    # Paramètres pour l'algorithme du recuit simulé
    temperature = 100.0
    cooling_rate = 0.99
    min_temperature = 1.0

    while temperature > min_temperature:
        # Sélection d'un voisin aléatoire en échangeant un gardien avec une cible non couverte
        neighbor = guards.copy()
        i = random.randint(0, len(guards) - 1)
        j = random.randint(0, len(targets) - 1)
        neighbor[i] = targets[j]

        # Calcul du coût de la solution actuelle et du voisin
        current_cost = cost(guards)
        neighbor_cost = cost(neighbor)

        # Acceptation du voisin avec une certaine probabilité même s'il est moins optimal
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / temperature):
            guards = neighbor

        # Refroidissement de la température
        temperature *= cooling_rate

    return guards

# Boucle pour traiter toutes les instances
for i in range(1, 17):
    instance_path = f'Instances-20230612/gr{i}.txt'
    solution_path = f'res_{i}.txt'

    # Chargement de la grille
    grid, targets = load_grid(instance_path)

    # Placement des gardiens
    guards = place_guards(grid, targets)

    # Enregistrement des positions des gardiens dans le fichier de solution
    with open(solution_path, 'w') as file:
        file.write("EQUIPE lionel pepsi\n")
        file.write(f"INSTANCE {i}\n")
        for guard in guards:
            file.write(f"{guard[0]} {guard[1]}\n")

    print(f"Solution pour l'instance {instance_path} enregistrée dans {solution_path}.")