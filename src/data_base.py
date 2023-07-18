import numpy as np


class DataBase:
    def __init__(self, universe_discourse_range: tuple, number_of_partitions: int):
        self.universe_discourse_start = universe_discourse_range[0]
        self.universe_discourse_end = universe_discourse_range[1]
        self.number_of_partitions = number_of_partitions
        self.partition_size = 2 * (self.universe_discourse_end - self.universe_discourse_start) / (
                self.number_of_partitions + 1)
        self.half_partition_size = self.partition_size / 2
        # self.database_type = database_type

    def get_rule_and_membership(self, x: int):
        rule_membership = {}
        if x < self.universe_discourse_start:
            x = self.universe_discourse_start

        if x > self.universe_discourse_end:
            x = self.universe_discourse_end

        if x < self.universe_discourse_start or x > self.universe_discourse_end:
            raise ValueError(f"x = {x}, x should be between discourse_start = {self.universe_discourse_start} and discourse_end = {self.universe_discourse_end}")

        if (x - self.universe_discourse_start) <= self.half_partition_size:
            rule1 = 1
            membership1 = (x - self.universe_discourse_start) / self.half_partition_size

            rule_membership[rule1] = membership1

        elif (self.universe_discourse_end - x) <= self.half_partition_size:
            rule1 = self.number_of_partitions
            membership1 = (self.universe_discourse_end - x) / self.half_partition_size

            rule_membership[rule1] = membership1
        else:
            rule1 = int(np.ceil((x - self.universe_discourse_start) / self.half_partition_size))
            rule2 = rule1 - 1

            membership1 = abs(self.universe_discourse_start + (
                        rule1 - 1) * self.half_partition_size - x) / self.half_partition_size
            membership2 = (self.universe_discourse_start + (
                    rule2 + 1) * self.half_partition_size - x) / self.half_partition_size

            rule_membership[rule1] = membership1
            rule_membership[rule2] = membership2

        return rule_membership

