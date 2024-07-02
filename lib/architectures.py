import networkx as nx
from typing import Callable


# IBM Quadalupe. Coupling graph based on Peham et. al
def ibmq_quadalupe() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 8),
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 0),
            (12, 0),
            (13, 4),
            (14, 6),
            (15, 8),
        ]
    )

    return G


# Example architecture from Peham et. al
def double_o_plus() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
    G.add_edges_from(
        {
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 0),
            (0, 5),
            (5, 6),
            (6, 7),
            (7, 8),
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 12),
            (12, 13),
            (13, 9),
            (7, 14),
            (14, 15),
            (14, 16),
            (14, 17),
        }
    )

    return G


# Tokyo architecture from IBM Qiskit
def ibmq_tokyo() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    )
    G.add_edges_from(
        [
            (0, 1),
            (0, 5),
            (1, 2),
            (1, 6),
            (2, 3),
            (2, 7),
            (3, 4),
            (3, 8),
            (4, 9),
            (9, 8),
            (8, 7),
            (8, 13),
            (8, 12),
            (7, 13),
            (7, 12),
            (7, 6),
            (6, 11),
            (6, 10),
            (6, 5),
            (5, 10),
            (5, 11),
            (10, 15),
            (10, 11),
            (11, 16),
            (11, 17),
            (11, 12),
            (12, 13),
            (13, 18),
            (13, 19),
            (13, 14),
            (14, 18),
            (14, 19),
        ]
    )

    return G


# Own example used in Bachelor's Project
def six_grid() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (2, 5), (3, 5), (4, 5)])

    return G


# Rigetti-8 architecture
# https://github.com/irfansha/Q-Synth/blob/main/architecture.py
def rigetti_8() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
    G.add_edges_from([(0, 4), (1, 5), (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)])
    return G


# Burlington architecture from IBM Qiskit
def ibmq_burlington() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4])
    G.add_edges_from([(0, 1), (1, 2), (1, 3), (3, 4)])
    return G


# 3x3 Grid architecture
def grid_3x3() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(list(range(9)))
    for r in range(3):
        G.add_edges_from((3 * r + i, 3 * r + i + 1) for i in range(2))
    for r in range(2):
        G.add_edges_from((3 * r + i, 3 * r + i + 3) for i in range(3))
    return G


# 4x4 Grid architecture
def grid_4x4() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(list(range(4)))
    for r in range(4):
        G.add_edges_from((4 * r + i, 4 * r + i + 1) for i in range(3))
    for r in range(3):
        G.add_edges_from((4 * r + i, 4 * r + i + 4) for i in range(4))
    return G


# Rigetti-12 architecture
# https://github.com/irfansha/Q-Synth/blob/main/architecture.py
def rigetti_12() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(list(range(12)))
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 0),
            (7, 8),
            (8, 9),
            (9, 0),
            (8, 10),
            (9, 11),
        ]
    )
    return G


# Rigetti-14 architecture
# https://github.com/irfansha/Q-Synth/blob/main/architecture.py
def rigetti_14() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(list(range(14)))
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 6),
            (3, 6),
            (1, 3),
            (0, 4),
            (0, 5),
            (4, 7),
            (5, 7),
            (2, 8),
            (6, 9),
            (3, 10),
            (4, 11),
            (7, 12),
            (5, 13),
        ]
    )
    return G


# Rigetti-16
# https://github.com/irfansha/Q-Synth/blob/main/architecture.py
def rigetti_16() -> nx.Graph():
    G = nx.Graph()
    G.add_nodes_from(list(range(16)))
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (0, 8),
            (3, 11),
            (4, 12),
            (7, 15),
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 12),
            (12, 13),
            (13, 14),
            (14, 15),
        ]
    )
    return G


# Rigetti-80
# https://github.com/irfansha/Q-Synth/blob/main/architecture.py
def rigetti_80() -> nx.Graph():
    G = nx.Graph()
    G.add_nodes_from(list(range(80)))
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 0),
            (0, 13),
            (1, 12),
            (2, 47),
            (3, 46),
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 12),
            (12, 13),
            (13, 14),
            (14, 15),
            (15, 8),
            (8, 21),
            (9, 20),
            (10, 55),
            (11, 54),
            (16, 17),
            (17, 18),
            (18, 19),
            (19, 20),
            (20, 21),
            (21, 22),
            (22, 23),
            (23, 16),
            (16, 29),
            (17, 28),
            (18, 63),
            (19, 62),
            (24, 25),
            (25, 26),
            (26, 27),
            (27, 28),
            (28, 29),
            (29, 30),
            (30, 31),
            (31, 24),
            (24, 37),
            (25, 36),
            (26, 71),
            (27, 70),
            (32, 33),
            (33, 34),
            (34, 35),
            (35, 36),
            (36, 37),
            (37, 38),
            (38, 39),
            (39, 32),
            (34, 79),
            (35, 78),
            (40, 41),
            (41, 42),
            (42, 43),
            (43, 44),
            (44, 45),
            (45, 46),
            (46, 47),
            (47, 40),
            (40, 53),
            (41, 52),
            (48, 49),
            (49, 50),
            (50, 51),
            (51, 52),
            (52, 53),
            (53, 54),
            (54, 55),
            (55, 48),
            (48, 61),
            (49, 60),
            (56, 57),
            (57, 58),
            (58, 59),
            (59, 60),
            (60, 61),
            (61, 62),
            (62, 63),
            (63, 56),
            (56, 69),
            (57, 68),
            (64, 65),
            (65, 66),
            (66, 67),
            (67, 68),
            (68, 69),
            (69, 70),
            (70, 71),
            (71, 64),
            (64, 77),
            (65, 76),
            (72, 73),
            (73, 74),
            (74, 75),
            (75, 76),
            (76, 77),
            (77, 78),
            (78, 79),
            (79, 72),
        ]
    )
    return G


