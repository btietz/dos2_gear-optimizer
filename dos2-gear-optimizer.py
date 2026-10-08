import copy
import random
import sys
import time

characters = [
    {"name": "Brian",
     "strength": 17,
     "finesse": 10,
     "intelligence": 10,

     "physical": 68,
     "magic": 48,
     "hp": 189,

     "gloves": None,
     "belt": None,
     "ring1": None,
    },
    {"name": "The Red Prince",
     "strength": 12,
     "finesse": 10,
     "intelligence": 10,

     "physical": 47,
     "magic": 27,
     "hp": 169,

     "belt": None,
    },
    {"name": "Lohse",
     "strength": 11,
     "finesse": 10,
     "intelligence": 14,

     "physical": 8,
     "magic": 42,
     "hp": 160,

     "chest": None,
     "necklace": None,
    },
    {"name": "Fane",
     "strength": 10,
     "finesse": 10,
     "intelligence": 14,

     "physical": 0,
     "magic": 2,
     "hp": 160,

     "ring1": None,
    },
]

available_gear = [
    {"type": "helmet",
     "avail": [
        {"name": "CH",
         "physical": 15,
         "magic": 3,
         "hp": 0,
         "strength": 11,
        },
        {"name": "HoP",
         "physical": 10,
         "magic": 3,
         "hp": 0,
         "strength": 11,
        },
        {"name": "M",
         "physical": 3,
         "magic": 12,
         "hp": 0,
         "intelligence": 11,
        },
        {"name": "SH",
         "physical": 4,
         "magic": 1,
         "hp": 0,
        },
        {"name": "LH",
         "physical": 3,
         "magic": 2,
         "hp": 0,
        },
     ]
    },
    {"type": "chest",
     "avail": [
        {"name": "MagM",
         "physical": 3,
         "magic": 18,
         "hp": 0,
         "intelligence": 11,
        },
        {"name": "MenM",
         "physical": 4,
         "magic": 16,
         "hp": 0,
         "intelligence": 11,
        },
        {"name": "LSA",
         "physical": 16,
         "magic": 4,
         "hp": 0,
         "strength": 11,
        },
        {"name": "MB",
         "physical": 15,
         "magic": 3,
         "hp": 0,
         "strength": 11,
        },
     ]
    },
    {"type": "gloves",
     "avail": [
        {"name": "SF",
         "physical": 3,
         "magic": 15,
         "hp": 0,
         "intelligence": 11,
        },
        {"name": "WM",
         "physical": 2,
         "magic": 10,
         "hp": 0,
         "intelligence": 11,
        },
        {"name": "SSG",
         "physical": 8,
         "magic": 2,
         "hp": 0,
         "strength": 11,
        },
        {"name": "SG",
         "physical": 13,
         "magic": 2,
         "hp": 0,
         "strength": 11,
        },
        {"name": "WM",
         "physical": 2,
         "magic": 7,
         "hp": 0,
        },
     ]
    },
    {"type": "belt",
     "avail": [
        {"name": "SB",
         "physical": 12,
         "magic": 0,
         "hp": 20,
        },
        {"name": "SS",
         "physical": 18,
         "magic": 0,
         "hp": 32,
        },
     ]
    },
    {"type": "pants",
     "avail": [
        {"name": "HSP",
         "physical": 23,
         "magic": 5,
         "hp": 0,
         "strength": 12,
        },
        {"name": "LHM",
         "physical": 16,
         "magic": 5,
         "hp": 0,
         "strength": 11,
        },
        {"name": "SSL",
         "physical": 10,
         "magic": 2,
         "hp": 0,
         "strength": 11,
        },
        {"name": "WL",
         "physical": 3,
         "magic": 9,
         "hp": 0,
        },
        {"name": "RSP",
         "physical": 8,
         "magic": 2,
         "hp": 0,
        },
     ]
    },
    {"type": "boots",
     "avail": [
        {"name": "SS",
         "physical": 15,
         "magic": 3,
         "hp": 0,
         "strength": 11,
        },
        {"name": "MS1",
         "physical": 3,
         "magic": 12,
         "hp": 10,
         "intelligence": 11,
        },
        {"name": "MS2",
         "physical": 3,
         "magic": 9,
         "hp": 0,
         "intelligence": 11,
        },
        {"name": "MS3",
         "physical": 1,
         "magic": 6,
         "hp": 0,
        },
        {"name": "BSB",
         "physical": 4,
         "magic": 1,
         "hp": 0,
        },
     ]
    },
    {"type": "necklace",
     "avail": [
        {"name": "PN",
         "physical": 0,
         "magic": 14,
         "hp": 0,
        },
        {"name": "AD",
         "physical": 0,
         "magic": 12,
         "hp": 10,
        },
        {"name": "AV",
         "physical": 0,
         "magic": 11,
         "hp": 0,
        },
     ]
    },
    {"type": "ring",
     "avail": [
        {"name": "KP",
         "physical": 0,
         "magic": 14,
         "hp": 28,
        },
        {"name": "SM",
         "physical": 0,
         "magic": 14,
         "hp": 0,
        },
        {"name": "ASR",
         "physical": 0,
         "magic": 8,
         "hp": 0,
        },
        {"name": "ASR",
         "physical": 0,
         "magic": 8,
         "hp": 0,
        },
        {"name": "LR",
         "physical": 0,
         "magic": 6,
         "hp": 15,
        },
        {"name": "DR",
         "physical": 0,
         "magic": 6,
         "hp": 0,
        },
     ]
    },
]

