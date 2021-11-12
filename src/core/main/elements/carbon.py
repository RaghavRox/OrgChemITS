from node import node



class carbon(node):

    __symbol = ("C")

    def __init__(self,connectedNodes) -> None:
        super().__init__(connectedNodes)