import sys

class Node(): # presents one position in the maze during search
    def __init__(self, state, parent, action):
        self.state = state # current cell position (row, column)
        self.parent = parent # previous node use to reach this cell
        self.action = action # the movement used to reach it: up, down, left, or right
# example.
# Node(state=(2, 4), parent=previous_node, action="right")
# means that the algorithm reached row 2, column 4 by moving right from previous_node.
#The parent attribute is important because it lets the program trace backward from B to A after it finds the goal.



class StackFrontier():
#A frontier stores states that have been discovered but not yet explored.


    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)# add at the end 

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
# or def contains_state(self, state):
#        for node in self.frontier:
#            if node.state == state:
#                return True

#    return False

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1] # remove the last node
            self.frontier = self.frontier[:-1] # readjust the frontier
            return node



class QueueFrontier(StackFrontier): # inherit the StackFrontier

    def remove(self): # only override the remove method that act like queue
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0] # remove the node at the start
            self.frontier = self.frontier[1:] # readjust the frontier
            return node


#Maze.__init__(): reading the maze

class Maze():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()#This reads the complete text maze into contents.
            print ("contents:")
            print (type(contents))
            print (contents)


        # Validate start and goal, #The maze must have: exactly one A exactly one B If there are zero or multiple start/goal characters, the program stops with an error.

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")
        


        # Determine height and width of maze, # height: number of lines in the file width: length of the longest line
        
        contents = contents.splitlines()
        
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
      #  print("contents[i][j]", contents[1][1])
#OR
#        self.width = 0
#        for line in contents:
#           if len(line) > self.width:
#               self.width = len(line)
            
# Keep track of walls The program creates a two-dimensional list called:
# Each cell stores either: True == wall or  False == open space

#Therefore: A is open and saved as the start position.
#B is open and saved as the goal position.
#A blank space is open. Any other character is treated
#as a wall (row, column) eg (0,0) means the top-left cell.
#The coordinate format is:
        self.walls = []
        for i in range(self.height):    
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None # it attribute of maze class

#print(): terminal display

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

#This function receives the current position and returns valid neighboring positions.
#state = (3, 5)
#| Action | Candidate position |
#| ------ | ------------------ |
#| Up     | (2, 5)             |
#| Down   | (4, 5)             |
#| Left   | (3, 4)             |
#| Right  | (3, 6)             |
    
    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
#This condition ensures that the candidate cell:
#Is inside the maze boundaries.
#Is not a wall.
#if ((0 <= r and r < self.height) and (0 <= c and c < self.width) and
# (not self.walls[r][c])):
#    result.append((action, (r, c)))
#Only valid open cells are returned
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


#This is the main AI-search portion of the program.


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        #The start node has:state = location of A parent = None, because it has no previous cell
        #action = None, because no movement was needed to reach the start
        start = Node(state=self.start, parent=None, action=None)

  # ---------------- DFS ----------------
        # Uses a stack: last node added is explored first.
        #frontier = StackFrontier()

        # ---------------- BFS ----------------
        # To use BFS instead, comment the above DFS line and remove
        # the # from the next line:
        #
        frontier = QueueFrontier()
        # --------------------------------------

        frontier.add(start)

        # Initialize an empty explored set
        # This set stores positions already visited by the search.
        # It prevents the algorithm from repeatedly revisiting the same cells and getting stuck in cycles.
        self.explored = set()

        # Keep looping until solution found
        #The program keeps exploring until it finds the goal or runs out of possible cells.


        while True: 

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                    #Goal B → parent → parent → parent → Start A
                    #However, this produces the route in reverse order, from goal to start.
                    #So it reverses both lists:


                actions.reverse()
                cells.reverse()
#self.solution = (
#   ["right", "right", "down", "down"],
#   [(0, 1), (0, 2), (1, 2), (2, 2)]
#)
                
                self.solution = (actions, cells)
                #print ("type(self.solution):",type(self.solution))
                return

            # Mark node as explored
            #If the current node is not the goal, the program marks it explored:


            self.explored.add(node.state)

            # Add neighbors to frontier
            #Then it checks all valid neighboring cells:
            #This condition prevents duplicate exploration:
      
            for action, state in self.neighbors(node.state):
                #The neighbor must be: not already waiting in the frontier and not already explored
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action) #Then it creates and adds a child node:


                    frontier.add(child)#This preserves the chain of parent references needed to reconstruct the final path.




    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1]) #This creates a Maze object and passes the input filename, for example maze.txt.
print("Maze:")
m.print()
print("Solving...")

m.solve()
print("States Explored:", m.num_explored)
print("Solution: of DSF:")
m.print()
m.output_image("maze2_BFS2.png", show_explored=True)