# Google Sycamore
# https://github.com/irfansha/Q-Synth/blob/main/architecture.py
def sycamore() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(range(54))
    G.add_edges_from(
        [
            (0, 6),
            (1, 6),
            (1, 7),
            (2, 7),
            (2, 8),
            (3, 8),
            (3, 9),
            (4, 9),
            (4, 10),
            (5, 10),
            (5, 11),
            (6, 12),
            (6, 13),
            (7, 13),
            (7, 14),
            (8, 14),
            (8, 15),
            (9, 15),
            (9, 16),
            (10, 16),
            (10, 17),
            (11, 17),
            (12, 18),
            (13, 18),
            (13, 19),
            (14, 19),
            (14, 20),
            (15, 20),
            (15, 21),
            (16, 21),
            (16, 22),
            (17, 22),
            (17, 23),
            (18, 24),
            (18, 25),
            (19, 25),
            (19, 26),
            (20, 26),
            (20, 27),
            (21, 27),
            (21, 28),
            (22, 28),
            (22, 29),
            (23, 29),
            (24, 30),
            (25, 30),
            (25, 31),
            (26, 31),
            (26, 32),
            (27, 32),
            (27, 33),
            (28, 33),
            (28, 34),
            (29, 34),
            (29, 35),
            (30, 36),
            (30, 37),
            (31, 37),
            (31, 38),
            (32, 38),
            (32, 39),
            (33, 39),
            (33, 40),
            (34, 40),
            (34, 41),
            (35, 41),
            (36, 42),
            (37, 42),
            (37, 43),
            (38, 43),
            (38, 44),
            (39, 44),
            (39, 45),
            (40, 45),
            (40, 46),
            (41, 46),
            (41, 47),
            (42, 48),
            (42, 49),
            (43, 49),
            (43, 50),
            (44, 50),
            (44, 51),
            (45, 51),
            (45, 52),
            (46, 52),
            (46, 53),
            (47, 53),
        ]
    )
    return G


# IBM Eagle
# https://github.com/irfansha/Q-Synth/blob/main/architecture.py
def eagle() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(range(127))
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 8),
            (9, 10),
            (10, 11),
            (11, 12),
            (12, 13),
            (0, 14),
            (14, 18),
            (4, 15),
            (15, 22),
            (8, 16),
            (16, 26),
            (12, 17),
            (17, 30),
            (18, 19),
            (19, 20),
            (20, 21),
            (21, 22),
            (22, 23),
            (23, 24),
            (24, 25),
            (25, 26),
            (26, 27),
            (27, 28),
            (28, 29),
            (29, 30),
            (30, 31),
            (31, 32),
            (20, 33),
            (33, 39),
            (24, 34),
            (34, 43),
            (28, 35),
            (35, 47),
            (32, 36),
            (36, 51),
            (37, 38),
            (38, 39),
            (39, 40),
            (40, 41),
            (41, 42),
            (42, 43),
            (43, 44),
            (44, 45),
            (45, 46),
            (46, 47),
            (47, 48),
            (48, 49),
            (49, 50),
            (50, 51),
            (37, 52),
            (52, 56),
            (41, 53),
            (53, 60),
            (45, 54),
            (54, 64),
            (49, 55),
            (55, 68),
            (56, 57),
            (57, 58),
            (58, 59),
            (59, 60),
            (60, 61),
            (61, 62),
            (62, 63),
            (63, 64),
            (64, 65),
            (65, 66),
            (66, 67),
            (67, 68),
            (68, 69),
            (69, 70),
            (58, 71),
            (71, 77),
            (62, 72),
            (72, 81),
            (66, 73),
            (73, 85),
            (70, 74),
            (74, 89),
            (75, 76),
            (76, 77),
            (77, 78),
            (78, 79),
            (79, 80),
            (80, 81),
            (81, 82),
            (82, 83),
            (83, 84),
            (84, 85),
            (85, 86),
            (86, 87),
            (87, 88),
            (88, 89),
            (75, 90),
            (90, 94),
            (79, 91),
            (91, 98),
            (83, 92),
            (92, 102),
            (87, 93),
            (93, 106),
            (94, 95),
            (95, 96),
            (96, 97),
            (97, 98),
            (98, 99),
            (99, 100),
            (100, 101),
            (101, 102),
            (102, 103),
            (103, 104),
            (104, 105),
            (105, 106),
            (106, 107),
            (107, 108),
            (96, 109),
            (100, 110),
            (110, 118),
            (104, 111),
            (111, 112),
            (108, 112),
            (112, 126),
            (113, 114),
            (114, 115),
            (115, 116),
            (116, 117),
            (117, 118),
            (118, 119),
            (119, 120),
            (120, 121),
            (121, 122),
            (122, 123),
            (123, 124),
            (124, 125),
            (125, 126)
        ]
    )
    return G

# Map from architecture name to generators
architecture: dict[str, Callable[None, nx.Graph]] = {
    "ibmq_quadalupe": ibmq_quadalupe,
    "double_o_plus": double_o_plus,
    "ibmq_tokyo": ibmq_tokyo,
    "six_grid": six_grid,
    "rigetti_8": rigetti_8,
    "ibmq_burlington": ibmq_burlington,
    "grid_3x3": grid_3x3,
    "grid_4x4": grid_4x4,
    "rigetti_12": rigetti_12,
    "rigetti_14": rigetti_14,
    "rigetti_16": rigetti_16,
    "rigetti_80": rigetti_80,
    "google_sycamore": sycamore,
    "ibmq_eagle": eagle,
}
