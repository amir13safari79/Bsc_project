import numpy as np
from .performance_table import get_performance_table


class RuleBase:
    def __init__(self, number_of_partitions: int, train=True, trained_rule_base=None):
        # self.rules = np.random.randint(low=-10, high=10, size=(number_of_partitions + 1, number_of_partitions)).astype("float")
        self.performance_table = get_performance_table(number_of_partitions)

        if train:
            self.rules = np.random.randint(low=-10, high=10, size=(number_of_partitions + 1, number_of_partitions)).astype("float")
        else:
            self.rules = trained_rule_base

    def update_rules(self, er_cr_rules_number: tuple, membership: float):
        er_cr_rules_number = (er_cr_rules_number[0] - 1, er_cr_rules_number[1] - 1)
        self.rules[er_cr_rules_number] = self.rules[er_cr_rules_number] + membership * self.performance_table[er_cr_rules_number]
        # self.rules[er_cr_rule_number] = self.rules[er_cr_rule_number] + self.performance_table[
        #     er_cr_rule_number]

    def get_rules(self):
        return self.rules

    def get_change_in_input(self, er_cr_rules_number: tuple, membership: float):
        er_cr_rules_number = (er_cr_rules_number[0] - 1, er_cr_rules_number[1] - 1)
        # er_cr_rule = (error_rule_number - 1, change_in_error_rule_number - 1)
        return membership * self.rules[er_cr_rules_number]
