import copy
import random
import sys
import sortedcontainers
# pip install sortedcontainers
# -or-
# python3 -m pip install sortedcontainers
import time

characters = [
    {"name": "Brian",
     "strength": 17,
     "finesse": 11,
     "intelligence": 11,

     "physical": 48,
     "magic": 50,
     "hp": 218,

     "necklace": None,
    },
    {"name": "The Red Prince",
     "strength": 13,
     "finesse": 11,
     "intelligence": 11,

     "physical": 46,
     "magic": 32,
     "hp": 262,
    },
    {"name": "Lohse",
     "strength": 11,
     "finesse": 12,
     "intelligence": 14,

     "physical": 55,
     "magic": 118,
     "hp": 240,

     "helmet": None,
     "chest": None,
     "pants": None,
     "boots": None,
     "ring1": None,
    },
    {"name": "Fane",
     "strength": 13,
     "finesse": 11,
     "intelligence": 15,

     "physical": 20,
     "magic": 134,
     "hp": 218,

     "chest": None,
     "pants": None,
     "boots": None,
     "necklace": None,
     "ring1": None,
    },
]

available_gear = [
    {"type": "helmet",
     "avail": [
        {"name": "PH",
         "physical": 20,
         "magic": 4,
         "hp": 0,
         "strength": 12,
        },
        {"name": "MMH",
         "physical": 13,
         "magic": 9,
         "hp": 0,
         "finesse": 12,
        },
        {"name": "Sk",
         "physical": 4,
         "magic": 17,
         "hp": 0,
        },
        {"name": "CH",
         "physical": 15,
         "magic": 3,
         "hp": 0,
        },
        {"name": "M",
         "physical": 3,
         "magic": 12,
         "hp": 0,
         "characters": ["Lohse", "Fane"]   # +1 intelligence
        },
     ]
    },
    {"type": "chest",
     "avail": [
        {"name": "SA",
         "physical": 43,
         "magic": 9,
         "hp": 0,
         "strength": 12,
        },
        {"name": "AK",
         "physical": 8,
         "magic": 36,
         "hp": 0,
         "intelligence": 12,
        },
        {"name": "SSA",
         "physical": 31,
         "magic": 6,
         "hp": 0,
         "strength": 12,
        },
        {"name": "WM",
         "physical": 5,
         "magic": 27,
         "hp": 0,
        },
        {"name": "BA",
         "physical": 16,
         "magic": 11,
         "hp": 0,
        },
     ]
    },
    {"type": "gloves",
     "avail": [
        {"name": "HoP",
         "physical": 6,
         "magic": 24,
         "hp": 0,
         "intelligence": 12,
        },
        {"name": "PG",
         "physical": 20,
         "magic": 4,
         "hp": 0,
         "strength": 12,
        },
        {"name": "MCG",
         "physical": 13,
         "magic": 9,
         "hp": 0,
         "finesse": 12,
        },
        {"name": "MLSG",
         "physical": 18,
         "magic": 4,
         "hp": 0,
         "strength": 12,
        },
        {"name": "SF",
         "physical": 3,
         "magic": 15,
         "hp": 0,
        },
        {"name": "SG",
         "physical": 13,
         "magic": 2,
         "hp": 0,
        },
        {"name": "MLG",
         "physical": 8,
         "magic": 6,
         "hp": 0,
        },
     ]
    },
    {"type": "belt",
     "avail": [
        {"name": "BoV",
         "physical": 20,
         "magic": 0,
         "hp": 0,
         "characters": ["Lohse"]   # Barter
        },
        {"name": "CC",
         "physical": 18,
         "magic": 0,
         "hp": 12,
         "characters": ["Brian"]   # Telekinesis
        },
        {"name": "BoT",
         "physical": 20,
         "magic": 0,
         "hp": 15,
        },
        {"name": "SS",
         "physical": 18,
         "magic": 0,
         "hp": 37,
        },
        {"name": "SB",
         "physical": 12,
         "magic": 0,
         "hp": 20,
        },
     ]
    },
    {"type": "pants",
     "avail": [
        {"name": "ILA",
         "physical": 30,
         "magic": 7,
         "hp": 0,
         "strength": 12,
        },
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
        },
        {"name": "MPL",
         "physical": 8,
         "magic": 6,
         "hp": 10,
        },
     ]
    },
    {"type": "boots",
     "avail": [
        {"name": "SS",
         "physical": 15,
         "magic": 3,
         "hp": 0,
        },
        {"name": "MS",
         "physical": 3,
         "magic": 12,
         "hp": 10,
        },
     ]
    },
    {"type": "necklace",
     "avail": [
        {"name": "AD",
         "physical": 0,
         "magic": 12,
         "hp": 12,
        },
        {"name": "AR",
         "physical": 0,
         "magic": 14,
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
        {"name": "FiF",
         "physical": 0,
         "magic": 11,
         "hp": 23,
        },
        {"name": "DC",
         "physical": 0,
         "magic": 17,
         "hp": 0,
        },
        {"name": "MR",
         "physical": 0,
         "magic": 15,
         "hp": 0,
        },
        {"name": "SM",
         "physical": 0,
         "magic": 14,
         "hp": 0,
        },
        {"name": "RR",
         "physical": 0,
         "magic": 13,
         "hp": 0,
         "characters": ["Brian", "The Red Prince"], # for +1 warfare
        },
     ]
    },
]

