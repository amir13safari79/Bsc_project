from src.rule_base import RuleBase
from src.data_base import DataBase

import cv2
import numpy as np

# setup original and edge_detected images:
input_image = cv2.imread('images/org_image.jpg', cv2.IMREAD_GRAYSCALE).astype("float")

G_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
x_edge_detected_image = np.zeros((input_image.shape[0], input_image.shape[1]))
for i in range(1, input_image.shape[0] - 1):
    for j in range(1, input_image.shape[1] - 1):
        x_edge_detected_image[i, j] = np.vdot(G_x, input_image[i-1: i+2, j-1: j+2])

cv2.imwrite('images/x_edge_detected_image.jpg', x_edge_detected_image)
x_edge_detected_image_new = cv2.imread('images/x_edge_detected_image.jpg', cv2.IMREAD_GRAYSCALE).astype("float")


# initial 3*3 filter(as input):
edge_filter = np.random.randint(low=-5, high=5, size=(3, 3)).astype("float")

################### start train process ###################
# create rule_base:
number_of_partitions = 11
# initial rule base and database
rule_base = RuleBase(number_of_partitions)
data_base = DataBase((-255, 255), number_of_partitions)

# initial parameters:
output = np.vdot(edge_filter, input_image[0: 3, 0: 3])
error = output - x_edge_detected_image[1, 1]
old_error = 0
change_in_error = error - old_error

# find active rules and their memberships:
er_active_rules_number_membership = data_base.get_rule_and_membership(error)
er_active_rules_number = list(er_active_rules_number_membership.keys())
for i in range(len(er_active_rules_number)):
    if er_active_rules_number[i] > (number_of_partitions // 2) + 1:
        er_active_rules_number[i] += 1
    elif er_active_rules_number[i] == (number_of_partitions // 2) + 1:
        er_active_rules_number[i] = er_active_rules_number[i] + 1 if error > 0 else er_active_rules_number[i]
    else:
        pass
er_active_rules_membership = list(er_active_rules_number_membership.values())

cr_active_rules_number_membership = data_base.get_rule_and_membership(change_in_error)
cr_active_rules_number = list(cr_active_rules_number_membership.keys())
cr_active_rules_membership = list(cr_active_rules_number_membership.values())


for i in range(1, input_image.shape[0] - 1):
    for j in range(1, input_image.shape[1] - 1):
        if (i, j) == (1, 1):
            continue
        else:
            # update then-part of rules:
            for m in range(len(er_active_rules_number)):
                for n in range(len(cr_active_rules_number)):
                    er_cr_rules_number = (er_active_rules_number[m], cr_active_rules_number[n])
                    er_cr_membership = min(er_active_rules_membership[m], cr_active_rules_membership[n])
                    rule_base.update_rules(er_cr_rules_number, er_cr_membership)

            # find change_in_input and update edge_filter:
            change_in_input = 0
            for v in range(len(er_active_rules_number)):
                for w in range(len(cr_active_rules_number)):
                    er_cr_rules_number = (er_active_rules_number[v], cr_active_rules_number[w])
                    er_cr_membership = min(er_active_rules_membership[v], cr_active_rules_membership[w])
                    change_in_input += rule_base.get_change_in_input(er_cr_rules_number, er_cr_membership)

            edge_filter += change_in_input

            # find error and change in error:
            output = np.vdot(edge_filter, input_image[i-1: i+2, j-1: j+2])
            error = output - x_edge_detected_image[i, j]
            change_in_error = error - old_error

            # update old_error:
            old_error = error

            # find active rules and their memberships:
            er_active_rules_number_membership = data_base.get_rule_and_membership(error)
            er_active_rules_number = list(er_active_rules_number_membership.keys())
            for p in range(len(er_active_rules_number)):
                if er_active_rules_number[p] > (number_of_partitions // 2) + 1:
                    er_active_rules_number[p] += 1
                elif er_active_rules_number[p] == (number_of_partitions // 2) + 1:
                    er_active_rules_number[p] = er_active_rules_number[p] + 1 if error > 0 else er_active_rules_number[
                        p]
                else:
                    pass
            er_active_rules_membership = list(er_active_rules_number_membership.values())

            cr_active_rules_number_membership = data_base.get_rule_and_membership(change_in_error)
            cr_active_rules_number = list(cr_active_rules_number_membership.keys())
            cr_active_rules_membership = list(cr_active_rules_number_membership.values())

    print(f"error = {error} and change in error = {change_in_error}")



