import copy
import random
import sys
import time

characters = [
    {"name": "Brian",
     "strength": 13,
     "finesse": 10,
     "intelligence": 10,

     "physical": 46,
     "magic": 25,

     "chest": None,
    },
    {"name": "The Red Prince",
     "strength": 12,
     "finesse": 10,
     "intelligence": 10,

     "physical": 24,
     "magic": 6,

     "chest": None,
    },
    {"name": "Lohse",
     "strength": 10,
     "finesse": 10,
     "intelligence": 14,

     "physical": 1,
     "magic": 10,

     "necklace": None,
    },
    {"name": "Fane",
     "strength": 10,
     "finesse": 10,
     "intelligence": 14,

     "physical": 2,
     "magic": 9,

     "ring1": None,
    },
]

available_gear = [
    {"type": "helmet",
     "avail": [
        {"name": "M",
         "physical": 3,
         "magic": 12,
         "intelligence": 11,
        },
        {"name": "HoP",
         "physical": 10,
         "magic": 3,
         "strength": 11,
        },
        {"name": "SH",
         "physical": 4,
         "magic": 1,
        },
        {"name": "LH",
         "physical": 3,
         "magic": 2,
        },
     ]
    },
    {"type": "chest",
     "avail": [
        {"name": "MagM",
         "physical": 3,
         "magic": 18,
         "intelligence": 11,
        },
        {"name": "MenM",
         "physical": 4,
         "magic": 16,
         "intelligence": 11,
        },
        {"name": "SSA",
         "physical": 12,
         "magic": 3,
        },
        {"name": "SA",
         "physical": 8,
         "magic": 6,
        },
     ]
    },
    {"type": "belt",
     "avail": [
        {"name": "B",
         "physical": 6,
         "magic": 0,
        },
        {"name": "B",
         "physical": 6,
         "magic": 0,
        },
        {"name": "B",
         "physical": 6,
         "magic": 0,
        },
     ]
    },
    {"type": "pants",
     "avail": [
        {"name": "SSL",
         "physical": 10,
         "magic": 2,
         "strength": 11,
        },
        {"name": "WL",
         "physical": 3,
         "magic": 9,
        },
        {"name": "RSP",
         "physical": 8,
         "magic": 2,
        },
        {"name": "WP",
         "physical": 1,
         "magic": 5,
        },
     ]
    },
    {"type": "boots",
     "avail": [
        {"name": "MSandal",
         "physical": 3,
         "magic": 9,
         "intelligence": 11,
        },
        {"name": "MShoe",
         "physical": 1,
         "magic": 6,
        },
        {"name": "BSB",
         "physical": 4,
         "magic": 1,
        },
        {"name": "RB",
         "physical": 4,
         "magic": 0,
        },
     ]
    },
    {"type": "ring",
     "avail": [
        {"name": "AR",
         "physical": 0,
         "magic": 8,
        },
        {"name": "DLR",
         "physical": 0,
         "magic": 6,
        },
        {"name": "DLR",
         "physical": 0,
         "magic": 6,
        },
        {"name": "JR",
         "physical": 0,
         "magic": 5,
        },
     ]
    },
    {"type": "necklace",
     "avail": [
        {"name": "SA",
         "physical": 0,
         "magic": 11,
        },
        {"name": "SP",
         "physical": 0,
         "magic": 9,
        },
        {"name": "PA",
         "physical": 0,
         "magic": 8,
        },
     ]
    },
]

required_attrs = set(["strength", "intelligence", "finesse"])

best_solutions = []
max_best_solutions = 40
total_permutations = 0
debug_depth = 0

start_time = time.time()

