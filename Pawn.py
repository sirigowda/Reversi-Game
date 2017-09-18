class Pawn:
    row = -1
    column = -1

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return '[{},{}]'.format(self.row, self.column)

    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column

    def setRowColumn(self, row, column):
        self.row = row
        self.column = column