required_attrs = set(["strength", "intelligence", "finesse"])

best_hp_solutions = [
    # {
    #     "characters": copy.deepcopy(characters),
    #     "available_gear": copy.deepcopy(available_gear),
    #     "min_hp": calculate_min_hp(characters),
    # }
]
best_hp_solutions_tolerance = 0.85
best_armor_solutions = [
    # characters array
]
max_best_solutions = 40
total_permutations = 0
assignment_key_splits = {}
debug_depth = 0

start_time = time.time()

def main():
    global debug_depth
    global characters
    global available_gear
    global required_attrs
    global best_hp_solutions
    global best_armor_solutions

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
        required_properties = copy.copy(required_attrs)
        required_properties.add("name")
        required_properties.add("physical")
        required_properties.add("magic")
        required_properties.add("hp")
        for key in required_properties:
            if not key in character:
                name = character["name"]
                raise KeyError(f"{name} missing {key}") 

    required_properties = ["name", "physical", "magic", "hp"]
    for type_group in available_gear:
        type_name = type_group["type"]
        avail = type_group["avail"]
        for item in avail:
            item_name = item["name"]
            for key in required_properties:
                if not key in item:
                    raise KeyError(f"{type_name}: {item_name} missing {key}") 

    print("\nEvaluating HP solutions\n")
    best_hp_solutions = [
        {
            "characters": copy.deepcopy(characters),
            "available_gear": copy.deepcopy(available_gear),
            "min_hp": calculate_min_hp(characters),
        }
    ]
    hp_solution_sigs = set()
    build_all_hp_solutions(characters, available_gear, hp_solution_sigs, 0)

    for hp_i in range(0, len(best_hp_solutions)):
        print(f"\nEvaluating armor for HP solution {hp_i+1}/{len(best_hp_solutions)}\n")
        hp_solution = best_hp_solutions[hp_i]
        available_gear = hp_solution["available_gear"]
        characters = hp_solution["characters"]
        for type_group in available_gear:
            type_name = type_group["type"]
            type_group["combinations"] = []
            print(f"Building armor combinations for {type_name}")
            build_all_armor_combinations(type_group, type_name, 0, characters, {})
            count = len(type_group["combinations"])
            print(f"Number of armor combinations for {type_name}: {count}")
            combinations = type_group["combinations"]
            strip_duplicate_combinations(combinations)
            for i in range(0, len(combinations)):
                print(f"#{i+1}: {combinations[i]}")
            print("\n")

        apply_all_armor_combinations(0, characters, 0)

    sort_best_solutions_min_variance_first()

    for i in range(0, min(len(best_armor_solutions), 8)):
        print(f"\nOPTION {i+1}:\n")
        solution = best_armor_solutions[i]
        for character in solution:
            print(character["name"])
            physical = character["physical"]
            print(f"physical: {physical}")
            magic = character["magic"]
            print(f"magic: {magic}")
            hp = character["hp"]
            print(f"hp: {hp}")
            for key in character:
                if key in set(["name", "physical", "magic", "hp", "variance_sum_of_squares"]) or key in required_attrs:
                    continue
                item_type = key
                item = character[key]
                if item == None:
                    continue
                item_name = item["name"]
                physical = item["physical"]
                magic = item["magic"]
                hp = item["hp"]
                print(f"{item_type}: {item_name}, {physical}, {magic}, {hp}")
            print("\n")