def main():
    global debug_depth
    global characters
    global available_gear
    global required_attrs
    global best_solutions

    argv_copy = sys.argv[1:]

    while len(argv_copy):
        if argv_copy[0] == '-d':
            if len(argv_copy) == 1:
                raise KeyError("missing debug depth") 
            debug_depth = int(argv_copy[1])
            argv_copy = argv_copy[2:]
            continue

        raise KeyError(f"invalid argument {argv_copy[0]}") 

    for character in characters:
        for key in required_attrs:
            if not key in character:
                name = character["name"]
                raise KeyError(f"{name} missing {key}") 

    for type_group in available_gear:
        type_group["combinations"] = []
        type_name = type_group["type"]
        print(f"Building combinations for {type_name}")
        build_all_combinations(type_group, type_name, 0, characters, {})
        count = len(type_group["combinations"])
        print(f"Number of combinations for {type_name}: {count}")
        combinations = type_group["combinations"]
        for i in range(0, len(combinations)):
            print(f"#{i}: {combinations[i]}")
        print("\n")

    apply_all_combinations(0, characters, 0)

    sort_best_solutions_min_variance_first()

    for i in range(0, min(len(best_solutions), 8)):
        print(f"\nOPTION {i+1}:\n")
        solution = best_solutions[i]
        for character in solution:
            print(character["name"])
            print(character["physical"])
            print(character["magic"])
            for key in character:
                if key in set(["name", "physical", "magic", "variance_sum_of_squares"]) or key in required_attrs:
                    continue
                item_type = key
                item = character[key]
                if item == None:
                    continue
                item_name = item["name"]
                physical = item["physical"]
                magic = item["magic"]
                print(f"{item_type}: {item_name}, {physical}, {magic}")
            print("\n")

def build_all_combinations(type_group, type_name, assign_item_i, characters, partial_assignment):
    global required_attrs

    avail = type_group["avail"]
    assert assign_item_i < len(avail)
    assign_item = avail[assign_item_i]

    any_assigned = False
    for character in characters:
        if type_name in character or (type_name == "ring" and ("ring1" in character and "ring2" in character)):
            continue
        item_char_possible_assignment = True
        for attr in required_attrs:
            if attr in assign_item:
                if character[attr] < assign_item[attr]:
                    item_char_possible_assignment = False
                    break
        if not item_char_possible_assignment:
            continue

        if type_name != "ring":
            assigned_key = type_name
        else:
            if "ring1" in character:
                assigned_key = "ring2"
            else:
                assigned_key = "ring1"

        character[assigned_key] = assign_item
        any_assigned = True

        new_assignments = copy.copy(partial_assignment)
        character_name = character["name"]
        new_assignments[f"{character_name} : {assigned_key}"] = assign_item
        if any_assignable_gear(type_name, avail, assign_item_i + 1, characters):
            # That's a partial combination
            build_all_combinations(type_group, type_name, assign_item_i + 1, characters, new_assignments)
        else:
            type_group["combinations"].append(new_assignments)

        del character[assigned_key]

    if assign_item_i < len(avail) - 1 and not any_assigned:
        build_all_combinations(type_group, type_name, assign_item_i + 1, characters, new_assignments)

def any_assignable_gear(type_name, avail, min_item_i, characters):
    global required_attrs

    while min_item_i < len(avail):
        assign_item = avail[min_item_i]

        for character in characters:
            if type_name in character or (type_name == "ring" and ("ring1" in character and "ring2" in character)):
                continue
            item_char_possible_assignment = True
            for attr in required_attrs:
                if attr in assign_item:
                    if character[attr] < assign_item[attr]:
                        item_char_possible_assignment = False
                        break
            if item_char_possible_assignment:
                return True

        min_item_i += 1
    return False

