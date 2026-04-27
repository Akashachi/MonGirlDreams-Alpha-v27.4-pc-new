init python:
    import heapq

    class Node():
        """A node class for A* Pathfinding /w heapq - initially from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2"""

        def __init__(self, parent=None, position=None):
            self.parent = parent
            self.position = position

            self.g = 0
            self.h = 0
            self.f = 0

        def __eq__(self, other):
            return self.position == other.position

        def __lt__(self, other):
            return self.f < other.f

    def return_path(current_node):
        path = []
        current = current_node
        while current is not None:
            path.append([current.position[0], current.position[1]] )
            current = current.parent
        return path[::-1]  # Return reversed path

    def astar(maze, start, end, tileset, ActiveGridNPCs, NPCCanShareTile=None, ignoreWalls=0, directions=[[0, -1], [0, 1], [-1, 0], [1, 0]] ):
        """Returns a list of tuples as a path from the given start to the given end in the given maze - initally from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2"""

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize open list, heap eepy
        open_list = []
        heapq.heappush(open_list, (start_node.f, 0, start_node))  # (f, counter, node)

        closed_set = set()

        # Dictionaries for g and f scores
        g_score = {start: 0}
        f_score = {start: 0}

        # For node parent tracking
        came_from = {}

        # Counter for tie-breaking in heap
        counter = 0

        # Adding a stop condition
        outer_iterations = 0
        max_iterations = ((len(maze[0]) * len(maze))*2)

        # Loop until you find the end
        while open_list:
            outer_iterations += 1

            if outer_iterations > max_iterations:
                # If we have a path to end, return it, else return empty because no path was found
                if end in came_from:
                    current = came_from[end]
                    return return_path(current)
                else:
                    return []

            # Get the current node
            current_f, _, current_node = heapq.heappop(open_list)

            # Skip if already processed
            if current_node.position in closed_set:
                continue

            closed_set.add(current_node.position)

            # Found the goal
            if current_node.position == end:
                return return_path(current_node)

            # Generate children
            for new_position in directions: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                #if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                #    continue

                # Make sure walkable terrain
                #if maze[node_position[0]][node_position[1]] != 0:
                #continue
                npcwallHit = 0

                if ignoreWalls == 0:
                    tileTarget = maze[node_position[1]][node_position[0]]
                    if tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                        continue

                    for wallNPC in ActiveGridNPCs:
                        if NPCCanShareTile:
                            # Only block if it's a wall NPC
                            if wallNPC.Wall == "Wall":
                                if wallNPC.coord == [node_position[0], node_position[1]]:
                                    npcwallHit = 1
                                    break
                        else:
                            # Block on walls or NPCs that don't allow sharing
                            if wallNPC.Wall == "Wall" or not wallNPC.CanShareTile:
                                if wallNPC.coord == [node_position[0], node_position[1]]:
                                    npcwallHit = 1
                                    break
                    if npcwallHit == 1:
                        continue

                # Calculate tentative g score
                tentative_g = g_score[current_node.position] + 1

                if node_position not in g_score or tentative_g < g_score[node_position]:
                    # Finding best path to the node
                    came_from[node_position] = current_node
                    g_score[node_position] = tentative_g
                    h = ((node_position[0] - end[0]) ** 2) + ((node_position[1] - end[1]) ** 2)
                    f = tentative_g + h
                    f_score[node_position] = f

                    # Create new node
                    new_node = Node(current_node, node_position)
                    new_node.g = tentative_g
                    new_node.h = h
                    new_node.f = f

                    # Push it to the open list
                    counter += 1
                    heapq.heappush(open_list, (f, counter, new_node))

        return []
