class kesh:
    carbons = ["meth","eth","prop","but","pent","hex","hept","oct","non","dec","undec","dodec"]

    @staticmethod
    def main(nodeList):
        leafNodes =[]
        for node in nodeList:
            if len(node.getConnectedNodes())==1:
                leafNodes.append(node)
        
        maxLength = 0
        
        for leafNode in leafNodes:
            maxLength = max(kesh.findLongestChain(leafNode),maxLength)

        return maxLength

    @staticmethod
    def findLongestChain(node , prevNode = None):
        shtList = []
        if len(node.getConnectedNodes())==1 and node.getConnectedNodes()[0]==prevNode:
                return 1
        else:
            connectedNodes = node.getConnectedNodes()
            if prevNode in connectedNodes:
                connectedNodes.remove(prevNode)
            for connectedNode in connectedNodes:
                shtList.append(kesh.findLongestChain(connectedNode,node))
            return max(shtList)+1