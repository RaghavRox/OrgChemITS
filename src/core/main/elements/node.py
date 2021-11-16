class node:

    __connectedNodes = []

    def __init__(self,cords) -> None:
        self.cords = cords


    def setConnectedNodes(self , node):
        if len(self.__connectedNodes) < 4 :
            self.__connectedNodes.append(node)
            return True
        else:
            return False

    def getConnectedNodes(self):
        return self.__connectedNodes