required_attrs = set(["strength", "intelligence", "finesse"])

best_hp_solutions = sortedcontainers.SortedList(key=lambda s: (s["min_hp"], s["gen#"]))
# = [
#       {
#           "characters": copy.deepcopy(characters),
#           "available_gear": copy.deepcopy(available_gear),
#           "min_hp": calculate_min_hp(characters),
#           "gen#": total_permutations,
#       }
#   ]
best_hp_solutions_tolerance = 0.85
max_temp_hp_solutions = 2000
best_armor_solutions = [
    # characters array
]
max_best_solutions = 40
total_permutations = 0
total_solution_refinements = 0
cofactor_delta = 0
cofactor_start_count = 10
cofactor_threshold = 0.949
assignment_key_splits = {}
debug_depth = 0

start_time = time.time()

def main():
    global debug_depth
    global cofactor_start_count
    global cofactor_threshold
    global max_best_solutions
    global characters
    global available_gear
    global required_attrs
    global best_hp_solutions
    global best_hp_solutions_tolerance
    global best_armor_solutions

    argv_copy = sys.argv[1:]
    faster = 0
    more_thorough = 0

    while len(argv_copy):
        if argv_copy[0] == '-d':
            if len(argv_copy) == 1:
                raise KeyError("missing debug depth") 
            debug_depth = int(argv_copy[1])
            argv_copy = argv_copy[2:]
            continue

        if argv_copy[0] == '--faster' or argv_copy[0] == '-f':
            if len(argv_copy) == 1:
                raise KeyError("missing faster factor") 
            faster = int(argv_copy[1])
            argv_copy = argv_copy[2:]
            if faster > 50:
                raise ValueError("--faster is limited to 50") 
            if faster == 1:
                cofactor_start_count = 9
            elif faster >= 2:
                cofactor_start_count = 8
            max_best_solutions -= min(faster, 20)           # min: 40 - 20 = 20
            cofactor_threshold += 0.001 * faster            # max: 0.949 + 0.001 * 50 = 0.999
            continue

        if argv_copy[0] == '--more-thorough' or argv_copy[0] == '-m':
            if len(argv_copy) == 1:
                raise KeyError("missing more-thorough factor") 
            more_thorough = int(argv_copy[1])
            argv_copy = argv_copy[2:]
            if more_thorough > 100:
                raise ValueError("--more-thorough is limited to 100") 
            if more_thorough == 1:
                cofactor_start_count = 11
            elif more_thorough >= 2:
                cofactor_start_count = 12
            max_best_solutions += min(more_thorough, 60)   # max: 40 + 60 = 100
            cofactor_threshold -= 0.001 * more_thorough    # max: 0.949 - 0.001 * 100 = 0.849
            continue

        raise KeyError(f"invalid argument {argv_copy[0]}") 

    if faster != 0 and more_thorough != 0:
        raise Exception("--faster and --more-thorough are mutually exclusive")

    total_hp = 0
    max_hp = 0
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
        total_hp += character["hp"]
        if max_hp < character["hp"]:
            max_hp = character["hp"]
    average_hp = total_hp / len(characters)
    min_best_hp_solutions_tolerance = average_hp / max_hp
    if best_hp_solutions_tolerance < min_best_hp_solutions_tolerance:
        best_hp_solutions_tolerance = min_best_hp_solutions_tolerance

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
    best_hp_solutions.add({
        "characters": copy.deepcopy(characters),
        "available_gear": copy.deepcopy(available_gear),
        "min_hp": calculate_min_hp(characters),
        "gen#": total_permutations,
    })
    hp_solution_sigs = set()
    build_all_hp_solutions(characters, available_gear, hp_solution_sigs, 0)
    limit_best_hp_solutions(max_best_solutions, 1000000)

    for hp_i in range(0, len(best_hp_solutions)):
        print(f"\nEvaluating armor for HP solution {hp_i+1}/{len(best_hp_solutions)}\n")
        hp_solution = best_hp_solutions[hp_i]
        available_gear = hp_solution["available_gear"]
        available_gear.sort(key=lambda s: gear_armor_value_spread(s), reverse=True)
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
    global debug_depth

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
                character_name = character["name"]
                if "characters" in assign_item and not character_name in assign_item["characters"]:
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
                    if not "ring1" in character:
                        assigned_key = "ring1"
                    else:
                        assert not "ring2" in character
                        assigned_key = "ring2"

                character[assigned_key] = assign_item
                character["hp"] += assign_item["hp"]
                character["physical"] += assign_item["physical"]
                character["magic"] += assign_item["magic"]
                avail.pop(avail_i)
                if len(avail) == 0:
                    available_gear.pop(type_group_i)

                sig = characters_sig(characters)
                if not (sig in hp_solution_sigs or is_dead_branch_hp(characters, available_gear)):
                    total_permutations += 1
                    hp_solution_sigs.add(sig)

                    if depth <= debug_depth:
                        elapsed_time = time.time() - start_time
                        item_name = assign_item["name"]
                        print(f"HP: d={depth} t={elapsed_time:.8f} n={total_permutations} applying {type_name}: "
                              f"{item_name} to {character_name}")

                    evaluate_for_hp(characters, available_gear, depth)
                    build_all_hp_solutions(characters, available_gear, hp_solution_sigs, depth + 1)

                if len(avail) == 0:
                    available_gear.insert(type_group_i, type_group)
                avail.insert(avail_i, assign_item)
                character["hp"] -= assign_item["hp"]
                character["physical"] -= assign_item["physical"]
                character["magic"] -= assign_item["magic"]
                del character[assigned_key]

