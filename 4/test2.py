from heapq import heappush, heappop
from collections import deque

def solve_towers(initial_id):
    # Define adjacency neighbors for each spindle 1-8
    neighbors = {
        1: [2, 3],
        2: [1, 3],
        3: [1, 2, 4],
        4: [3, 5],
        5: [4, 6],
        6: [5, 7, 8],
        7: [6, 8],
        8: [6, 7]
    }
    # Ensure symmetry
    for peg in range(1, 9):
        for n in neighbors[peg]:
            if peg not in neighbors[n]:
                neighbors[n].append(peg)
    # Compute distances from each peg to target peg1 using BFS
    dist = {i: float('inf') for i in range(1, 9)}
    dist[1] = 0
    dq = deque([1])
    while dq:
        u = dq.popleft()
        for v in neighbors[u]:
            if dist[v] == float('inf'):
                dist[v] = dist[u] + 1
                dq.append(v)
    # Parse initial ID into peg stacks
    s = str(initial_id)
    if len(s) != 8:
        raise ValueError("ID must be 8 digits")
    # Stacks: index0 for peg1, ..., index7 for peg8
    stacks = [[] for _ in range(8)]
    # digits from left (peg8) to right (peg1)
    for i, ch in enumerate(s):
        peg = 8 - i
        count = int(ch)
        for n in range(count, 0, -1):
            disk = peg * 10 + n
            stacks[peg-1].append(disk)
    initial_state = tuple(tuple(peg) for peg in stacks)
    # Build goal state: all disks on peg1 (sorted descending numeric)
    all_disks = []
    for peg in range(1, 9):
        all_disks.extend(stacks[peg-1])
    all_disks.sort(reverse=True)  # largest first (bottom of peg1)
    goal_stacks = [tuple(all_disks)] + [tuple() for _ in range(7)]
    goal_state = tuple(goal_stacks)
    # Heuristic: sum of distances of all disks to peg1 (lower bound on moves)
    def heuristic(state):
        h = 0
        for peg_index in range(1, 9):
            stack = state[peg_index-1]
            count = len(stack)
            if count:
                h += count * dist[peg_index]
        return h
    # A* search
    open_heap = []
    start_h = heuristic(initial_state)
    heappush(open_heap, (start_h, 0, initial_state, []))
    visited = {initial_state: 0}
    while open_heap:
        f, g, state, path = heappop(open_heap)
        if state == goal_state:
            # Output result
            print(len(path))
            for move in path:
                disk, frm, to = move
                print(f"{disk} {frm} {to}")
            return
        if visited.get(state, float('inf')) < g:
            continue
        # Generate moves
        for peg in range(1, 9):
            stack = state[peg-1]
            if not stack:
                continue
            disk = stack[-1]
            for target in neighbors[peg]:
                # Check if move allowed (smaller disk on larger)
                if state[target-1] and state[target-1][-1] < disk:
                    continue
                # Apply move
                new_state = list(list(x) for x in state)
                new_state[peg-1].pop()
                new_state[target-1].append(disk)
                new_state = tuple(tuple(x) for x in new_state)
                new_g = g + 1
                if visited.get(new_state, float('inf')) <= new_g:
                    continue
                visited[new_state] = new_g
                h_val = heuristic(new_state)
                heappush(open_heap, (new_g + h_val, new_g, new_state, path + [(disk, peg, target)]))
    print("No solution found")

if __name__ == "__main__":
    # Initial configuration ID (70194603)
    initial_id = 70194603
    solve_towers(initial_id)