from collections import deque

# === Настройка начальных башен по ID студента ===
student_id = "70194603"  # можно заменить на другой ID
# Храним списки дисков так, что index 0 — самый маленький (низ башни), последний — самый большой (вершина)
towers = {peg: [] for peg in range(1, 9)}
for idx, ch in enumerate(student_id):
    peg = 8 - idx  # башни нумеруются 8…1 слева направо
    count = int(ch)
    if count > 0:
        # диски M*10+1 … M*10+count, от малого к большому
        disks = [peg * 10 + n for n in range(1, count + 1)]
        towers[peg] = disks  # уже по возрастанию: [11,12,13] для башни 1

# Граф разрешённых переходов между башнями
allowed = {
    1: [2, 3],
    2: [1, 3],
    3: [2, 4],
    4: [3, 5],
    5: [4, 6],
    6: [5, 7],
    7: [6, 8],
    8: [6, 7],
}

move_count = 0  # счётчик сделанных ходов

def log_move(disk, src, dst):
    """Логируем и считаем ход."""
    global move_count
    move_count += 1
    print(f"ход {move_count}: перемещен диск {disk} с башни {src} на башню {dst}")

def move_top_disk(src, dst):
    """
    Снятие верхнего диска (последний элемент list) с src
    и установка его на вершину dst (append).
    """
    disk = towers[src].pop()     # снимаем верхний
    towers[dst].append(disk)     # ставим на вершину
    log_move(disk, src, dst)

def free_top(peg, moving_diameter, exclude=None):
    """
    Освобождаем вершину peg от блокирующих дисков,
    чтобы диск диаметра moving_diameter мог на него встать
    (правило: можно ставить только больший диск на меньший).
    exclude — множество башен, временно запрещённых для парковки.
    """
    if exclude is None:
        exclude = set()
    # Если башня пуста или её верхний диск меньше moving_diameter — ничего не надо делать
    if not towers[peg] or towers[peg][-1] < moving_diameter:
        return
    # Иначе снимаем блокирующий диск
    top_small = towers[peg][-1]
    # Попробуем все разрешённые соседи для временного хранения
    for neigh in allowed[peg]:
        if neigh in exclude:
            continue
        # Можно парковать, если башня пуста или её верхний диск меньше top_small
        if not towers[neigh] or towers[neigh][-1] < top_small:
            free_top(neigh, top_small, exclude | {peg})
            move_top_disk(peg, neigh)
            free_top(peg, moving_diameter, exclude)
            return
    # Фоллбек: допускаем любые другие разрешённые (без проверки dst)
    for neigh in allowed[peg]:
        if neigh in exclude:
            continue
        if not towers[neigh] or towers[neigh][-1] < top_small:
            free_top(neigh, top_small, exclude | {peg})
            move_top_disk(peg, neigh)
            free_top(peg, moving_diameter, exclude)
            return

def move_to_target(d):
    """
    Перемещает диск d по кратчайшему маршруту
    от текущей башни до башни 1.
    """
    # Находим башню, где сейчас лежит диск d
    src = next(peg for peg, stack in towers.items() if d in stack)
    if src == 1:
        return
    # Ищем путь BFS от src к 1
    parents = {src: None}
    queue = deque([src])
    while queue:
        u = queue.popleft()
        if u == 1:
            break
        for v in allowed[u]:
            if v not in parents:
                parents[v] = u
                queue.append(v)
    # Восстанавливаем путь из src в 1
    path = []
    cur = 1
    while cur is not None:
        path.append(cur)
        cur = parents[cur]
    path.reverse()  # теперь [src, ..., 1]
    # Перемещаем диск вдоль пути
    for i in range(len(path) - 1):
        cur, nxt = path[i], path[i+1]
        free_top(nxt, d, exclude={cur})
        move_top_disk(cur, nxt)

# === Печать начального состояния ===
print("Начальное состояние башен:")
for peg in range(1, 9):
    print(f" Башня {peg}: {towers[peg]}")
print("-" * 40)

# === Основной алгоритм ===
# Сортируем все диски по возрастанию (мелкие сначала)
all_disks = sorted(d for stack in towers.values() for d in stack)
for disk in all_disks:
    # Находим башню, где сейчас лежит диск
    cur_peg = next(peg for peg, stack in towers.items() if disk in stack)
    # Если диск не на вершине, освобождаем его
    if towers[cur_peg][-1] != disk:
        free_top(cur_peg, disk)
    # Переносим диск на башню 1
    move_to_target(disk)

# === Печать итогового состояния ===
print("-" * 40)
print("Финальное состояние башен:")
for peg in range(1, 9):
    print(f" Башня {peg}: {towers[peg]}")
print(f"\nВсего шагов: {move_count}")