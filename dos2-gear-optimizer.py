import copy
import hashlib
import sys
import time

characters = [
    {"name": "Brian",
     "physical": 39,
     "magic": 18,
     "gloves": None,
     "belt": None,
     "ring": None,
    },
    {"name": "The Red Prince",
     "physical": 17,
     "magic": 3,
    },
    {"name": "Sebille",
     "physical": 12,
     "magic": 10,
     "gloves": None,
    },
    {"name": "Fane",
     "physical": 11,
     "magic": 10,
     "ring": None,
    },
]

available_gear = [
    {"type": "shoes",
     "avail": [
        {"name": "MS",
         "physical": 1,
         "magic": 6,
        },
        {"name": "BSB",
         "physical": 4,
         "magic": 1,
        },
        {"name": "TS2",
         "physical": 2,
         "magic": 0,
        },
        {"name": "TS1",
         "physical": 1,
         "magic": 0,
        },
     ]
    },
    {"type": "gloves",
     "avail": [
        {"name": "WM",
         "physical": 2,
         "magic": 7,
        },
        {"name": "MM",
         "physical": 2,
         "magic": 0,
        },
     ]
    },

    {"type": "pants",
     "avail": [
        {"name": "WL",
         "physical": 3,
         "magic": 9,
        },
        {"name": "WP",
         "physical": 1,
         "magic": 5,
        },
        {"name": "FT",
         "physical": 3,
         "magic": 0,
        },
        {"name": "FT",
         "physical": 3,
         "magic": 0,
        },
     ]
    },
    {"type": "belt",
     "avail": [
        {"name": "RB",
         "physical": 6,
         "magic": 0,
        },
     ]
    },
    {"type": "ring",
     "avail": [
        {"name": "DR",
         "physical": 0,
         "magic": 6,
        },
     ]
    },
    {"type": "necklace",
     "avail": [
        {"name": "SN",
         "physical": 0,
         "magic": 8,
        },
     ]
    },
]

best_solutions = []
best_solutions_sigs = set()
already_evaluated_sig_hash_num_bits = 36
already_evaluated_sig_hash_mask = (1 << already_evaluated_sig_hash_num_bits) - 1
already_evaluated_sig_hash_num_bytes = 1 << (already_evaluated_sig_hash_num_bits - 3)
already_evaluated_bitmap = bytearray(already_evaluated_sig_hash_num_bytes)
start_time = time.time()
debug_depth = 0
total_permutations = 0

def main():
    global debug_depth
    global characters
    global available_gear
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

    pin_type_i = 0
    pin_type_i_num_constraints = 0
    pin_avail_i = False
    for type_i in range(0, len(available_gear)):
        type_group = available_gear[type_i]
        type_name = type_group["type"]
        num_constraints = 0
        for character in characters:
            if type_name in character:
                num_constraints += 1
        type_group_can_pin_avail_i = (num_constraints + len(type_group["avail"]) <= len(characters))

        if (type_group_can_pin_avail_i and not pin_avail_i) or ((type_group_can_pin_avail_i == pin_avail_i)
                                                                and pin_type_i_num_constraints < num_constraints):
            pin_type_i = type_i
            pin_type_i_num_constraints = num_constraints
            pin_avail_i = type_group_can_pin_avail_i
            print(f"pin_type_i={pin_type_i}, pin_avail_i={pin_avail_i} type_name={type_name}, "
                  f"num_constraints={num_constraints}")

    explore_all(characters, available_gear, 0, pin_type_i, pin_avail_i)

    sort_best_solutions_min_variance_first()

    for i in range(0, min(len(best_solutions), 8)):
        print(f"\nOPTION {i+1}:\n")
        solution = best_solutions[i]
        for character in solution:
            print(character["name"])
            print(character["physical"])
            print(character["magic"])
            for key in character:
                if key == "name" or key == "physical" or key == "magic" or key == "variance_sum_of_squares":
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

