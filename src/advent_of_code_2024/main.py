import re
from pathlib import Path
from pprint import pprint
from typing import Tuple, List
from collections import Counter

from loguru import logger


## DAY 1

def load_day_1(path: Path) -> Tuple[list,list]:
    with open(path, 'r') as file:
        items = file.read().splitlines()

    pairs = [x.split("   ") for x in items]
    first_list = list([int(x[0]) for x in pairs])
    second_list = list([int(x[-1]) for x in pairs])
    return first_list, second_list

def calculate_total_list_distance(path: Path) -> float:
    first_list, second_list = load_day_1(path)
    distance = sum([abs(x - y) for x, y in zip(sorted(first_list), sorted(second_list))])
    return distance

def calculate_similarity_score(path: Path) -> float:
    first_list, second_list = load_day_1(path)
    second_list_counter = Counter(second_list)
    similarities = [(value * second_list_counter.get(value)) for value in first_list if second_list_counter.get(value)]
    return sum(similarities)


## DAY 2

def load_day_2(path: Path) -> List[list]:
    with open(path, 'r') as file:
        items = file.read().splitlines()
    return list([int(y) for y in x.split(" ")] for x in items)

def is_report_safe(report: list[int], tolerate_1:bool = False) -> bool:
    report_diffs = [report[x+1] - report[x] for x in range(len(report)-1)]
    report_diffs_in_range = all([1 <= abs(report_diff) <= 3 for report_diff in report_diffs])
    report_diffs_all_same_sign = len(set([report_diff > 0 for report_diff in report_diffs]))==1
    pure_safe = all([report_diffs_in_range, report_diffs_all_same_sign])

    if pure_safe:
        return True
    elif not tolerate_1:
        return pure_safe
    else:
        for i in range(len(report)):
            report_copy = report.copy()
            del report_copy[i]
            if is_report_safe(report_copy):
                return True
        return False


def calculate_safety_of_reports(path: Path):
    reports = load_day_2(path)
    safeties = [is_report_safe(report) for report in reports]
    return safeties.count(True)

def calculate_tolerant_safety_of_reports(path: Path):
    reports = enumerate(load_day_2(path))
    safeties = {key: is_report_safe(value, True) for key, value in dict(reports).items()}
    return list(safeties.values()).count(True)


## Day 3

def read_file(path: Path):
    with open(path, 'r') as file:
        code = file.read()
    return code


def get_mul_matches(code: str):
    pattern = r'mul\(([0-9]{1,3}),([0-9]{1,3})\)'
    matches = re.findall(pattern, code)
    return sum([int(x[0]) * int(x[1]) for x in matches])

def get_enabled_code(code: str):
    items = code.split("don't()")
    good_code =  [items[0]] + list(["".join(item.split("do()")[1:]) for item in items[1:]])
    return "".join(good_code)

##Day 4

def wordsearch(input_str: str):

    def in_range(row, col, rows, cols):
        return 0 <= row < rows and 0 <= col < cols

    def get_diagonal_pairs(rows, cols):
        diagonals_square_length = rows + cols - 1
        pairs_1 = [
            [(x-y,y) for y in range(x + 1) if in_range(x-y, y, rows, cols)]
            for x in range(diagonals_square_length)
        ]
        # print(pairs_1)

        pairs_2 = [
            [(x-y,cols-y-1) for y in range(x + 1) if in_range(x-y, cols-y-1, rows, cols)]
            for x in range(diagonals_square_length)
        ]

        return pairs_1 + pairs_2

    def resolve_pairs(pair_sets: list[Tuple[int,int]], horizontals: list[str]):
        return [
            "".join([horizontals[pair[0]][pair[1]] for pair in pair_set])
            for pair_set in pair_sets
        ]

    #horizontals
    horizontals = input_str.splitlines()
    rows = len(horizontals)
    verticals = ["".join(x) for x in list(zip(*horizontals))]
    cols = len(verticals)
    pair_sets = get_diagonal_pairs(rows,cols)
    diagonals = resolve_pairs(pair_sets, horizontals)
    search_lists = horizontals + verticals + diagonals
    matches = [item.count("XMAS") + item.count("SAMX") for item in search_lists]
    return sum(matches)

