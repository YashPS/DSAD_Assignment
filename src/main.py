def read_inputs(path):
    """Reads the input data from path as specified.

    Parameters:
        path (str): Path of the file to be read.

    Raises:
        ValueError: Invalid input file, not enough weapons data provided based on weapon count

    Returns:
        weapon_count: Number of weapons for which ammunition data is provided
        max_weight: Maximum permissible cumulative weight of ammunition weights
        data: Ammunition data

    """
    with open(path, 'r') as inp:
        data = []
        weapon_count = int(
            inp.readline().strip().split(':')[1].strip())  # Numbers after colon of first line is weapon count
        max_weight = int(
            inp.readline().strip().split(':')[1].strip())  # Numbers after colon of second line is max weight

        try:
            for count in range(weapon_count):
                ammunition, weight, damage = inp.readline().strip().split('/')
                data.append([ammunition.strip(), weight.strip(), damage.strip()])
        except ValueError:
            exit()

        return weapon_count, max_weight, data


def select_ammunition(weapons, max_weight, data):
    """Finds optimal selection of ammunition based on greedy method.

    Parameters:
        weapons (int): Number of weapons for which ammunition is to be picked
        max_weight (int): Maximum weight allowed
        data (list): Weight and damage stats for all ammunition types

    Returns:
        selected_list: List of ammunition that fits the input criteria and is optimum
        total_damage: Total damage output of the selected ammunition

    """
    damage_per_kg_list = []
    selected_list = []
    total_damage = 0

    for item in data:
        weapon, weight, damage = item[0], item[1], item[2]
        damage_per_kg = round(int(int(damage) / int(weight)), 2)
        damage_per_kg_list.append([damage_per_kg, weapon, int(weight), int(damage)])

    damage_per_kg_list = sorted(damage_per_kg_list, reverse=True)
    remaining_space = max_weight

    for item in damage_per_kg_list:
        if remaining_space - item[2] > 0:
            remaining_space -= item[2]
            selected_list.append([item[1], 1, item[2], item[3]])
        elif remaining_space - item[2] == 0:
            selected_list.append([item[1], 1, item[2], item[3]])
            break
        else:
            selected_list.append([item[1], (remaining_space / item[2]), item[2], item[3]])
            break

    selected_list = sorted(selected_list)

    for item in selected_list:
        total_damage += item[1] * item[3]

    return selected_list, total_damage


def write_output(path, selected_list, total_damage):
    """Writes output data to the file at the specified path.

    Parameters:
        path (str): Path to write output data to
        selected_list (list): Data to be written to output file
        total_damage (int): Total damage of the selected ammunitions

    """
    with open(path, 'w') as outp:
        outp.write('Total Damage: {}\n'.format(round(total_damage, 2)))
        outp.write('Ammunition Packs Selection Ratio:\n')
        for item in selected_list:
            outp.write('{} > {}\n'.format(item[0], round(item[1], 2)))


def main():
    """Uses greedy algorithm to find optimum selection of ammunition based on input data

    """
    weapons, max_weight, data = read_inputs('src\\inputPS3.txt')
    selected_list, total_damage = select_ammunition(weapons, max_weight, data)
    write_output('src\\outputPS3.txt', selected_list, total_damage)


if __name__ == '__main__':
    main()
