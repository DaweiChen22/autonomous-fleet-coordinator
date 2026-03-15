import heapq
import numpy as np
from typing import List, Tuple, Dict

class AStarPathPlanner:
    """SOTA Path planning for autonomous units using A* algorithm on a grid mesh."""
    def __init__(self, grid_size: Tuple[int, int]):
        self.grid_size = grid_size

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def plan(self, start: Tuple[int, int], goal: Tuple[int, int], obstacles: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self.heuristic(start, goal)}
        oheap = []
        heapq.heappush(oheap, (fscore[start], start))

        while oheap:
            current = heapq.heappop(oheap)[1]
            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data[::-1]

            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                if 0 <= neighbor[0] < self.grid_size[0] and 0 <= neighbor[1] < self.grid_size[1]:
                    if neighbor in obstacles or neighbor in close_set: continue
                    
                    tentative_g_score = gscore[current] + self.heuristic(current, neighbor)
                    if neighbor not in [i[1] for i in oheap] or tentative_g_score < gscore.get(neighbor, 0):
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(oheap, (fscore[neighbor], neighbor))
        return []

if __name__ == "__main__":
    planner = AStarPathPlanner((100, 100))
    path = planner.plan((0,0), (10,10), [(5,5), (5,6), (5,4)])
    print(f"Autonomous Path Generated: {path}")
