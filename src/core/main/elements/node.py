class node:

    def __init__(self,cords) -> None:
        self.__cords = cords
        self.__connectedNodes = []


    def setConnectedNodes(self , node):
        if len(self.__connectedNodes) < 4 :
            self.__connectedNodes.append(node)
            return True
        else:
            return False

    def getConnectedNodes(self):
        connectedNodes = self.__connectedNodes.copy()
        return connectedNodes

    def getCords(self):
        return self.__cords