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

# Exemple d'utilisation
file_path = 'Instances-20230612/gr1.txt'
grid = load_grid(file_path)
guards = place_guards(grid)
print("Coordonnées des gardiens :")
for guard in guards:
    print(guard)
