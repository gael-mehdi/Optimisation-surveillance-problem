#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef struct {
    int x;
    int y;
} Position;

typedef struct {
    Position target;
    int isCovered;
} Target;

typedef struct {
    int numRows;
    int numCols;
    Position *obstacles;
    int numObstacles;
    Target *targets;
    int numTargets;
} Grid;

void readGridFromFile(const char *filename, Grid *grid) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier.\n");
        exit(1);
    }

    char line[100];
    fgets(line, sizeof(line), file);
    sscanf(line, "LIGNES %d", &(grid->numRows));

    fgets(line, sizeof(line), file);
    sscanf(line, "COLONNES %d", &(grid->numCols));

    int maxNumObstacles = grid->numRows * grid->numCols;
    grid->obstacles = (Position *)malloc(maxNumObstacles * sizeof(Position));
    grid->numObstacles = 0;

    int maxNumTargets = grid->numRows * grid->numCols;
    grid->targets = (Target *)malloc(maxNumTargets * sizeof(Target));
    grid->numTargets = 0;

    while (fgets(line, sizeof(line), file) != NULL) {
        char type[10];
        Position position;
        sscanf(line, "%s %d %d", type, &(position.x), &(position.y));

        if (strcmp(type, "OBSTACLE") == 0) {
            grid->obstacles[grid->numObstacles++] = position;
        } else if (strcmp(type, "CIBLE") == 0) {
            Target target;
            target.target = position;
            target.isCovered = 0;
            grid->targets[grid->numTargets++] = target;
        }
    }

    fclose(file);
}

int isPositionOccupied(Grid grid, Position position) {
    for (int i = 0; i < grid.numObstacles; i++) {
        if (grid.obstacles[i].x == position.x && grid.obstacles[i].y == position.y) {
            return 1;
        }
    }
    return 0;
}

int isTargetCovered(Grid grid, Position position) {
    for (int i = 0; i < grid.numTargets; i++) {
        if (grid.targets[i].target.x == position.x && grid.targets[i].target.y == position.y) {
            return grid.targets[i].isCovered;
        }
    }
    return 0;
}

int countUncoveredTargets(Grid grid) {
    int count = 0;
    for (int i = 0; i < grid.numTargets; i++) {
        if (grid.targets[i].isCovered == 0) {
            count++;
        }
    }
    return count;
}

int main() {
    Grid grid;
    readGridFromFile("Instances-20230612/gr1.txt", &grid);

    int numGuardians = 0;

    for (int i = 0; i < grid.numTargets; i++) {
        if (!grid.targets[i].isCovered) {
            Position position = grid.targets[i].target;
            int j = position.y;
            while (j < grid.numCols && !isPositionOccupied(grid, position)) {
                for (int k = 0; k < grid.numTargets; k++) {
                    if (grid.targets[k].target.x == position.x && !grid.targets[k].isCovered) {
                        grid.targets[k].isCovered = 1;
                    }
                }
                position.y++;
                j++;
            }
            numGuardians++;
        }
    }

    int numUncoveredTargets = countUncoveredTargets(grid);

    printf("Nombre de gardiens nécessaires : %d\n", numGuardians);
    printf("Nombre de cibles non surveillées : %d\n", numUncoveredTargets);

    free(grid.obstacles);
    free(grid.targets);

    return 0;
}