from src.rule_base import RuleBase
from src.data_base import DataBase

import cv2
import numpy as np
import copy
import pprint

input_image = cv2.imread('images/org_image.jpeg', cv2.IMREAD_GRAYSCALE).astype("float")
blurred_image = cv2.imread('images/blurred_image.jpeg', cv2.IMREAD_GRAYSCALE).astype("float")
input_h_dim = input_image.shape[0]
input_w_dim = input_image.shape[1]

# changed_image = input_image - blurred_image
# print(np.min(changed_image))

# for test use one pixel:
# input_value = int(input_image[100, 100])
# desired_value = int(blurred_image[100, 100])
# input_value = 100
# desired_value = 200
# test_mat = input_image[4, 2] - blurred_image[4, 2]
# print(test_mat)

# create rule_base:
number_of_partitions = 9
# initial rule base and database
data_base = DataBase((-75, 75), number_of_partitions)

window_size = 15
h_window_count = input_h_dim // window_size + 1
w_window_count = input_w_dim // window_size + 1
final_rule_base = np.zeros((number_of_partitions + 1, number_of_partitions))


# print(input_h_dim, input_w_dim)
# initial some values:
for row_ind in range(h_window_count):
    for col_ind in range(w_window_count):
        window_rule_base = np.zeros((number_of_partitions + 1, number_of_partitions))
        for pixel1 in range(row_ind*window_size, min((row_ind+1)*window_size, input_h_dim)):
            for pixel2 in range(col_ind*window_size, min((col_ind+1)*window_size, input_w_dim)):
                rule_base = copy.deepcopy(RuleBase(number_of_partitions))
                input_value = input_image[pixel1, pixel2]
                new_value = input_value
                desired_value = blurred_image[pixel1, pixel2]
                new_error = new_value - desired_value
                old_error = 0
                change_in_error = np.random.randint(-10, 10, 1)[0]

                for i in range(20):
                    # update rules:
                    if i > 0:
                        activated_rules_number = list(active_rules_number_membership.keys())
                        activated_rules_membership = list(active_rules_number_membership.values())
                        for idx in range(len(activated_rules_number)):
                            rule_base.update_rules(activated_rules_number[idx], active_rules_membership[idx])

                    error_rule_membership = data_base.get_rule_and_membership(new_error)
                    cr_rule_membership = data_base.get_rule_and_membership(change_in_error)

                    # find active rule_numbers:
                    active_rules_number_membership = {}
                    er_rules, er_memberships = list(error_rule_membership.keys()), list(error_rule_membership.values())
                    cr_rules, cr_memberships = list(cr_rule_membership.keys()), list(cr_rule_membership.values())

                    for j in range(len(error_rule_membership)):
                        for k in range(len(cr_rule_membership)):
                            er_rule, er_membership = er_rules[j], er_memberships[j]
                            cr_rule, cr_membership = cr_rules[k], cr_memberships[k]

                            if er_rule > (number_of_partitions // 2) + 1:
                                er_rule += 1
                            elif er_rule == (number_of_partitions // 2) + 1:
                                er_rule = er_rule + 1 if new_error > 0 else er_rule
                            else:
                                pass

                            active_rules_number_membership[(er_rule, cr_rule)] = min(er_membership, cr_membership)

                    # find change in input and update new_value:
                    active_rules_number = list(active_rules_number_membership.keys())
                    active_rules_membership = list(active_rules_number_membership.values())
                    for idx in range(len(active_rules_number_membership)):
                        new_value += rule_base.get_change_in_input(active_rules_number[idx], active_rules_membership[idx])

                    # update old_error, new_error, change_in_error:
                    old_error = new_error
                    new_error = new_value - desired_value
                    change_in_error = new_error - old_error
                    if abs(new_error) < 0.2:
                        # print(f"{i}:")
                        # print(f"for ({pixel1}, {pixel2}):")
                        # print(new_value, new_error, change_in_error, desired_value, input_value)
                        # rule_bases.append(rule_base.get_rules())
                        window_rule_base += (rule_base.get_rules() / (window_size ** 2))
                        # print(rule_base.get_rules())
                        break
        # print(window_rule_base)
        final_rule_base += window_rule_base / (h_window_count * w_window_count)

    # print((row_ind, col_ind))


# test final_rule_base:
is_converge = True
for pixel1 in range(input_h_dim):
    for pixel2 in range(input_w_dim):
        rule_base = copy.deepcopy(RuleBase(number_of_partitions, train=False, trained_rule_base=final_rule_base))
        input_value = input_image[pixel1, pixel2]
        new_value = input_value
        desired_value = blurred_image[pixel1, pixel2]
        new_error = new_value - desired_value
        old_error = 0
        change_in_error = np.random.randint(-10, 10, 1)[0]

        for i in range(20):
            error_rule_membership = data_base.get_rule_and_membership(new_error)
            cr_rule_membership = data_base.get_rule_and_membership(change_in_error)

            # find active rule_numbers:
            active_rules_number_membership = {}
            er_rules, er_memberships = list(error_rule_membership.keys()), list(error_rule_membership.values())
            cr_rules, cr_memberships = list(cr_rule_membership.keys()), list(cr_rule_membership.values())

            for j in range(len(error_rule_membership)):
                for k in range(len(cr_rule_membership)):
                    er_rule, er_membership = er_rules[j], er_memberships[j]
                    cr_rule, cr_membership = cr_rules[k], cr_memberships[k]

                    if er_rule > (number_of_partitions // 2) + 1:
                        er_rule += 1
                    elif er_rule == (number_of_partitions // 2) + 1:
                        er_rule = er_rule + 1 if new_error > 0 else er_rule
                    else:
                        pass

                    active_rules_number_membership[(er_rule, cr_rule)] = min(er_membership, cr_membership)

            # find change in input and update new_value:
            active_rules_number = list(active_rules_number_membership.keys())
            active_rules_membership = list(active_rules_number_membership.values())
            for idx in range(len(active_rules_number_membership)):
                new_value += rule_base.get_change_in_input(active_rules_number[idx], active_rules_membership[idx])

            # update old_error, new_error, change_in_error:
            old_error = new_error
            new_error = new_value - desired_value
            change_in_error = new_error - old_error

        if abs(new_error) > 0.5:
            print(new_error)
            is_converge = False


print(is_converge)