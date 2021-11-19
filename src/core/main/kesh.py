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
            maxLength = max(kesh.findLongestChain(leafNode,[]),maxLength)

        return maxLength

    @staticmethod
    def findLongestChain(node , visitedArray):
        connectedNodes = node.getConnectedNodes()
        notVisitedNodes = []
        for connectedNode in connectedNodes:
            if connectedNode not in visitedArray:
                notVisitedNodes.append(connectedNode)

            
            maxLength=0
            
            for notVisitedNode in notVisitedNodes:
                visitedArray.append(notVisitedNode)
                for nvncn in notVisitedNode.getConnectedNodes():
                    maxLength = max(kesh.findLongestChain(nvncn,visitedArray),maxLength)
            return maxLength+1