# First, let's define a function to find the node with the smallest distance
# that has not been visited yet

def min_distance ( distances , visited ) :
	# Initialize minimum distance for next node
	min_val = float ( 'inf' )
	min_index = -1
	
	# Loop through all nodes to find minimum distance
	for i in range ( len ( distances ) ) :
		if distances [ i ] < min_val and i not in visited :
			min_val = distances [ i ]
			min_index = i
	
	return min_index


# Now, let's implement Dijkstra's algorithm

def dijkstra_algorithm ( graph , start_node ) :
	# Get total number of nodes in the graph
	num_nodes = len ( graph )
	
	# Initialize distance and visited arrays
	distances = [ float ( 'inf' ) ] * num_nodes
	visited = [ ]
	
	# Set distance at starting node to 0 and add to visited list
	distances [ start_node ] = 0
	
	# Loop through all nodes to find shortest path to each node
	for i in range ( num_nodes ) :
		
		# Find minimum distance node that has not been visited yet
		current_node = min_distance ( distances , visited )
		
		# Add current_node to list of visited nodes
		visited.append ( current_node )
		
		# Loop through all neighboring nodes of current_node
		for j in range ( num_nodes ) :
			
			# Check if there is an edge from current_node to neighbor
			if graph [ current_node ] [ j ] != 0 :
				
				# Calculate the distance from start_node to neighbor,
				# passing through current_node
				new_distance = distances [ current_node ] + graph [ current_node ] [ j ]
				
				# Update the distance if it is less than previous recorded value
				if new_distance < distances [ j ] :
					distances [ j ] = new_distance
	
	# Return the list of the shortest distances to all nodes
	return distances


# Example graph represented as a 2D array
graph = [ [ 0 , 7 , 9 , 0 , 0 , 14 ] ,
          [ 7 , 0 , 10 , 15 , 0 , 0 ] ,
          [ 9 , 10 , 0 , 11 , 0 , 2 ] ,
          [ 0 , 15 , 11 , 0 , 6 , 0 ] ,
          [ 0 , 0 , 0 , 6 , 0 , 9 ] ,
          [ 14.0 , 2 , 0 , 9 , 8 , 10 ] ]

# Call Dijkstra's algorithm to find shortest paths from node 'A' (index of 'A' in the array is 0)
shortest_distances = dijkstra_algorithm ( graph , 0 )  # 'A' is represented by index 0

# Print the resulting shortest distances
print ( shortest_distances )
