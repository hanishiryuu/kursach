# Modified Tower of Hanoi solution for 8 towers and custom allowed transitions

# Setup initial towers from the student ID
student_id = "70194603"  # example ID; this can be changed as needed
towers = {peg: [] for peg in range(1, 9)}
for idx, ch in enumerate(student_id):
    peg = 8 - idx                        # tower numbers 8 down to 1
    count = int(ch)
    # Each tower gets 'count' disks labeled M*10+1 ... M*10+count (M = peg number)
    # We store disks in descending order (largest at bottom, smallest at top)
    if count > 0:
        disks = [peg * 10 + n for n in range(1, count+1)]
        towers[peg] = sorted(disks, reverse=True)
print(towers)

# Allowed transitions graph (adjacency list)
allowed = {
    1: [2, 3],
    2: [1, 3],
    3: [2, 4],
    4: [3, 5],
    5: [4, 6],
    6: [5, 7],
    7: [6, 8],
    8: [6, 7]
}

move_count = 0  # counter for moves

# Helper function to log a move
def log_move(disk, src, dst):
    global move_count
    move_count += 1
    print(f"перемещен диск {disk} с башни {src} на башню {dst}")

# Move the top disk from tower `src` to `dst` (assuming the move is legal)
def move_top_disk(src, dst):
    disk = towers[src].pop()        # remove top disk from source
    towers[dst].append(disk)        # place it on destination
    for row in range(72):
        if towers_2d[row][src-1][0] == disk // 10:
            towers_2d[row][src-1] = (0, "#000000")
            break
    for row in range(72):
        if towers_2d[row][dst-1][0] == 0:
            towers_2d[row][dst-1] = (disk // 10, "#000000")  # Assuming color "#000000" for simplicity
            break
    log_move(disk, src, dst)

# Recursive function to ensure tower `peg` can accept a disk of diameter `d`
# by moving any smaller top disks out of the way.
def free_top(peg, max_diameter, exclude=set()):
    # If peg is empty or top disk is larger than the disk we want to place, it's free
    if not towers[peg] or towers[peg][-1] > max_diameter:
        return
    # Otherwise, move the smaller top disk out
    top_small = towers[peg][-1]
    # Try all allowed neighbors of this peg as temporary storage
    for neighbor in allowed[peg]:
        if neighbor == 1 or neighbor in exclude:
            continue  # skip Tower 1 (final target) and already used pegs
        # Check size rule for neighbor: can it accept the smaller disk?
        if not towers[neighbor] or towers[neighbor][-1] < top_small:
            # Recursively free the neighbor if needed (in case neighbor has even smaller on top)
            free_top(neighbor, top_small, exclude | {peg})
            # Move the smaller disk to the neighbor
            move_top_disk(peg, neighbor)
            # After moving, recursively ensure peg is free for the larger disk
            free_top(peg, max_diameter, exclude)
            return

    # If no neighbor found in the first loop (avoiding Tower 1), we may allow moving to Tower 1 
    # as a last resort (this situation is rare if strategy is followed, but included for completeness).
    for neighbor in allowed[peg]:
        if neighbor in exclude:
            continue
        if not towers[neighbor] or towers[neighbor][-1] < top_small:
            free_top(neighbor, top_small, exclude | {peg})
            move_top_disk(peg, neighbor)
            free_top(peg, max_diameter, exclude)
            return

# Recursive function to move disk `d` from its current tower to Tower 1.
def move_to_target(d):
    # Find which tower currently holds disk d
    src = next(peg for peg, stack in towers.items() if d in stack)
    if src == 1:
        return  # already at target
    # Find a path from src to target (Tower 1) using BFS on the allowed graph
    from collections import deque
    parents = {src: None}
    queue = deque([src])
    while queue:
        peg = queue.popleft()
        if peg == 1:
            break
        for neigh in allowed[peg]:
            if neigh not in parents:      # not visited yet
                parents[neigh] = peg
                queue.append(neigh)
    # Reconstruct path from src to 1
    path = []
    peg = 1
    while peg is not None:
        path.append(peg)
        peg = parents[peg]
    path.reverse()  # now it's [src, ..., 1]

    # Move disk d along the path one step at a time
    for i in range(len(path) - 1):
        cur = path[i]
        nxt = path[i+1]
        # Make sure `nxt` peg is free (no smaller disk blocking) for disk d
        free_top(nxt, d, exclude={cur})
        # Perform the move from cur to nxt
        move_top_disk(cur, nxt)

# Initialize towers_2d for disk visualization
towers_2d = [[(0, "#000000") for _ in range(8)] for _ in range(72)]
for peg, stack in towers.items():
    for i, disk in enumerate(reversed(stack)):
        towers_2d[i][peg-1] = (disk // 10, "#000000")  # Assuming color "#000000" for simplicity

# Execute the plan: move all disks to Tower 1 from largest to smallest
all_disks = sorted([d for stack in towers.values() for d in stack], reverse=True)
for disk in all_disks:
    # Ensure the disk is free to move (no smaller above it on its current tower)
    current_tower = next(peg for peg, stack in towers.items() if disk in stack)
    if towers[current_tower][-1] != disk:
        # Move smaller disks out of the way from the current tower
        free_top(current_tower, disk)
    # Move this disk to Tower 1
    move_to_target(disk)

# After all moves, print total move count
print(f"Всего шагов: {move_count}")
print("Финальное состояние башен:")
for peg, stack in towers.items():
    print(f"Башня {peg}: {stack}")