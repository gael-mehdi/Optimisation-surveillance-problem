from collections import defaultdict

# Fonction pour lire les données à partir du fichier
def lire_donnees(nom_fichier):
    obstacles = []
    cibles = []
    
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            mots = ligne.strip().split()
            if len(mots) > 1:
                if mots[0] == 'OBSTACLE':
                    obstacles.append((int(mots[1]), int(mots[2])))
                elif mots[0] == 'CIBLE':
                    cibles.append((int(mots[1]), int(mots[2])))
    
    return obstacles, cibles

# Fonction pour trouver les cases vides couvertes par une cible
def trouver_cases_vides(obstacles, cible, lignes, colonnes):
    cases_vides = set()
    
    # Vérification dans la direction verticale (haut)
    for i in range(cible[0]-1, -1, -1):
        if (i, cible[1]) in obstacles:
            break
        cases_vides.add((i, cible[1]))
    
    # Vérification dans la direction verticale (bas)
    for i in range(cible[0]+1, lignes):
        if (i, cible[1]) in obstacles:
            break
        cases_vides.add((i, cible[1]))
    
    # Vérification dans la direction horizontale (gauche)
    for j in range(cible[1]-1, -1, -1):
        if (cible[0], j) in obstacles:
            break
        cases_vides.add((cible[0], j))
    
    # Vérification dans la direction horizontale (droite)
    for j in range(cible[1]+1, colonnes):
        if (cible[0], j) in obstacles:
            break
        cases_vides.add((cible[0], j))
    
    return cases_vides

# Fonction principale pour placer les surveillants
def placer_surveillants(obstacles, cibles, lignes, colonnes):
    surveillants = []
    cases_a_surveiller = set()
    
    for cible in cibles:
        cases_vides = trouver_cases_vides(obstacles, cible, lignes, colonnes)
        
        # Vérifier si la cible peut être vue par un surveillant existant
        vue_possible = False
        for surveillant in surveillants:
            if surveillant.intersection(cases_vides):
                vue_possible = True
                break
        
        if not vue_possible:
            cases_a_surveiller.update(cases_vides)
    
    while cases_a_surveiller:
        position_surveillant = cases_a_surveiller.pop()
        surveillants.append({position_surveillant})
        
        # Mettre à jour les cases à surveiller
        cases_a_surveiller -= {position_surveillant}
        for cible in cibles:
            if position_surveillant in trouver_cases_vides(obstacles, cible, lignes, colonnes):
                cases_a_surveiller -= trouver_cases_vides(obstacles, cible, lignes, colonnes)
    
    return surveillants

# Fonction pour afficher les positions des surveillants
def afficher_surveillants(surveillants):
    for i, surveillant in enumerate(surveillants):
        print(f"Surveillant {i+1} : {surveillant}")

# Boucle pour traiter toutes les instances
for i in range(1, 17):
    instance_path = f'Instances-20230612/gr{i}.txt'

    # Lecture des données à partir du fichier
    obstacles, cibles = lire_donnees(instance_path)

    # Détermination du nombre de lignes et de colonnes à partir des données
    lignes = max(max(obstacles)[0], max(cibles)[0]) + 1
    colonnes = max(max(obstacles)[1], max(cibles)[1]) + 1

    # Placement des surveillants
    surveillants = placer_surveillants(obstacles, cibles, lignes, colonnes)

    """
    # Affichage des positions des surveillants
    afficher_surveillants(surveillants)
    print(f"Solution pour l'instance {instance_path} traitée.")
    """

    # Enregistrement des positions des surveillants dans le fichier de solution
    solution_path = f'res_{i}.txt'
    with open(solution_path, 'w') as file:
        file.write("EQUIPE lionel pepsi\n")
        file.write(f"INSTANCE {i}\n")
        for surveillant in surveillants:
            for position in surveillant:
                file.write(f"{position[0]} {position[1]}\n")

    print(f"Solution pour l'instance {instance_path} enregistrée dans {solution_path}.")
