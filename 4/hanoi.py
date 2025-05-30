def hanoi_preserve(n, src, dst, aux, moves):
    """
    Стандартный перенос n дисков с src на dst через aux,
    соблюдая правило «больший на меньший».
    moves — список кортежей (откуда, куда).
    """
    if n == 0:
        return
    hanoi_preserve(n - 1, src, aux, dst, moves)
    moves.append((src, dst))
    hanoi_preserve(n - 1, aux, dst, src, moves)

def invert_tower(n, src, aux1, aux2):
    """
    Инвертирует башню из n дисков на штифте src,
    используя aux1 и aux2. Правило: можно ставить
    только больший диск на меньший.
    Возвращает список moves: [(откуда, куда), ...].
    """
    moves = []

    # вспомогательная функция для стандартного переноса
    def preserve(k, a, b, c):
        hanoi_preserve(k, a, b, c, moves)

    def invert(k, a, b, c):
        if k == 0:
            return
        # 1) снять k−1 дисков с a → c
        preserve(k - 1, a, c, b)
        # 2) большой диск k: a → b
        moves.append((a, b))
        # 3) вернуть k−1 дисков c → a
        preserve(k - 1, c, a, b)
        # 4) диск k: b → a (станет наверху)
        moves.append((b, a))
        # 5) инвертировать оставшиеся k−1 на a
        invert(k - 1, a, b, c)

    invert(n, src, aux1, aux2)
    return moves

def simulate(n, moves, pegs):
    """
    Смоделировать переносы moves на pegs: dict штифт→список.
    Возвращает финальное состояние pegs.
    """
    for frm, to in moves:
        disk = pegs[frm].pop()
        pegs[to].append(disk)
    return pegs

if __name__ == "__main__":
    n = 4
    # генерируем список ходов для инверсии
    moves = invert_tower(n, 'A', 'B', 'C')

    # инициализируем башню: на A — диски n…1 (n внизу, 1 наверху)
    pegs = {
        'A': list(range(n, 0, -1)),
        'B': [],
        'C': []
    }

    # выводим начальное состояние
    print("Первоначальное состояние башни:")
    for peg in ('A', 'B', 'C'):
        print(f"  {peg}: {pegs[peg]}")

    # (по желанию) печать всех ходов:
    # for i, (frm, to) in enumerate(moves, 1):
    #     print(f"Ход {i:2d}: {frm} → {to}")

    # выполняем переносы
    final_pegs = simulate(n, moves, pegs)

    # выводим конечное состояние
    print("\nКонечное состояние башни (инверсия выполнена):")
    for peg in ('A', 'B', 'C'):
        print(f"  {peg}: {final_pegs[peg]}")