def wordsearch_complex(input_str: str):
    def in_range(row, col, rows, cols):
        return 0 <= row < rows and 0 <= col < cols

    def resolve_pairs(pair_sets: list[Tuple[int,int]], horizontals: list[str]):
        return [
            "".join([horizontals[pair[0]][pair[1]] for pair in pair_set])
            for pair_set in pair_sets
        ]

    horizontals = input_str.splitlines()
    rows = len(horizontals)
    verticals = ["".join(x) for x in list(zip(*horizontals))]
    cols = len(verticals)

    diagonals_square_length = rows + cols - 1

    pairs_a = [
        [(x - y, y) for y in range(x + 1) if in_range(x - y, y, rows, cols)]
        for x in range(diagonals_square_length)
    ]

    pairs_b = [
        [(x - y, cols - y - 1) for y in range(x + 1) if in_range(x - y, cols - y - 1, rows, cols)][::-1]
        for x in range(diagonals_square_length)
    ]


    diagonals_a = resolve_pairs(pairs_a, horizontals)
    diagonals_b = resolve_pairs(pairs_b, horizontals)

    a_coords = [[pairs_a[key][m.start()+1] for m in re.finditer("MAS", value)]
                     + [pairs_a[key][m.start()+1] for m in re.finditer("SAM", value)]
                for key, value in enumerate(diagonals_a)]
    a_coords_set = {c for l in a_coords for c in l}

    b_coords = [[pairs_b[key][m.start() + 1] for m in re.finditer("MAS", value)]
                     + [pairs_b[key][m.start() + 1] for m in re.finditer("SAM", value)]
                for key, value in enumerate(diagonals_b)]
    b_coords_set = {c for l in b_coords for c in l}

    return len(b_coords_set.intersection(a_coords_set))

    # def count_string_matches(find_string: str):
    #     a_coords = {key: [pairs_a[key][m.start()+1] for m in re.finditer(find_string, value)]
    #                      + [pairs_a[key][m.start()+1] for m in re.finditer(find_string[::-1], value)]
    #
    #                 for key, value in diagonals_a.items()}
    #     print(a_coords)
    #
    #     b_coords = {key: [pairs_b[key][m.start() + 1] for m in re.finditer(find_string, value)]
    #                      + [pairs_b[key][m.start() + 1] for m in re.finditer(find_string[::-1], value)]
    #                 for key, value in diagonals_b.items()}
    #
    #     print(b_coords)
    #
    #     a_coords_set = {c for l in a_coords.values() for c in l}
    #     pprint(a_coords_set)
    #     b_coords_set = {c for l in b_coords.values() for c in l}
    #     pprint(b_coords_set)
    #
    #     return len(a_coords_set.intersection(b_coords_set))
    #
    # print(count_string_matches("MAS"))
    # matching_coords = set(a_coords.values()).intersection(set(b_coords.values()))

    # pprint(matching_coords)
    # pprint(b_coords)

    # pprint(diagonals_b)
    # print([
    #     [
    #         (match.start(), match.end())
    #         for match in re.finditer("MAS", diagonal)
    #     ]
    #     for diagonal in diagonals_a])
    #

    #
    # print(pairs_a)
    # print(pairs_b)
    #






if __name__ == "__main__":

    ## Day 1
    data_1_example_path = Path("data/2024_day_1_example.txt")
    data_1_path = Path("data/2024_day_1.txt")

    distance_example = calculate_total_list_distance(data_1_example_path)
    print(f"distance example: {distance_example}")

    distance = calculate_total_list_distance(data_1_path)
    print(f"distance: {distance}")

    similarities_example = calculate_similarity_score(data_1_example_path)
    print(f"{similarities_example}")

    similarities_example = calculate_similarity_score(data_1_path)
    print(f"{similarities_example}")

    ##Day 2
    day_2_example_path = Path("data/2024_day_2_example.txt")
    day_2_path = Path("data/2024_day_2.txt")

    safeties_example = calculate_safety_of_reports(day_2_example_path)
    print(f"safeties examples: {safeties_example}")

    safeties = calculate_safety_of_reports(day_2_path)
    print(f"safeties: {safeties}")

    tolerant_safeties_example = calculate_tolerant_safety_of_reports(day_2_example_path)
    print(f"tolerant safeties examples: {tolerant_safeties_example}")

    tolerant_safeties = calculate_tolerant_safety_of_reports(day_2_path)
    print(f"tolerant safeties: {tolerant_safeties}")

    ##Day 3
    day_3_example = read_file(Path("data/2024_day_3_example.txt"))
    day_3_example_2 = read_file(Path("data/2024_day_3_example_2.txt"))
    day_3 = read_file(Path("data/2024_day_3.txt"))


    print(f"matches_example:{get_mul_matches(day_3_example)}")
    print(f"matches:{get_mul_matches(day_3)}")

    print(f"only working code example: {get_mul_matches(get_enabled_code(day_3_example_2))}")
    print(f"only working code: {get_mul_matches(get_enabled_code(day_3))}")


    ##Day 4
    day_4_example = read_file(Path("data/2024_day_4_example.txt"))
    day_4 = read_file(Path("data/2024_day_4.txt"))

    print(f"example wordsearch: {wordsearch(day_4_example)}")
    print(f"wordsearch: {wordsearch(day_4)}")

    print(f"complex wordsearch example: {wordsearch_complex(day_4_example)}")
    print(f"complex wordsearch: {wordsearch_complex(day_4)}")
