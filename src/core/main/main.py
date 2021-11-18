from core.main.elements.carbon import carbon
from core.main.elements.node import node
from core.main.kesh import kesh

#GUI calls this function which returns name and description
def mainAlgo(lines):
    nodes = {}
    for line in lines:
        cords1 = (line[0],line[1])
        cords2 = (line[2],line[3])
        nodes[cords1] = carbon(cords1)
        nodes[cords2] = carbon(cords2)


    return nodes[(1,1)]


#takes image and returns image with detected lines and also a list of lines
def detectLines():
    pass