def build_all_hp_solutions(characters, available_gear, hp_solution_sigs, depth):
    global required_attrs
    global total_permutations

    for type_group_i in range(0, len(available_gear)):
        type_group = available_gear[type_group_i]
        type_name = type_group["type"]
        avail = type_group["avail"]
        for avail_i in range(0, len(avail)):
            assign_item = avail[avail_i]
            if assign_item["hp"] == 0:
                # This item does not contribute to HP, so skip it
                continue

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
                character["hp"] += assign_item["hp"]
                avail.pop(avail_i)
                if len(avail) == 0:
                    available_gear.pop(type_group_i)

                sig = characters_sig(characters)
                if not sig in hp_solution_sigs:
                    total_permutations += 1
                    hp_solution_sigs.add(sig)

                    if depth <= debug_depth:
                        elapsed_time = time.time() - start_time
                        item_name = assign_item["name"]
                        character_name = character["name"]
                        print(f"HP: d={depth} t={elapsed_time:.8f} n={total_permutations} applying {type_name}: "
                              f"{item_name} to {character_name}")

                    evaluate_for_hp(characters, available_gear)
                    build_all_hp_solutions(characters, available_gear, hp_solution_sigs, depth + 1)

                if len(avail) == 0:
                    available_gear.insert(type_group_i, type_group)
                avail.insert(avail_i, assign_item)
                character["hp"] -= assign_item["hp"]
                del character[assigned_key]

def characters_sig(characters):
    global required_attrs

    sig = ""
    for character in characters:
        for key in character:
            if key in set(["name", "physical", "magic", "hp"]) or key in required_attrs:
                continue
            item = character[key]
            if item == None:
                continue
            item_name = item["name"]
            if sig != "":
                sig += ", "
            sig += f"{key}:{item_name}"
    assert sig != ""
    return sig

def evaluate_for_hp(characters, available_gear):
    global start_time
    global best_hp_solutions
    global best_hp_solutions_tolerance

    existing_best_min = best_hp_solutions[0]["min_hp"]
    new_min = calculate_min_hp(characters)

    if new_min > existing_best_min * best_hp_solutions_tolerance:
        best_hp_solutions.append(
            {
                "characters": copy.deepcopy(characters),
                "available_gear": copy.deepcopy(available_gear),
                "min_hp": calculate_min_hp(characters),
            }
        )
        sort_and_limit_best_hp_solutions()
        if new_min > existing_best_min:
            elapsed_time = time.time() - start_time
            print(f"min: {new_min} t={elapsed_time:.8f}, count={len(best_hp_solutions)}")
            print(f"{best_hp_solutions}")
        return

def calculate_min_hp(characters):
    result = characters[0]["hp"]
    for character in characters:
        if result > character["hp"]:
            result = character["hp"]
    return result

