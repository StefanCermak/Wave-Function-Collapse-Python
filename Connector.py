class ClassConnector:
    def __init__(self, connector):
        self.connector = connector

    def __eq__(self, other):
        return self.connector == other.connector[::-1]

    def __str__(self):
        return self.connector