def characters_sig(characters):
    global required_attrs

    sig = ""
    for character in characters:
        character_name = character["name"]
        if sig == "":
            sig += f"{character_name}::"
        else:
            sig += f";{character_name}::"

        keys = sorted(character)
        ring1 = None

        if "ring1" in character and character["ring1"] != None:
            ring1 = character["ring1"]["name"]

        ring2 = None
        if "ring2" in character and character["ring2"] != None:
            ring2 = character["ring2"]["name"]

        if ring1 == None and ring2 != None:
            ring1 = ring2
            ring2 = None

        if ring1 != None and ring2 != None:
            if ring2 < ring1:
                temp = ring1
                ring1 = ring2
                ring2 = temp

        for key in keys:
            if key in set(["name", "physical", "magic", "hp"]) or key in required_attrs:
                continue
            item = character[key]
            if item == None:
                continue
            item_name = item["name"]

            if key == "ring1" or key == "ring2":

                if ring1 != None:
                    key = "ring1"
                    item_name = ring1
                    ring1 = None
                else:
                    assert ring2 != None
                    key = "ring2"
                    item_name = ring2
                    ring2 = None

            if sig[-2:] != "::":
                sig += ","
            sig += f"{key}:{item_name}"
    assert sig != ""
    return sig

def is_dead_branch_hp(characters, available_gear):
    global best_hp_solutions
    global max_temp_hp_solutions
    global best_hp_solutions_tolerance
    global required_attrs

    if len(best_hp_solutions) < max_temp_hp_solutions:
        # Don't start dead branch pruning until the HP solutions are adequately seeded
        return False

    required_min = calculate_min_hp(best_hp_solutions[-1]["characters"]) * best_hp_solutions_tolerance
    for character in characters:
        character_name = character["name"]
        max_character_hp = character["hp"]
        for type_group in available_gear:
            best_add_hp_for_type_group = 0
            for item in type_group["avail"]:
                if item["hp"] == 0:
                    continue
                if "characters" in item and not character_name in item["characters"]:
                    continue
                item_char_possible_assignment = True
                for attr in required_attrs:
                    if attr in item:
                        if character[attr] < item[attr]:
                            item_char_possible_assignment = False
                            break
                if item_char_possible_assignment:
                    if best_add_hp_for_type_group < item["hp"]:
                        best_add_hp_for_type_group = item["hp"]
            max_character_hp += best_add_hp_for_type_group

        if max_character_hp < required_min:
            return True

    return False

