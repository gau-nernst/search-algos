class Search():
    valid_strat = {'bfs', 'dfs', 'ldfs', 'ids', 'ucs', 'greedy', 'a_star'}
    
    def __init__(self, strategy):
        assert strategy in self.valid_strat
        self.strat = strategy
        
    def __call__(self, start, end, adj_list, max_depth=3, heuristic=None):
        print("Strategy:", self.strat)
        print("Start:", start)
        print("End:", end)
        print()
        if self.strat == 'dfs' or self.strat == 'bfs':
            self.bfs_dfs(self.strat, start, end, adj_list)
            
        elif self.strat == 'ldfs':
            self.ldfs(start, end, adj_list, max_depth=max_depth)
            
        elif self.strat == 'ids':
            for i in range(1, max_depth+1):
                print("Max depth:", i)
                self.ldfs(start, end, adj_list, max_depth=i)
                print()
                print()
        elif self.strat == 'ucs':
            self.ucs(start, end, adj_list)
        elif self.strat == 'greedy':
            self.greedy(start, end, adj_list, heuristic=heuristic)
        elif self.strat == 'a_star':
            self.a_star(start, end, adj_list, heuristic=heuristic)

    def bfs_dfs(self, strat, start, end, adj_list):
        from collections import deque
        assert strat == 'bfs' or strat == 'dfs'
        
        if strat == 'dfs':
            candidates = []
        elif strat == 'bfs':
            candidates = deque()

        candidates.append(start)
        visited = set()
        parent = {}
        step = 1

        while candidates:
            print("Step", step)
            step += 1
            
            if strat == 'dfs':
                current_node = candidates.pop()
            elif strat == 'bfs':
                current_node = candidates.popleft()
            
            print("Current node:", current_node)
            
            if current_node == end:
                print("Found the destination")
                print()
                self.print_path(start, end, parent, adj_list)
                return

            visited.add(current_node)
            print("Visited nodes:", visited)
            print(f"Neighbors of {current_node}: {adj_list[current_node]}")
            print()

            for x in adj_list[current_node]:
                if x not in visited and x not in candidates:
                    candidates.append(x)
                    parent[x] = current_node

            print("Candidates:", candidates)
            if candidates: 
                print("Next node to examine:", candidates[-1] if strat == 'dfs' else candidates[0])
            print()
            print()

        print(f"Does not found a path from {start} to {end}")
    
    def ldfs(self, start, end, adj_list, max_depth=1):
        candidates = []
        candidates.append((start,0))
        
        parent = {}
        step = 1

        print("start:", candidates)
        print()
        print()

        while candidates:
            print("Step", step)
            step += 1
            
            current_node, depth = candidates.pop() 
            print("Current node:", current_node)
            print("Current depth:", depth)
            print(f"Neighbors of {current_node}: {adj_list[current_node]}")
            
            if current_node == end:
                print("Found the destination")
                print()
                self.print_path(start, end, parent, adj_list)
                return

            if depth < max_depth:
                for x in adj_list[current_node]:
                    if current_node in parent and x == parent[current_node]:
                        continue
                        
                    candidates.append((x,depth+1))
                    parent[x] = current_node
            else:
                print("Reach max depth")
            
            print(candidates)
            print()
            print()
                
        print(f"Does not found a path from {start} to {end} with depth {depth}")
        
    def ucs(self, start, end, adj_list):
        candidates = set()
        path_cost = {}
        parent = {}
        
        step = 1
        
        candidates.add(start)
        path_cost[start] = 0
        
        while candidates:
            print("Step", step)
            step += 1
            
            min_node = None
            min_cost = float('inf')
            for node in candidates:
                if path_cost[node] < min_cost:
                    min_node = node
                    min_cost = path_cost[node]
            
            candidates.remove(min_node)
            current_node = min_node
            print("Current node:", current_node)
            
            if current_node == end:
                print("Found the destination")
                print()
                self.print_path(start, end, parent, adj_list)
                return
            
            print(f"Neighbors of {current_node}: {adj_list[current_node]}")
            print("Path cost:", path_cost)
            print()
            
            for x in adj_list[current_node]:
                if x in parent and parent[x] == current_node:
                    continue
                    
                new_cost = path_cost[current_node] + adj_list[current_node][x]
                if x not in path_cost or new_cost < path_cost[x]:
                    parent[x] = current_node
                    path_cost[x] = new_cost
                    candidates.add(x)
            print("Candidates:", candidates)
            print()
            print()
        print(f"Does not found a path from {start} to {end} with depth {depth}")
        
    def greedy(self, start, end, adj_list, heuristic):
        assert heuristic
        
        current_node = start
        path = []
        
        step = 1
        path.append(start)
        
        while current_node != end:
            print("Step", step)
            step += 1
            
            print("Current node:", current_node)
            neighbors = list(adj_list[current_node].keys())
            neighbors_est_cost = [heuristic(x, end) for x in neighbors]
            if not neighbors:
                print(f"Does not found a path from {start} to {end} with depth {depth}")
                return
            n = {neighbors[i]: round(neighbors_est_cost[i]) for i in range(len(neighbors))}
            print(f"Neighbors of {current_node}: {n}")
            
            next_node = None
            min_est_cost = float('inf')
            
            for i in range(len(neighbors)):
                if neighbors_est_cost[i] < min_est_cost:
                    next_node = neighbors[i]
                    min_est_cost = neighbors_est_cost[i]
            
            path.append(next_node)
            current_node = next_node
            
            print()
            print()
            
        print("Found the destination")
        print()
        print("Full path: ", end="")
        print(*path, sep=' → ')

        total = 0
        for i in range(len(path)-1):
            a = path[i]
            b = path[i+1]
            total += adj_list[a][b]
            print(f"\t{a} → {b}: {adj_list[a][b]}")
        print(f"Total cost: {total}")       
            
    def a_star(self, start, end, adj_list, heuristic):
        assert heuristic
        
        candidates = set()
        path_cost = {}
        heuristic_cost = {}
        parent = {}
        
        step = 1
        candidates.add(start)
        path_cost[start] = 0
        
        while candidates:
            print("Step", step)
            step += 1
            
            min_node = None
            min_cost = float('inf')
            for node in candidates:
                if node not in heuristic_cost:
                    heuristic_cost[node] = heuristic(node, end)
                
                total_cost = path_cost[node] + heuristic_cost[node]
                if total_cost < min_cost:
                    min_node = node
                    min_cost = total_cost
            
            candidates.remove(min_node)
            current_node = min_node
            print("Current node:", current_node)
            
            if current_node == end:
                print("Found the destination")
                print()
                self.print_path(start, end , parent, adj_list)
                return
            
            print(f"Neighbors of {current_node}: {adj_list[current_node]}")
            print("Path cost:", path_cost)
            n = {k: round(v) for k,v in heuristic_cost.items()}
            print("Heuristic cost:", n)
            print()
            
            for x in adj_list[current_node]:
                if x in parent and parent[x] == current_node:
                    continue
                    
                new_cost = path_cost[current_node] + adj_list[current_node][x]
                if x not in path_cost or new_cost < path_cost[x]:
                    parent[x] = current_node
                    path_cost[x] = new_cost
                    candidates.add(x)
            print("Candidates:", candidates)
            print()
            print()
        print(f"Does not found a path from {start} to {end} with depth {depth}")  
        
    def print_path(self, start, end, parent, adj_list):
        print("Full path: ", end="")

        x = end
        path = [x]
        while x != start:
            x = parent[x]
            path.append(x)
        path.reverse()
        print(*path, sep=' → ')

        total = 0
        for i in range(len(path)-1):
            a = path[i]
            b = path[i+1]
            total += adj_list[a][b]
            print(f"\t{a} → {b}: {adj_list[a][b]}")
        print(f"Total cost: {total}")