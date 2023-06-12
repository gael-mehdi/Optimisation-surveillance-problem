from ortools.linear_solver import pywraplp

def load_grid(file_path):
    grid = []
    cibles = []
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
                grid[int(x)][int(y)] = True
                cibles.append((int(x), int(y)))
            elif line.startswith('OBSTACLE'):
                _, x, y = line.split()
                grid[int(x)][int(y)] = False
    return grid, cibles

def resoudre_probleme_gardiens(grid, cibles):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    rows = len(grid)
    columns = len(grid[0])

    gardiens = [[solver.BoolVar(f"Gardien_{x}_{y}") for y in range(columns)] for x in range(rows)]

    # Contrainte : Chaque cible doit être couverte par au moins un gardien
    for x, y in cibles:
        solver.Add(sum(gardiens[x][y] for y in range(columns)) >= 1)

    # Contrainte : Un gardien ne peut pas être placé sur un obstacle
    for x in range(rows):
        for y in range(columns):
            if not grid[x][y]:
                solver.Add(gardiens[x][y] == 0)

    # Fonction objectif : Minimiser le nombre total de gardiens
    objective = solver.Objective()
    for x in range(rows):
        for y in range(columns):
            objective.SetCoefficient(gardiens[x][y], 1)
    objective.SetMinimization()

    # Résolution du problème
    solver.Solve()

    guards = []
    if solver.Status() == pywraplp.Solver.OPTIMAL:
        for x in range(rows):
            for y in range(columns):
                if gardiens[x][y].solution_value() > 0:
                    guards.append((x, y))
                    print(f"Gardien placé à la position ({x}, {y})")
    else:
        print("Aucune solution optimale trouvée.")

    return guards

# Heuristique pour optimiser le placement des gardiens
def optimiser_placement_gardiens(grid, cibles):
    rows = len(grid)
    columns = len(grid[0])

    # Initialiser la liste des gardiens
    guards = []

    # Parcourir toutes les cibles
    for target_x, target_y in cibles:
        # Calculer la distance minimale
        min_distance = float('inf')
        best_guard = None

        # Parcourir toutes les positions possibles pour un gardien
        for x in range(rows):
            for y in range(columns):
                if grid[x][y]:
                    # Calculer la distance entre le gardien potentiel et la cible
                    distance = abs(target_x - x) + abs(target_y - y)

                    # Si la distance est plus courte, mettre à jour le meilleur gardien
                    if distance < min_distance:
                        min_distance = distance
                        best_guard = (x, y)

        # Ajouter le meilleur gardien à la liste
        guards.append(best_guard)

        # Mettre à jour la grille pour empêcher d'autres gardiens d'être placés sur la même position
        grid[best_guard[0]][best_guard[1]] = False

    return guards

# Boucle pour traiter toutes les instances
for i in range(1, 17):
    instance_path = f'Instances-20230612/gr{i}.txt'
    solution_path = f'res_{i}.txt'

    # Chargement de la grille et des cibles
    grid, cibles = load_grid(instance_path)

    # Placement des gardiens
    guards = optimiser_placement_gardiens(grid, cibles)

    # Enregistrement des positions des gardiens dans le fichier de solution
    with open(solution_path, 'w') as file:
        file.write("EQUIPE lionel pepsi\n")
        file.write(f"INSTANCE {i}\n")
        for guard in guards:
            file.write(f"{guard[0]} {guard[1]}\n")

    print(f"Solution pour l'instance {instance_path} enregistrée dans {solution_path}.")