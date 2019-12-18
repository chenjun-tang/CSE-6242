from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        # self.tree = []
        self.tree = {}
        # pass

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        # pass
        self.group = None
        self.depth = 0
        max_info_gain = -float("inf")
        split_attribute = -1
        x_l, x_r, y_l, y_r = [], [], [], []

        if self.depth < 15 and entropy(y) > 0:           

            for col in range(len(X[0])):
                values = [row[col] for row in X]
                cur_split_val = sum(values)/len(values)            

                X_left, X_right, y_left, y_right = partition_classes(X, y, col, cur_split_val)
                cur_y = [y_left, y_right]
                cur_info_gain = information_gain(y, cur_y)
                if max_info_gain < cur_info_gain:
                    max_info_gain = cur_info_gain
                    x_l, x_r, y_l, y_r = X_left, X_right, y_left, y_right
                    split_attribute = col
                    split_val = cur_split_val

            self.tree['left'], self.tree['right'] = DecisionTree(), DecisionTree()
            self.tree['split_attribute'] = split_attribute
            self.tree['split_val'] = split_val
            self.tree['left'].learn(x_l, y_l)
            self.tree['right'].learn(x_r, y_r)
            self.tree['left'].depth = self.depth + 1
            self.tree['right'].depth = self.depth + 1

        else:
            self.group = y[0]
            return

            


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        node = self.tree
        while self.group == None:
            split_val = node['split_val']
            split_attribute = node['split_attribute']

            if isinstance(record[split_attribute], str):
                if record[split_attribute] == split_val:
                    label = node['left'].classify(record)
                else:
                    label = node['right'].classify(record)
            else:
                if record[split_attribute] <= split_val:
                    label = node['left'].classify(record)
                else:
                    label = node['right'].classify(record)
            return label

        label = self.group
        return label
