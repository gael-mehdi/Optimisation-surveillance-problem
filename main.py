def load_grid(file_path):
    grid = []
    with open(file_path, 'r') as file:
        rows = None
        columns = None
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

def count_visible_targets(grid, x, y):
    rows = len(grid)
    columns = len(grid[0])
    count = 0

    # Vérifier les cibles visibles vers la droite
    for i in range(y, columns):
        if grid[x][i] == 'CIBLE':
            count += 1
        if grid[x][i] == 'OBSTACLE':
            break

    # Vérifier les cibles visibles vers la gauche
    for i in range(y, -1, -1):
        if grid[x][i] == 'CIBLE':
            count += 1
        if grid[x][i] == 'OBSTACLE':
            break

    # Vérifier les cibles visibles vers le bas
    for i in range(x, rows):
        if grid[i][y] == 'CIBLE':
            count += 1
        if grid[i][y] == 'OBSTACLE':
            break

    # Vérifier les cibles visibles vers le haut
    for i in range(x, -1, -1):
        if grid[i][y] == 'CIBLE':
            count += 1
        if grid[i][y] == 'OBSTACLE':
            break

    return count

def place_guards(grid):
    guards = []
    rows = len(grid)
    columns = len(grid[0])

    while True:
        best_guard = None
        max_visible_targets = 0

        # Parcourir toutes les positions de gardien possibles
        for x in range(rows):
            for y in range(columns):
                if grid[x][y] == 'CIBLE':
                    visible_targets = count_visible_targets(grid, x, y)
                    if visible_targets > max_visible_targets:
                        max_visible_targets = visible_targets
                        best_guard = (x, y)

        # S'il n'y a plus de cibles visibles, sortir de la boucle
        if best_guard is None:
            break

        # Supprimer les cibles visibles par le meilleur gardien
        x, y = best_guard
        for i in range(y, columns):
            if grid[x][i] == 'CIBLE':
                grid[x][i] = False
            if grid[x][i] == 'OBSTACLE':
                break
        for i in range(y, -1, -1):
            if grid[x][i] == 'CIBLE':
                grid[x][i] = False
            if grid[x][i] == 'OBSTACLE':
                break
        for i in range(x, rows):
            if grid[i][y] == 'CIBLE':
                grid[i][y] = False
            if grid[i][y] == 'OBSTACLE':
                break
        for i in range(x, -1, -1):
            if grid[i][y] == 'CIBLE':
                grid[i][y] = False
            if grid[i][y] == 'OBSTACLE':
                break

        guards.append(best_guard)

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