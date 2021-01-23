import argparse
import typing as tp

CONFORMITY_TABLE = {" ": -1, "☒": 0, "☺": 1, "☼": 2, ".": 3}
CONFORMITY_TABLE_REVERSE = {-1: " ", 0: "☒", 1: "☺", 2: "☼", 3: "."}


def read_map(filename: str):
    """ Прочитать карту из указанного файла """
    game_map: tp.List[tp.List[int]] = []
    start_pos = (0, 0)
    with open(filename) as f:
        for line, i in enumerate(map(lambda s: s.strip("\n"), f.readlines())):
            game_map.append([])
            for col, j in enumerate(i):
                game_map[-1].append(CONFORMITY_TABLE[j])
                if CONFORMITY_TABLE[j] == 1:
                    start_pos = (line, col)
    return game_map, start_pos


def restore(
    game_map: tp.List[tp.List[int]],
    map_to_relax: tp.Dict[tp.Tuple[int, int], tp.Tuple[int, int]],
    start_pos: tp.Tuple[int, int],
    end_pos: tp.Tuple[int, int],
):
    curr_pos = map_to_restore[end_pos]
    while curr_pos != start_pos:
        game_map[curr_pos[0]][curr_pos[1]] = 1
        curr_pos = map_to_restore[curr_pos]
    return game_map


def solve(game_map: tp.List[tp.List[int]], start_pos: tp.Tuple[int, int]):
    que = [start_pos]
    map_to_restore = {start_pos: start_pos}
    while que:
        curr_pos = que.pop(0)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 and j != 0:
                    continue
                if curr_pos[0] - i < 0 or curr_pos[1] - j < 0:
                    continue
                try:
                    k, m = curr_pos[0] - i, curr_pos[1] - j
                    if game_map[k][m] == 3:
                        
                    if game_map[k][m] == 2:
                       
                        return game_map, map_to_restore, start_pos, (k, m)
                except IndexError:
                    pass
    return game_map, map_to_restore, start_pos, (0, 0)

map_to_relax
def main():
    parser = argparse.ArgumentParser(description="For exam-winter")
    parser.add_argument("filename", help="Path to file", type=str)
    args = parser.parse_args()
    game_map, map_to_restore, start_pos, end_pos = solve(*read_map(args.filename))
    game_map = restore(game_map, map_to_restore, start_pos, end_pos)
    
    for i in game_map:
        print("".join(map(lambda x: CONFORMITY_TABLE_REVERSE[x], i)))


if __name__ == "__main__":
    main()
