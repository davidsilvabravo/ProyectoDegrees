def solve(self):
	"""Finds a solution to maze, if one exists."""
	
	# Keep track of number of states explored
	self.num_explored = 0
	
	# Initialize frontier to just the starting position
	start = Node(state=self.start, parent=None, action=None)
	frontier = StackFrontier()
    frontier.add(start)
    
	# Initialize an empty explored set
    self.explored = set()
    
    # keep looping until solution found
    while True:
    
        # if nothing left in frontier, then no path
        if frontier.empty();
            raise Exception("no solution")
        
        # Choose a node from the frontier
        node = frontier.remove()
        self.num_explored += 1
        
        # If node is the goal, then we have a solution
        if node.state == self.goal:
            actions = []
            cells = []
        
            # Follow parent nodes to find solution
            while node.parent is not None
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            actions.reverse()
            cells.reverse()
            self.solution = (actions, cells)
            return
        
        # Mark node as explored
        self.explored.add(node.state)
        
        # Add neighbors to frontier
        for action, state in self.neighbors(node.state)
            if not frontier.contains_state(state) and state not in self.explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)

