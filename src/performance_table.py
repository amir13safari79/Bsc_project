import numpy as np

full_performance_table = np.array([[0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6],
                                   [0, 0, 0, 2, 2, 3, 6, 6, 6, 6, 6, 6, 6],
                                   [0, 0, 0, 2, 4, 5, 6, 6, 6, 6, 6, 6, 6],
                                   [0, 0, 0, 2, 2, 3, 4, 4, 4, 4, 5, 5, 6],
                                   [0, 0, 0, 0, 0, 0, 2, 2, 2, 3, 4, 5, 6],
                                   [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 3, 4, 5],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -2, -3, -4],
                                   [0, 0, 0, 0, 0, 0, -1, -1, -1, -2, -3, -4, -5],
                                   [0, 0, 0, 0, 0, 0, -2, -2, -2, -3, -4, -5, -6],
                                   [0, 0, 0, -2, -2, -3, -4, -4, -4, -4, -5, -5, -6],
                                   [0, 0, 0, -2, -4, -5, -6, -6, -6, -6, -6, -6, -6],
                                   [0, 0, 0, -2, -2, -3, -6, -6, -6, -6, -6, -6, -6],
                                   [0, 0, 0, 0, 0, 0, -6, -6, -6, -6, -6, -6, -6]]
                                  ).astype("float")


def get_performance_table(number_of_partitions):
    performance_table = full_performance_table[6 - number_of_partitions // 2: 8 + number_of_partitions // 2,
                                               6 - number_of_partitions // 2: 7 + number_of_partitions // 2]

    return performance_table