def sort_and_limit_best_hp_solutions():
    global best_hp_solutions
    global debug_depth

    best_hp_solutions.sort(key=lambda s: s["min_hp"])

    existing_best_min = best_hp_solutions[-1]["min_hp"]

    while best_hp_solutions[0]["min_hp"] < existing_best_min * best_hp_solutions_tolerance:
        best_hp_solutions.pop(0)

    cut_range_low_i = 0
    cut_range_high_i = len(best_hp_solutions) - 1
    while len(best_hp_solutions) > max_best_solutions:
        cut_range_mid_i = int((cut_range_low_i + cut_range_high_i) / 2)
        if cut_range_mid_i == cut_range_low_i or cut_range_mid_i == cut_range_high_i:
            best_hp_solutions.pop(cut_range_mid_i)
            continue

        low_hp = best_hp_solutions[cut_range_low_i]["min_hp"]
        mid_hp = best_hp_solutions[cut_range_mid_i]["min_hp"]
        high_hp = best_hp_solutions[cut_range_high_i]["min_hp"]
        low_mid_delta = mid_hp - low_hp
        mid_high_delta = high_hp - mid_hp
        if low_mid_delta > mid_high_delta:
            cut_range_high_i = cut_range_mid_i
        elif low_mid_delta < mid_high_delta:
            cut_range_low_i = cut_range_mid_i
        else:
            # The halves are balanced, so randomly cut from the low or high side
            if random.randint(0, 1) == 0:
                cut_range_low_i = cut_range_mid_i
            else:
                cut_range_high_i = cut_range_mid_i

    if debug_depth > 0:
        value = best_hp_solutions[0]["min_hp"]
        values = f"{value}"
        for i in range(1, len(best_hp_solutions)):
            value = best_hp_solutions[i]["min_hp"]
            values += f", {value}"
        elapsed_time = time.time() - start_time
        print(f"best_hp_solutions: count={len(best_hp_solutions)}, t={elapsed_time:.8f}: [{values}]")

def build_all_armor_combinations(type_group, type_name, assign_item_i, characters, partial_assignment):
    global required_attrs
    global assignment_key_splits

    avail = type_group["avail"]
    assert assign_item_i < len(avail)
    assign_item = avail[assign_item_i]

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

        new_assignments = copy.copy(partial_assignment)
        character_name = character["name"]
        assignment_key = f"{character_name} : {assigned_key}"
        new_assignments[assignment_key] = assign_item
        assignment_key_splits[assignment_key] = [character_name, assigned_key]
        if any_assignable_gear(type_name, avail, assign_item_i + 1, characters):
            # That's a partial combination
            build_all_armor_combinations(type_group, type_name, assign_item_i + 1, characters, new_assignments)
        else:
            type_group["combinations"].append(new_assignments)

        del character[assigned_key]

    if assign_item_i < len(avail) - 1:
        build_all_armor_combinations(type_group, type_name, assign_item_i + 1, characters,
                                     copy.copy(partial_assignment))

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

def strip_duplicate_combinations(combinations):
    combination_sigs = set()
    i = 0
    while i < len(combinations):
        sig = combination_sig(combinations[i])
        if sig in combination_sigs:
            print(f"REMOVED: {i}: {sig}")
            combinations.pop(i)
            continue
        combination_sigs.add(sig)
        i += 1

def combination_sig(combination):
    global assignment_key_splits

    sig = ""
    for character in characters:
        character_name = character["name"]
        for assignment in combination:
            assignment_split = assignment_key_splits[assignment]
            assigned_character_name = assignment_split[0]
            if character_name == assigned_character_name:
                assigned_item_name = combination[assignment]["name"]
                if sig != "":
                    sig += ", "
                sig += f"{character_name}: {assigned_item_name}"
    return sig