def apply_all_combinations(type_group_i, characters, depth):
    global available_gear
    global total_permutations

    combinations = available_gear[type_group_i]["combinations"]

    for combination in combinations:
        for assignment in combination:
            assigned_item = combination[assignment]
            separator_i = assignment.find(" : ")
            assert separator_i > 0 and separator_i < len(assignment) - 3
            character_name = assignment[:separator_i]
            assigned_key = assignment[separator_i + 3:]
            found = False
            for character in characters:
                if character["name"] == character_name:
                    if assigned_key in character:
                        item_name = character[assigned_key]["name"]
                        raise KeyError(f"{character_name} already has {assigned_key}: {item_name}")
                    character[assigned_key] = assigned_item
                    character["physical"] += assigned_item["physical"]
                    character["magic"] += assigned_item["magic"]
                    found = True
            assert found

        total_permutations += 1
        if depth <= debug_depth:
            elapsed_time = time.time() - start_time
            print(f"d={depth} n={total_permutations}  t={elapsed_time:.8f} applying combination {combination}")

        if type_group_i < len(available_gear) - 1:
            apply_all_combinations(type_group_i + 1, characters, depth + 1)
        else:
            evaluate(characters)

        for assignment in combination:
            assigned_item = combination[assignment]
            separator_i = assignment.find(" : ")
            assert separator_i > 0 and separator_i < len(assignment) - 3
            character_name = assignment[:separator_i]
            assigned_key = assignment[separator_i + 3:]
            found = False
            for character in characters:
                if character["name"] == character_name:
                    del character[assigned_key]
                    character["physical"] -= assigned_item["physical"]
                    character["magic"] -= assigned_item["magic"]
                    found = True
            assert found

def evaluate(characters):
    global start_time
    global best_solutions

    new_min = calculate_min(characters)
    new_average = calculate_average(characters)

    if len(best_solutions) == 0:
        best_solutions = [copy.deepcopy(characters)]
        print(f"min: {new_min}, average: {new_average}")
        print(f"{best_solutions}")
        return

    existing_min = calculate_min(best_solutions[0])
    existing_average = calculate_average(best_solutions[0])
    elapsed_time = time.time() - start_time

    if new_min > existing_min or (new_min == existing_min and new_average > existing_average):
        limit_best_solutions()
        best_solutions.insert(0, copy.deepcopy(characters))
        print(f"min: {new_min}, average: {new_average}, t={elapsed_time:.8f}")
        print(f"{best_solutions}")
        return
    if new_min == existing_min and new_average == existing_average:
        limit_best_solutions()
        best_solutions.insert(0, copy.deepcopy(characters))
        return

def calculate_min(characters):
    result = characters[0]["physical"]
    for character in characters:
        if result > character["physical"]:
            result = character["physical"]
        if result > character["magic"]:
            result = character["magic"]
    return result

def calculate_average(characters):
    result = 0
    for character in characters:
        result += character["physical"]
        result += character["magic"]
    return result / (len(characters) * 2)

def calculate_min_physical(characters):
    result = characters[0]["physical"]
    for character in characters:
        if result > character["physical"]:
            result = character["physical"]
    return result

def calculate_min_magic(characters):
    result = characters[0]["magic"]
    for character in characters:
        if result > character["magic"]:
            result = character["magic"]
    return result

def limit_best_solutions():
    global best_solutions
    global max_best_solutions

    if len(best_solutions) == max_best_solutions:
        i = random.randint(1, max_best_solutions - 1)

        # Remove a random one
        best_solutions.pop(i)

        # Also remove the oldest (worst) one
        best_solutions.pop()

def sort_best_solutions_min_variance_first():
    global best_solutions

    for solution in best_solutions:
        min_physical = calculate_min_physical(solution)
        min_magic = calculate_min_magic(solution)
        min_average = (min_physical + min_magic) / 2
        physical_sum_of_squares = 0
        magic_sum_of_squares = 0
        p_m_diff_sum_of_squares = 0
        for character in solution:
            physical_boost = character["physical"] - min_average
            physical_sum_of_squares += abs(physical_boost * physical_boost)
            magic_boost = character["magic"] - min_average
            magic_sum_of_squares += abs(magic_boost * magic_boost)
            p_m_diff = physical_boost - magic_boost
            p_m_diff_sum_of_squares += abs(p_m_diff * p_m_diff)
        solution[0]["variance_sum_of_squares"] = (physical_sum_of_squares + magic_sum_of_squares
                                                  + p_m_diff_sum_of_squares)

    best_solutions.sort(key=lambda s: s[0]["variance_sum_of_squares"])

main()