def evaluate_for_hp(characters, available_gear, depth):
    global start_time
    global best_hp_solutions
    global best_hp_solutions_tolerance
    global max_temp_hp_solutions

    existing_best_min = best_hp_solutions[-1]["min_hp"]
    new_min = calculate_min_hp(characters)

    if new_min > existing_best_min * best_hp_solutions_tolerance:
        best_hp_solutions.add({
            "characters": copy.deepcopy(characters),
            "available_gear": copy.deepcopy(available_gear),
            "min_hp": calculate_min_hp(characters),
            "gen#": total_permutations,
        })
        limit_best_hp_solutions(max_temp_hp_solutions, depth)
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

def limit_best_hp_solutions(limit, depth):
    global best_hp_solutions
    global total_permutations
    global debug_depth

    existing_best_min = best_hp_solutions[-1]["min_hp"]

    while best_hp_solutions[0]["min_hp"] < existing_best_min * best_hp_solutions_tolerance:
        best_hp_solutions.pop(0)

    while len(best_hp_solutions) > limit:
        cut_range_low_i = 0
        cut_range_high_i = len(best_hp_solutions) - 1

        while True:
            cut_range_mid_i = int((cut_range_low_i + cut_range_high_i) / 2)
            if cut_range_mid_i == cut_range_low_i or cut_range_mid_i == cut_range_high_i:
                best_hp_solutions.pop(cut_range_mid_i)
                break

            low_hp = best_hp_solutions[cut_range_low_i]["min_hp"]
            mid_hp = best_hp_solutions[cut_range_mid_i]["min_hp"]
            high_hp = best_hp_solutions[cut_range_high_i]["min_hp"]
            low_mid_delta = mid_hp - low_hp
            mid_high_delta = high_hp - mid_hp
            if low_mid_delta < mid_high_delta:
                cut_range_high_i = cut_range_mid_i
            elif low_mid_delta > mid_high_delta:
                cut_range_low_i = cut_range_mid_i
            else:
                # The halves are balanced, so randomly cut from the low or high side.  The 1:2 ratio corrects for recency
                # bias, for a better sampling of seed HP solutions to feed into the armor values leveling.
                if random.randint(0, 2) != 0:
                    cut_range_low_i = cut_range_mid_i
                else:
                    cut_range_high_i = cut_range_mid_i

    if depth <= debug_depth:
        value = best_hp_solutions[0]["min_hp"]
        values = f"{value}"
        if len(best_hp_solutions) < 9:
            d_i = 1
        else:
            d_i = (len(best_hp_solutions) - 1) / 4
        i = d_i
        while i < len(best_hp_solutions):
            if d_i == 1:
                value = best_hp_solutions[i]["min_hp"]
                values += f", {value}"
            else:
                value = best_hp_solutions[int(i)]["min_hp"]
                values += f" ... {value}"
            i += d_i

        elapsed_time = time.time() - start_time
        print(f"best_hp_solutions: d={depth} count={len(best_hp_solutions)}, n={total_permutations} "
              f"t={elapsed_time:.8f}: [{values}]")

def gear_armor_value_spread(type_group):
    avail = type_group["avail"]
    if len(type_group) < 2:
        return 0
    min_physical = avail[0]["physical"]
    max_physical = min_physical
    min_magic = avail[0]["magic"]
    max_magic = min_magic
    for i in range(1, len(avail)):
        physical = avail[i]["physical"]
        if min_physical > physical:
            min_physical = physical
        if max_physical < physical:
            max_physical = physical
        magic = avail[i]["magic"]
        if min_magic > magic:
            min_magic = magic
        if max_magic < magic:
            max_magic = magic
    physical_spread = max_physical - min_physical
    magic_spread = max_magic - min_magic
    return max(physical_spread, magic_spread)