def explore_all(characters, available_gear, depth, pin_type_i, pin_avail_i):
    global start_time
    global already_evaluated_bitmap
    global total_permutations
    global debug_depth

    type_count = len(available_gear)
    type_i = 0
    while type_i < type_count:
        if pin_type_i != None and type_i != pin_type_i:
            type_i += 1
            continue
        type = available_gear[type_i]
        type_name = type["type"]
        avail = type["avail"]
        avail_count = len(avail)
        if avail_count > 1:
            pop_item = True
        else:
            pop_item = False

        avail_i = 0
        while avail_i < avail_count:
            if pin_avail_i and avail_i != 0:
                avail_i += 1
                continue
            item = avail[avail_i]

            type_item_s = None
            if depth <= debug_depth:
                type_item_s = f"type: {type_i+1} of {type_count} ("
                for i in range(0, type_count):
                    if i > 0:
                        type_item_s += " "
                    if i == type_i:
                        type_item_s += "*"
                    type_item_s += available_gear[i]["type"]
                type_item_s += f") item: {avail_i+1} of {avail_count} ("
                for i in range(0, avail_count):
                    if i > 0:
                        type_item_s += " "
                    if i == avail_i:
                        type_item_s += "*"
                    type_item_s += avail[i]["name"]
                type_item_s += ")"

            if pop_item:
                avail.pop(avail_i)
            else:
                available_gear.pop(type_i)

            for character_i in range(0, len(characters)):
                if depth <= debug_depth:
                    elapsed_time = time.time() - start_time
                    debug_s = f"d={depth} c={character_i} t={elapsed_time:.6f} "
                    while len(debug_s) < 24:
                        debug_s += " "
                    debug_s += f"n={total_permutations} "
                    while len(debug_s) < 37:
                        debug_s += " "
                    debug_s += "| "
                    debug_s += ("  " * depth)
                    debug_s += type_item_s
                    print(debug_s)

                character = characters[character_i]
                if not type_name in character:
                    character[type_name] = item
                    character["physical"] += item["physical"]
                    character["magic"] += item["magic"]

                    sig = characters_sig(characters)
                    sig_byte_index = sig >> 3
                    sig_mask = 1 << (sig & 7)

                    if not (already_evaluated_bitmap[sig_byte_index] & sig_mask):
                        already_evaluated_bitmap[sig_byte_index] |= sig_mask

                        if not is_dead_branch(character, available_gear):
                            evaluate(characters, sig)
                            explore_all(characters, available_gear, depth + 1, None, False)

                    del character[type_name]
                    character["physical"] -= item["physical"]
                    character["magic"] -= item["magic"]

            if pop_item:
                avail.insert(avail_i, item)
            else:
                available_gear.insert(type_i, type)

            avail_i += 1
        type_i += 1

def characters_sig(characters):
    sig = ""
    for character in characters:
        character_name = character["name"]
        sig += f"::{character_name}"
        keys = list(character)
        keys.sort()
        for key in keys:
            if key == "name" or key == "physical" or key == "magic":
                continue
            item = character[key]
            if item is None:
                continue
            item_name = character[key]["name"]
            item_physical = character[key]["physical"]
            item_magic = character[key]["magic"]
            sig += f":{item_name}({item_physical},{item_magic})"

    digest = hashlib.sha256(sig.encode('utf-8')).digest()
    return int.from_bytes(digest[:8], byteorder='big') & already_evaluated_sig_hash_mask

def evaluate(characters, sig):
    global start_time
    global best_solutions
    global best_solutions_sigs
    global total_permutations

    total_permutations += 1

    new_min = calculate_min(characters)
    new_average = calculate_average(characters)

    if len(best_solutions) == 0:
        best_solutions = [copy.deepcopy(characters)]
        best_solutions_sigs.add(sig)
        print(f"min: {new_min}, average: {new_average}")
        print(f"{best_solutions}")
        return

    if sig in best_solutions_sigs:
        return  # already there

    existing_min = calculate_min(best_solutions[0])
    existing_average = calculate_average(best_solutions[0])
    elapsed_time = time.time() - start_time

    if new_min > existing_min or (new_min == existing_min and new_average > existing_average):
        best_solutions = [copy.deepcopy(characters)]
        best_solutions_sigs.clear()
        best_solutions_sigs.add(sig)
        print(f"min: {new_min}, average: {new_average}, t={elapsed_time:.8f}")
        print(f"{best_solutions}")
        return
    if new_min == existing_min and new_average == existing_average:
        best_solutions.append(copy.deepcopy(characters))
        best_solutions_sigs.add(sig)
        print(f"min: {new_min}, average: {new_average}, t={elapsed_time:.8f}, count: {len(best_solutions)}")
        return

def calculate_min(characters):
    result = characters[0]["physical"]
    for character in characters:
        if result > character["physical"]:
            result = character["physical"]
        if result > character["magic"]:
            result = character["magic"]
    return result

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

def calculate_average(characters):
    result = 0
    for character in characters:
        result += character["physical"]
        result += character["magic"]
    return result / (len(characters) * 2)

def is_dead_branch(character, available_gear):
    global best_solutions

    if len(best_solutions) == 0:
        return False

    best_possible_physical = character["physical"]
    best_possible_magic = character["magic"]
    for avail_type in available_gear:
        avail_type_name = avail_type["type"]

        if avail_type_name in character:
            continue

        best_add_physical = 0
        best_add_magic = 0

        avail_items = avail_type["avail"]
        for avail_item in avail_items:
            if best_add_physical < avail_item["physical"]:
                best_add_physical = avail_item["physical"]
            if best_add_magic < avail_item["magic"]:
                best_add_magic = avail_item["magic"]

        best_possible_physical += best_add_physical
        best_possible_magic += best_add_magic

    if best_possible_physical < calculate_min_physical(best_solutions[0]):
        return True
    if best_possible_magic < calculate_min_magic(best_solutions[0]):
        return True

    return False

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