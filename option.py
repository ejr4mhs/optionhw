# Option Pricing Calculator using Equivalent Portfolio Method
# Evan Rees - April 26, 2023

# Change Variables to Reflect Given Problem

# current stock price
period_0_stock = 420
# strike price of option
strike = 500  
# number of shares that the option controls  
shares_controlled = 100 
# % increase in stock price if stock goes up
up_factor = 0.1
# % decrease in stock price if stock goes down
down_factor = 0.1    
# period in which contract expires
period = 4     
# risk-free rate
rf = 0.05     
# call = 1, put = 0 (or any number != 1)
optionType = 1              

# Program Body

class Node:
    def __init__(self, stock_price):
        self.up = None
        self.down = None
        self.stock = stock_price
        self.option = -1
        self.shares = 0
        self.riskfree = 0

class Tree:
    def __init__(self):
        self.root = Node(period_0_stock)

    def getRoot(self):
        return self.root

    # initialize tree with current stock price and possible prices in next state
    def makeTree(self):
        self.root.up = Node(self.root.stock * (1+up_factor))
        self.root.down = Node(self.root.stock * (1-down_factor))
        cur_period = 1
        self._makeTree(self.root.up, cur_period)
        self._makeTree(self.root.down, cur_period)

    # recursively populate tree with stock prices that reflect % gain/loss in up/down state
    def _makeTree(self, node, cur_period):
        if cur_period is period:
            return
        else:
            node.up = Node(node.stock * (1+up_factor))
            node.down = Node(node.stock * (1-down_factor))
            cur_period += 1
            self._makeTree(node.up, cur_period)
            self._makeTree(node.down, cur_period)

    # calculate the value of the option at each node
    def setEndOptionPrice(self):
        if self.root is not None:
            self._setEndOptionPrice(self.root)
        else:
             return

    # calculate option value in the final state
    def _setEndOptionPrice(self, node):
        if node.up is not None:
            self._setEndOptionPrice(node.up)
            self._setEndOptionPrice(node.down)
        elif optionType == 1:
            node.option = (node.stock - strike)*shares_controlled # call formula
            if node.option < 0:
                node.option = 0
            return
        else:
            node.option = (strike - node.stock)*shares_controlled # put formula
            if node.option < 0:
                node.option = 0
            return
        

    # recursively calculate option value at earlier states
    def findEquivPortfolio(self):
        if self.root is not None:
            self._findEquivPortfolio(self.root)
        else:
            return

    def _findEquivPortfolio(self, node):
        if node.up.option != -1:
            # perform calculation of equivalent portfolio attributes (from BDM 21.1)
            node.shares = (node.up.option - node.down.option)/(node.up.stock - node.down.stock)
            node.riskfree = (node.down.option - (node.down.stock * node.shares))/(1+rf)
            node.option = node.shares * node.stock + node.riskfree 
            return
        else:
            self._findEquivPortfolio(node.up)
            self._findEquivPortfolio(node.down)

    # helper functions
    def deleteTree(self):
        self.root = None

    def printTree(self):
        if self.root is not None:
            self._printTree(self.root)

    def _printTree(self, node):
        if node is not None:
            self._printTree(node.up)
            print(str(node.option), " ", str(node.stock))
            self._printTree(node.down)

# initialize and populate binary tree
tree = Tree()
tree.makeTree()

tree.setEndOptionPrice()

# compute option price
for i in range(period):
    tree.findEquivPortfolio()

# print results
if optionType == 1:
    print("Call price: $", tree.root.option.__round__(2), sep="")
else:
    print("Put price: $", tree.root.option.__round__(2), sep="")

print("Number of Shares in Equivalent Portfolio:", tree.root.shares.__round__(4))
print("Amount invested in risk-free asset:", tree.root.riskfree.__round__(4))
