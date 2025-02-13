from looking_for_a_way_task.map import Map


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
    start = tuple(input())
    print("Choose finish coordinates. For example: (9, 9)")
    finish = tuple(input())
    map.find_path(start, finish)
    map.show_map()


if __name__ == '__main__':
    main()
