class kesh:
    carbons = ["meth","eth","prop","but","pent","hex","hept","oct","non","dec","undec","dodec"]

    @staticmethod
    def main(nodeList):
        leafNodes =[]
        for node in nodeList:
            if len(node.getConnectedNodes())==1:
                leafNodes.append(node)
        
        leafNodeMaxLengthList = []
        
        for leafNode in leafNodes:
            leafNodeMaxLengthList.append(kesh.findLongestChain(leafNode))

        maxLength = max(leafNodeMaxLengthList)
        ind = 0
        leafNodesWithMaxLength = []
        for l in leafNodeMaxLengthList:
            if l==maxLength:
                leafNodesWithMaxLength.append(leafNodes[ind])
            ind+=1
        

        return leafNodesWithMaxLength

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
    
    @staticmethod
    def findMainChain(fNode , prevNode , lNode):
        if fNode == lNode:
            return [fNode]
        else:
            connectedNodes = fNode.getConnectedNodes()
            if prevNode in connectedNodes:
                connectedNodes.remove(prevNode)
            if len(connectedNodes)!=0:
                for node in connectedNodes:
                    x = kesh.findMainChain(node,fNode,lNode)
                    if len(x)!=0:
                        return x.append(node)
                    else:
                        continue