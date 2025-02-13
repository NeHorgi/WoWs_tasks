import heapq
import math
import random


class Map:

    def __init__(self, length, width, land_percent, map_type):
        self.__length = length
        self.__width = width
        self.__land_percent = land_percent
        self.__map_type = map_type
        self.__map = None

    @property
    def map(self):
        if self.__map:
            return self.__map
        else:
            print("Map is not created yet.")

    def show_map(self):
        if self.map:
            for row in self.map:
                print(row)

    def generate_map(self):
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
    def shortest_way(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start, finish):
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
