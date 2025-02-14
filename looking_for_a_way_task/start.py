from looking_for_a_way_task.map import Map


def generate_tuple_with_coords(coords: str) -> tuple:
    """
    Method to create a tuple with coords from given string.

    :param coords: String with coordinates by user.
    :return: Tuple of coordinates.
    """
    result = ()
    for item in coords:
        if not item.isdigit():
            continue
        else:
            result += (int(item),)
    return result


def main():
    print("Hello!")
    print("Choose length.")
    length = int(input())
    print("Choose width.")
    width = int(input())
    print("Choose type of the map: 1 - Continents; 2 - Islands; 3 - Pangea")
    type_of_map = int(input())
    print("Choose percentage of land on the map.")
    percentage = int(input())
    map = Map(length, width, percentage, type_of_map)
    map.generate_map()
    map.show_map()
    print("Choose start coordinates. For example: (0, 1)")
    start = generate_tuple_with_coords(input())
    print("Choose finish coordinates. For example: (9, 9)")
    finish = generate_tuple_with_coords(input())
    map.find_path(start, finish)
    map.show_map()


if __name__ == '__main__':
    main()
