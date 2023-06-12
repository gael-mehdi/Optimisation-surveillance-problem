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
                # Check if the target is already covered by a guard
                is_covered = False
                for guard in guards:
                    if guard[0] == x or guard[1] == y:
                        is_covered = True
                        break

                if not is_covered:
                    # Place a guard at the target
                    guards.append((x, y))
                    for i in range(y+1, columns):
                        if grid[x][i] == 'OBSTACLE':
                            break
                        grid[x][i] = True
                    for i in range(y-1, -1, -1):
                        if grid[x][i] == 'OBSTACLE':
                            break
                        grid[x][i] = True
    return guards

# Boucle pour traiter toutes les instances
for i in range(1, 17):
    instance_path = f'Instances-20230612/gr{i}.txt'
    solution_path = f'res_{i}.txt'

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