def build_all_armor_combinations(type_group, type_name, assign_item_i, characters, partial_assignment):
    global required_attrs
    global assignment_key_splits

    avail = type_group["avail"]
    assert assign_item_i < len(avail)
    assign_item = avail[assign_item_i]

    for character in characters:
        if type_name in character or (type_name == "ring" and ("ring1" in character and "ring2" in character)):
            continue
        character_name = character["name"]
        if "characters" in assign_item and not character_name in assign_item["characters"]:
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
            if "characters" in assign_item and not character["name"] in assign_item["characters"]:
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
        sorted_assignments = sorted(combination)
        for assignment in sorted_assignments:
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
    global debug_depth

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
                    character["hp"] += assigned_item["hp"]
                    found = True
            assert found

        total_permutations += 1
        if depth <= debug_depth:
            elapsed_time = time.time() - start_time
            print(f"A: d={depth} c={c_i+1}/{len(combinations)} t={elapsed_time:.8f} n={total_permutations} applying "
                  f"combination {combination}")

        if type_group_i < len(available_gear) - 1 and not is_dead_branch_armor(type_group_i + 1, characters):
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
                    character["hp"] -= assigned_item["hp"]
                    found = True
            assert found

def is_dead_branch_armor(min_type_group_i, characters):
    global best_armor_solutions
    global assignment_key_splits
    global total_solution_refinements
    global max_best_solutions
    global cofactor_start_count
    global cofactor_threshold

    if len(best_armor_solutions) == 0:
        return False

    best_min = calculate_min_armor(best_armor_solutions[0])

    for character in characters:
        character_name = character["name"]
        max_character_physical = character["physical"]
        max_character_magic = character["magic"]
        max_character_physical_cofactor_magic = max_character_magic
        max_character_magic_cofactor_physical = max_character_physical
        type_group_i = min_type_group_i
        while type_group_i < len(available_gear):
            type_group = available_gear[type_group_i]
            combinations = type_group["combinations"]
            best_type_physical = 0
            best_type_magic = 0
            best_type_physical_cofactor_magic = 0
            best_type_magic_cofactor_physical = 0

            for combination in combinations:
                for assignment in combination:
                    assignment_split = assignment_key_splits[assignment]
                    if assignment_split[0] == character_name:
                        assigned_item = combination[assignment]
                        if best_type_physical < assigned_item["physical"]:
                            best_type_physical = assigned_item["physical"]
                            best_type_physical_cofactor_magic = assigned_item["magic"]
                        if best_type_magic < assigned_item["magic"]:
                            best_type_magic = assigned_item["magic"]
                            best_type_magic_cofactor_physical = assigned_item["physical"]
            max_character_physical += best_type_physical
            max_character_magic += best_type_magic
            max_character_physical_cofactor_magic += best_type_physical_cofactor_magic
            max_character_magic_cofactor_physical += best_type_magic_cofactor_physical
            type_group_i += 1

        if max_character_physical < best_min:
            return True
        if max_character_magic < best_min:
            return True

        if (total_solution_refinements > cofactor_start_count and
                max_character_physical_cofactor_magic < best_min * cofactor_threshold):
            return True
        if (total_solution_refinements > cofactor_start_count and
                max_character_magic_cofactor_physical < best_min * cofactor_threshold):
            return True

    return False

def evaluate_for_armor(characters):
    global start_time
    global best_armor_solutions
    global total_solution_refinements

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
        total_solution_refinements += 1
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
        min_hp = calculate_min_hp(solution)
        physical_sum_of_squares = 0
        magic_sum_of_squares = 0
        p_m_diff_sum_of_squares = 0
        hp_sum_of_squares = 0
        for character in solution:
            physical_boost = character["physical"] - min_average
            physical_sum_of_squares += abs(physical_boost * physical_boost)
            magic_boost = character["magic"] - min_average
            magic_sum_of_squares += abs(magic_boost * magic_boost)
            p_m_diff = physical_boost - magic_boost
            p_m_diff_sum_of_squares += abs(p_m_diff * p_m_diff)
            hp_boost = character["hp"] - min_hp
            assert hp_boost >= 0
            hp_sum_of_squares += hp_boost * hp_boost
        solution[0]["variance_sum_of_squares"] = (physical_sum_of_squares + magic_sum_of_squares
                                                  + p_m_diff_sum_of_squares + hp_sum_of_squares)

    best_armor_solutions.sort(key=lambda s: s[0]["variance_sum_of_squares"])

main()