def apply_all_armor_combinations(type_group_i, characters, depth):
    global available_gear
    global assignment_key_splits
    global total_permutations

    combinations = available_gear[type_group_i]["combinations"]

    for c_i in range(0, len(combinations)):
        combination = combinations[c_i]
        for assignment in combination:
            assigned_item = combination[assignment]
            assignment_split = assignment_key_splits[assignment]
            character_name = assignment_split[0]
            assigned_key = assignment_split[1]
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
            print(f"A: d={depth} c={c_i+1}/{len(combinations)} t={elapsed_time:.8f} n={total_permutations} applying "
                  f"combination {combination}")

        if type_group_i < len(available_gear) - 1 and not is_dead_branch(type_group_i + 1, characters):
            apply_all_armor_combinations(type_group_i + 1, characters, depth + 1)
        else:
            evaluate_for_armor(characters)

        for assignment in combination:
            assigned_item = combination[assignment]
            assignment_split = assignment_key_splits[assignment]
            character_name = assignment_split[0]
            assigned_key = assignment_split[1]
            found = False
            for character in characters:
                if character["name"] == character_name:
                    del character[assigned_key]
                    character["physical"] -= assigned_item["physical"]
                    character["magic"] -= assigned_item["magic"]
                    found = True
            assert found

def is_dead_branch(min_type_group_i, characters):
    global best_armor_solutions
    global assignment_key_splits

    if len(best_armor_solutions) == 0:
        return False

    best_min = calculate_min_armor(best_armor_solutions[0])

    for character in characters:
        character_name = character["name"]
        max_character_physical = character["physical"]
        max_character_magic = character["magic"]
        type_group_i = min_type_group_i
        while type_group_i < len(available_gear):
            type_group = available_gear[type_group_i]
            combinations = type_group["combinations"]
            best_type_physical = 0
            best_type_magic = 0
            for combination in combinations:
                for assignment in combination:
                    assignment_split = assignment_key_splits[assignment]
                    if assignment_split[0] == character_name:
                        assigned_item = combination[assignment]
                        if best_type_physical < assigned_item["physical"]:
                            best_type_physical = assigned_item["physical"]
                        if best_type_magic < assigned_item["magic"]:
                            best_type_magic = assigned_item["magic"]
            max_character_physical += best_type_physical
            max_character_magic += best_type_magic
            type_group_i += 1

        if max_character_physical < best_min:
            return True
        if max_character_magic < best_min:
            return True

    return False

def evaluate_for_armor(characters):
    global start_time
    global best_armor_solutions

    new_min = calculate_min_armor(characters)
    new_average = calculate_average_armor(characters)

    if len(best_armor_solutions) == 0:
        best_armor_solutions = [copy.deepcopy(characters)]
        print(f"min: {new_min}, average: {new_average}")
        print(f"{best_armor_solutions}")
        return

    existing_min = calculate_min_armor(best_armor_solutions[0])
    existing_average = calculate_average_armor(best_armor_solutions[0])
    elapsed_time = time.time() - start_time

    if new_min > existing_min or (new_min == existing_min and new_average > existing_average):
        limit_best_armor_solutions()
        best_armor_solutions.insert(0, copy.deepcopy(characters))
        print(f"min: {new_min}, average: {new_average}, t={elapsed_time:.8f}")
        print(f"{best_armor_solutions}")
        return
    if new_min == existing_min and new_average == existing_average:
        limit_best_armor_solutions()
        best_armor_solutions.insert(0, copy.deepcopy(characters))
        return

def calculate_min_armor(characters):
    result = characters[0]["physical"]
    for character in characters:
        if result > character["physical"]:
            result = character["physical"]
        if result > character["magic"]:
            result = character["magic"]
    return result

def calculate_average_armor(characters):
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

def limit_best_armor_solutions():
    global best_armor_solutions
    global max_best_solutions

    if len(best_armor_solutions) == max_best_solutions:
        i = random.randint(1, max_best_solutions - 1)

        # Remove a random one
        best_armor_solutions.pop(i)

        # Also remove the oldest (worst) one
        best_armor_solutions.pop()

def sort_best_solutions_min_variance_first():
    global best_armor_solutions

    for solution in best_armor_solutions:
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

    best_armor_solutions.sort(key=lambda s: s[0]["variance_sum_of_squares"])

main()