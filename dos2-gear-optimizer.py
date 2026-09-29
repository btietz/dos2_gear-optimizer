import copy
import hashlib
import random
import sys
import time

characters = [
    {"name": "Brian",
     "physical": 43,
     "magic": 35,
     "strength": 13,
     "intelligence": 10,
     "finesse": 10,
     "chest": None,
     "gloves": None,
    },
    {"name": "Beast",
     "physical": 16,
     "magic": 4,
     "strength": 12,
     "intelligence": 12,
     "finesse": 10,
     "chest": None,
    },
    {"name": "Lohse",
     "physical": 0,
     "magic": 0,
     "strength": 10,
     "intelligence": 13,
     "finesse": 10,
    },
    {"name": "Fane",
     "physical": 0,
     "magic": 8,
     "strength": 10,
     "intelligence": 14,
     "finesse": 10,
    },
]

available_gear = [
    {"type": "helmet",
     "avail": [
        {"name": "HoP",
         "physical": 10,
         "magic": 3,
         "strength": 11,
        },
        {"name": "M",
         "physical": 3,
         "magic": 12,
         "intelligence": 11,
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
        {"name": "SA",
         "physical": 8,
         "magic": 6,
        },
        {"name": "SSA",
         "physical": 12,
         "magic": 3,
        },
     ]
    },
    {"type": "gloves",
     "avail": [
        {"name": "SSG",
         "physical": 8,
         "magic": 2,
         "strength": 11,
        },
        {"name": "MLG",
         "physical": 4,
         "magic": 3,
        },
        {"name": "WM",
         "physical": 2,
         "magic": 7,
        },
     ]
    },
    {"type": "pants",
     "avail": [
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
        {"name": "FT",
         "physical": 3,
         "magic": 0,
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
    {"type": "ring",
     "avail": [
        {"name": "AR",
         "physical": 0,
         "magic": 8,
        },
        {"name": "DR",
         "physical": 0,
         "magic": 6,
        },
        {"name": "JR",
         "physical": 0,
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
]

best_solutions = []
best_solutions_sigs = set()
max_best_solutions = 40
already_evaluated_sig_hash_num_bits = 36
already_evaluated_sig_hash_mask = (1 << already_evaluated_sig_hash_num_bits) - 1
already_evaluated_sig_hash_num_bytes = 1 << (already_evaluated_sig_hash_num_bits - 3)
already_evaluated_bitmap = bytearray(already_evaluated_sig_hash_num_bytes)
start_time = time.time()
debug_depth = 0
termination_factor = 0.0
total_permutations = 0

required_attrs = set(["strength", "intelligence", "finesse"])

def main():
    global debug_depth
    global termination_factor
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

    for character in characters:
        for key in required_attrs:
            if not key in character:
                name = character["name"]
                raise KeyError(f"{name} missing {key}") 

    num_items = 0
    for type_group in available_gear:
        num_items += len(type_group["avail"])
    assert num_items > 0
    termination_factor = calculate_termination_factor(num_items)

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

    explore_all(characters, available_gear, 0, pin_type_i, pin_avail_i, True)

    for sweep_pass_limited in [True, False]:
        best_limited_solutions = copy.deepcopy(best_solutions)
        for solution_i in range(0, len(best_limited_solutions)):
            solution = best_limited_solutions[solution_i]
            available_gear_after_assignments = copy.deepcopy(available_gear)
            for character in solution:
                for key in character:
                    if key in set(["name", "physical", "magic"]) or key in required_attrs:
                        continue
                    assigned_item_type = key
                    assigned_item = character[key]
                    if assigned_item == None:
                        continue
                    assigned_item_name = assigned_item["name"]
                    found_and_removed = False
                    for type_group in available_gear_after_assignments:
                        if type_group["type"] == assigned_item_type:
                            avail = type_group["avail"]
                            for i in range(0, len(avail)):
                                avail_item = avail[i]
                                if avail_item["name"] == assigned_item_name:
                                    avail.pop(i)
                                    found_and_removed = True
                                    break
                        if found_and_removed:
                            break
                    if not found_and_removed:
                        raise KeyError(f"item multiply assigned: {assigned_item_type}, {assigned_item_name}")

            all_slots_filled = True
            for character in solution:
                for type_group in available_gear_after_assignments:
                    item_type = type_group["type"]
                    if not item_type in character:
                        for item in type_group["avail"]:
                            item_name = item["name"]
                            attr_minimum_met = True
                            for attr in required_attrs:
                                if attr in item:
                                    if character[attr] < item[attr]:
                                        attr_minimum_met = False
                            if attr_minimum_met:
                                character_name = character["name"]
                                print(f"character {character_name} could take {item_type}: {item_name}")
                                all_slots_filled = False

            if not all_slots_filled:
                print(f"retrying limited solution {solution_i}")
                print(f"remaining gear: {available_gear_after_assignments}")
                explore_all(solution, available_gear_after_assignments, 0, None, None, sweep_pass_limited)

    remove_suboptimal_solutions()
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

def calculate_termination_factor(N):
    survival_prob = 24.25 * (N ** -1.917)
    
    T_prob = 1.0 - survival_prob

    return min(0.99999, max(0.0, T_prob))
    
def explore_all(characters, available_gear, depth, pin_type_i, pin_avail_i, allow_termination):
    global start_time
    global already_evaluated_bitmap
    global total_permutations
    global debug_depth
    global termination_factor

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
                if depth > 1 and termination_factor > 0.0:
                    if allow_termination and random.random() <= termination_factor:
                        continue
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
                    attr_minimum_met = True
                    for attr in required_attrs:
                        if attr in item:
                            if character[attr] < item[attr]:
                                attr_minimum_met = False
                    if not attr_minimum_met:
                        continue

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
                            explore_all(characters, available_gear, depth + 1, None, False, allow_termination)

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
            if key == "name" or key == "physical" or key == "magic" or key in required_attrs:
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
        limit_best_solutions(max_best_solutions - 1)
        best_solutions.insert(0, copy.deepcopy(characters))
        best_solutions_sigs.add(sig)
        print(f"min: {new_min}, average: {new_average}, t={elapsed_time:.8f}")
        print(f"{best_solutions}")
        return
    if new_min == existing_min and new_average == existing_average:
        limit_best_solutions(max_best_solutions - 1)
        best_solutions.insert(0, copy.deepcopy(characters))
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

def limit_best_solutions(n):
    global best_solutions

    if len(best_solutions) > n:
        assert len(best_solutions) == n + 1
        i = random.randint(1, n)

        # Remove a random one
        removed = best_solutions.pop(i)
        best_solutions_sigs.remove(characters_sig(removed))

        # Also remove the oldest (worst) one
        removed = best_solutions.pop()
        best_solutions_sigs.remove(characters_sig(removed))

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

def remove_suboptimal_solutions():
    best_min = calculate_min(best_solutions[0])
    best_average = calculate_average(best_solutions[0])
    while len(best_solutions) > 1:
        if calculate_min(best_solutions[-1]) < best_min or calculate_average(best_solutions[-1]) < best_average:
            best_solutions.pop()
        else:
            return

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