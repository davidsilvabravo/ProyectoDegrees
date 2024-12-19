import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# names es un diccionario que relaciona nombres con un conjunto de person_ids
# (es posible que múltiples actores tengan el mismo nombre)
names = {}

# people es un diccionario que relaciona person_ids con un diccionario que contiene
# name, birth, movies (un conjunto de movie_ids)
people = {}

# movies es un dccionario que relaciona movie_ids con un diccionario que contiene
# title, year, stars (un conjunto de person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            # Ejm:
            # people[person_id = 102] = {name: "Kevin Bacon", birth: 1958, movies: ...}

            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])
                # en caso que el nombre de la persona aparezca varias veces, se añade a la lista de person_id
                # Ejm:
                # names["kevin bacon"] = {102, 103, 104, person_id ...}

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }
            # Ejm:
            # movies[movie_id = 112384] = {title: "Apollo 13", year: 1995, stars: ...}

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                # Ejm: ver la línea 33 -> películas asociadas a la persona con person_id = 102
                # people[person_id = 102]["movies"] = {104257, 112384, ...}

                movies[row["movie_id"]]["stars"].add(row["person_id"])
                # Ejm: personas asociadas a la película con movie_id = 104257
                # movies[movie_id = 112384]["stars"] = {102, 158, 200, 641, person_id}
            except KeyError:
                pass


def main():

    # checks if the number of command-line arguments (sys.argv) is greater than 2
    # includes the script name as the first element
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    
    # If exactly two arguments are provided (the script name and one additional argument)
    #  directory is set to the value of the second argument
    #  otherwise, if only the script name is provided (one argument),
    #  directory is set to the default value "large"
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # ====================================================================================================
    # Imprimimos para ver la data que se ha cargado

    # movies
    print ("\nmovies:\n")
    print ("movie_id | title | year | stars")
    for m in movies:
        print(m + " | " + movies[m]["title"] + " | " + movies[m]["year"] + " | ", end='')
        for s in movies[m]["stars"]:
            print(s + " ", end='')
        print()
    print()

    # people
    print ("\npeople:\n")
    print ("person_id | name | birth | movies")
    for p in people:
        print(p + " | " + people[p]["name"] + " | " + people[p]["birth"] + " | ", end='')
        for m in people[p]["movies"]:
            print(m + " ", end='')
        print()
    print()

    # names
    print ("\nnames:\n")
    print ("names | person_ids (homonimos)")
    for n in names:
        print(n + " | " , end='')
        for p in names[n]:
            print(p + " ", end='')
        print()
    print()

    # ====================================================================================================
    #Source:
    source_id = person_id_for_name(input("\nSource Name: "))  # lista
    if source_id is None:
        sys.exit("Source person not found.")
    
    print(source_id + " | " + people[source_id]["name"] + " | " + people[source_id]["birth"] + " | ", end='')
    print("movie_ids: ", end='')
    for m in people[source_id]["movies"]:
        print(m + " ", end='')
    print()

    #Target:
    target_id = person_id_for_name(input("\nTarget Name: "))  # lista
    if target_id is None:
        sys.exit("Target person not found.")

    print(target_id + " | " + people[target_id]["name"] + " | " + people[target_id]["birth"] + " | ", end='')
    print("movie_ids: ", end='')
    for n in people[target_id]["movies"]:
        print(n + " ", end='')
    print("\n")

    # path es una lista de tuplas representando una secuencia de conecciones o pasos,
    # donde cada tupla contiene 2 elements (movie_id, person_id)
    path = shortest_path(source_id, target_id)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        # (list of movies, list of people)
        path = [(None, source_id)] + path
        for i in range(degrees):
            # people[person_id = 102] = {name: "Kevin Bacon", birth: 1958, movies: ...}
            person1 = people[path[i][1]]["name"]     # person1 = "Kevin Bacon"
            person2 = people[path[i + 1][1]]["name"] # person2 = "Tom Cruise"

            # movies[idMovies] = {title: "Apollo 13", year: 1995, stars: ...}
            movie = movies[path[i + 1][0]]["title"]  # 

            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


# Ejm:
#  source: "Mandy Patinkin" (person_id = 1597)
#  target: "Kevin Bacon"    (person_id = 102)
def shortest_path(source_id, target_id):
# By using breadth-first search, we can find the shortest path from one actor to another
    """
    Returns the shortest list of (movie_id, person_id) pairs that connect the source to the target
    If no possible path, returns None
    """
    # Keep track of number of states explored
    num_explored = 0

    # Initialize frontier to just the starting position
    start = Node(state=source_id, parent=None, action=None) # our states are people, our actions are movies
                                                            # CREO QUE action tiene que ser la lista de películas
                                                            # de la persona del correspondiente source_id
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:

        # if nothing left in frontier, then no path
        if frontier.empty():
            raise Exception("no solution")

        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1

        # If node is the goal, then we have a solution
        if node.state == target_id: # our states are people
            actions = []
            cells = []
        
            # Follow parent nodes to find solution
            while node.parent is not None:
                actions.append(node.action) # our actions are movies
                cells.append(node.state) # our states are people
                node = node.parent
            actions.reverse()
            cells.reverse()
            solution = []
            for i in range(len(actions)):
                solution.append((actions[i], cells[i]))
            return solution # (movies, people)
        
        # If node is NOT the goal
        # Mark node as explored
        explored.add(node.state) # our states are people

        # Add neighbors to frontier
        # Para todos los vecinos de la persona...
        # si no está en la frontera y no ha sido explorado, se añade a la frontera
        for action, state in neighbors_for_person(node.state): # our states are people
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


def person_id_for_name(name):
    # names["kevin bacon"] = {102}
    # obtiene una lista de person_id cuyo combre coincide con el nombre ingresado
    # si no encuentra el nombre, devuelve None
    person_ids = list(names.get(name.lower(), set()))

    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        # si hay varias personas que tengan el mismo nombre, pregunta cuál de ellas
        print(f"Which '{name}'?")

        for person_id in person_ids:
            # people[person_id = 102] = {name: "Kevin Bacon", birth: 1958, movies: ...}
            # people[person_id = 102]["movies"] = {104257, 112384, ...}
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else: # len(person_ids) == 1
        return person_ids[0]


def neighbors_for_person(person_id):
    # Para la persona identificada con un determinado person_id
    # se obtiene la lista de pares (movie_id, person_id)
    # que corresponde a los actores que participaron en las mismas películas
    #
    # Ejm:
    # si person_id = 102
    # y en el conjunto people se tiene:
    # people[person_id = 102] = {name: "Kevin Bacon", birth: 1958, movies: ...}
    # people[person_id = 102]["movies"] = {104257, 112384, ...}
    # entonces
    # neighbors = { (104257, 102), (112384, 102) }

    movie_ids = people[person_id]["movies"] # {104257, 112384}

    neighbors = set() # se inicializa un conjunto vacío

    # para cada película en la que participó la persona
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
            # neighbors = { (104257, 102), (104257, 129), (104257, 193), (104257, 197), 
            #               (112384, 102), (112384, 158), (112384, 200), (112384, 641) }
    return neighbors


if __name__ == "__main__":
    main()
