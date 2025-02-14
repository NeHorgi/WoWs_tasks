import heapq
import math
import random


class Map:
    """
    A Class for working with simple 2D map as a list of lists with strings.

    Attributes:
        __length (int): The number of rows in the map.
        __width (int): The number of columns in the map.
        __land_percent (float): The percentage of land coverage on the map.
        __map_type (int): The type of map generation:
            1 - Randomly scattered land tiles.
            2 - Clustered islands.
            3 - Centralized landmass.
        __map (list[list[str]]): The map.

    Examples:

        Map(length=10, width=10, percentage=30, type_of_map=1)

    """

    def __init__(self, length, width, land_percent, map_type):
        self.__length = length
        self.__width = width
        self.__land_percent = land_percent
        self.__map_type = map_type
        self.__map = None

    @property
    def map(self) -> list[list[str]] | None:
        """
        Property that returns the generated map if it exists.

        :return: The generated map as a list of lists with strings, or None if not generated.
        """
        if self.__map:
            return self.__map
        else:
            print("Map is not created yet.")

    def show_map(self):
        """
        Method that prints the generated map.
        """
        if self.map:
            for row in self.map:
                print(row)

    def generate_map(self) -> list[list[str]]:
        """
        Method that generates a map with randomly scattered land tiles.

        :return: Updated map with randomly scattered land tiles as a list of lists with strings.
        """
        if not self.__map:
            self.__map = [['~' for _ in range(self.__width)] for _ in range(self.__length)]
            total_cells = self.__length * self.__width
            land_cells = int(total_cells * self.__land_percent / 100)

            if self.__map_type == 1:
                for _ in range(land_cells):
                    x, y = random.randint(0, self.__width - 1), random.randint(0, self.__length - 1)
                    self.__map[y][x] = "■"

            elif self.__map_type == 2:
                count_of_islands = max(1, self.__width // 10)
                for _ in range(count_of_islands):
                    cx, cy = random.randint(0, self.__width - 1), random.randint(0, self.__length - 1)
                    for _ in range(land_cells // count_of_islands):
                        x = min(self.__width - 1, max(0, cx + random.randint(-3, 3)))
                        y = min(self.__length - 1, max(0, cy + random.randint(-3, 3)))
                        self.__map[y][x] = "■"

            elif self.__map_type == 3:
                center_x, center_y = self.__width // 2, self.__length // 2
                radius = min(self.__width, self.__length) // 3
                for _ in range(land_cells):
                    angle = random.uniform(0, 2 * 3.1415)
                    r = random.uniform(0, radius)
                    x = min(self.__width - 1, max(0, int(center_x + r * math.cos(angle))))
                    y = min(self.__length - 1, max(0, int(center_y + r * math.sin(angle))))
                    self.__map[y][x] = "■"
            return self.__map
        else:
            print("Map was already created, it is not needed to create it again.")

    @staticmethod
    def shortest_way(start: tuple[int, int], finish: tuple[int, int]) -> int:
        """
        Computes the Manhattan distance between two points on the map.

        :param start: Start coordinate (x, y).
        :param finish: Finish coordinate (x, y).
        :return: The Manhattan distance between start and finish.
        """
        return abs(start[0] - finish[0]) + abs(start[1] - finish[1])

    def find_path(self, start, finish) -> list[tuple[int, int]] | None:
        """
        Finds the shortest path between two points using the A* algorithm.

        :param start: Start coordinate (x, y).
        :param finish: Finish coordinate (x, y).
        :return: The shortest path between start and finish if it exists.
        """
        if self.__map is None:
            print("Error: Map is not created yet.")
            return None

        if self.__map[start[1]][start[0]] == "■" or self.__map[finish[1]][finish[0]] == "■":
            print("Start or Finish is on land. No path possible.")
            return None

        open_set = []
        heapq.heappush(open_set, (0, start))
        open_set_hash = {start}

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.shortest_way(start, finish)}

        while open_set:
            _, current = heapq.heappop(open_set)
            open_set_hash.remove(current)

            if current == finish:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()

                for x, y in path:
                    self.__map[y][x] = "a"

                return path

            x, y = current
            neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

            for neighbor in neighbors:
                nx, ny = neighbor
                if 0 <= nx < self.__width and 0 <= ny < self.__length and self.__map[ny][nx] == "~":
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.shortest_way(neighbor, finish)

                        if neighbor not in open_set_hash:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
                            open_set_hash.add(neighbor)

        print("No path found between these coordinates.")
        return None
