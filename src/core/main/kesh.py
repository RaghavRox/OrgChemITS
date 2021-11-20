class kesh:
    carbons = ["meth","eth","prop","but","pent","hex","hept","oct","non","dec","undec","dodec"]

    @staticmethod
    def main(nodeList):
        #find leaf nodes
        leafNodes =[]
        for node in nodeList:
            if len(node.getConnectedNodes())==1:
                leafNodes.append(node)
        

        #find the lenght of maximum chain i.e no of nodes in main chain
        leafNodeMaxLengthList = []
        for leafNode in leafNodes:
            leafNodeMaxLengthList.append(kesh.findLongestChainLength(leafNode))
        maxLength = max(leafNodeMaxLengthList)


        #all leaf nodes present in possible main chain list
        ind = 0
        leafNodesWithMaxLength = []
        for l in leafNodeMaxLengthList:
            if l==maxLength:
                leafNodesWithMaxLength.append(leafNodes[ind])
            ind+=1
        

        #find all possible main chains
        i=0
        j=0
        possibleMainChains = []#list of lists
        while i < len(leafNodesWithMaxLength):
            j=i+1
            while j < len(leafNodesWithMaxLength):
                labbe =kesh.findMainChain(leafNodesWithMaxLength[i],None,leafNodesWithMaxLength[j])
                if len(labbe) == maxLength:
                    possibleMainChains.append(labbe)
                j+=1
            i+=1



        return possibleMainChains

    @staticmethod
    def findLongestChainLength(node , prevNode = None):
        shtList = []
        if len(node.getConnectedNodes())==1 and node.getConnectedNodes()[0]==prevNode:
                return 1
        else:
            connectedNodes = node.getConnectedNodes()
            if prevNode in connectedNodes:
                connectedNodes.remove(prevNode)
            for connectedNode in connectedNodes:
                shtList.append(kesh.findLongestChainLength(connectedNode,node))
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
                    if x is not None:
                        if len(x)!=0:
                            x.append(fNode)
                            return x
                    