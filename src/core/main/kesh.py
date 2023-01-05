class kesh:
    carbons = ["meth", "eth", "prop", "but", "pent", "hex",
               "hept", "oct", "non", "dec", "undec", "dodec"]

    @staticmethod
    def main(nodeLists):
        if len(nodeLists) == 0:
            return "methane"

        # find leaf nodes
        leafNodes = []
        for node in nodeLists:
            if len(node.getConnectedNodes()) == 1:
                leafNodes.append(node)

        # find the lenght of maximum chain i.e no of nodes in main chain
        leafNodeMaxLengthList = []
        for leafNode in leafNodes:
            leafNodeMaxLengthList.append(kesh.findLongestChainLength(leafNode))
        maxLength = max(leafNodeMaxLengthList)

        # all leaf nodes present in possible main chain list
        ind = 0
        leafNodesWithMaxLength = []
        for l in leafNodeMaxLengthList:
            if l == maxLength:
                leafNodesWithMaxLength.append(leafNodes[ind])
            ind += 1

        # find all possible main chains
        i = 0
        j = 0
        possibleMainChains = []  # list of lists
        while i < len(leafNodesWithMaxLength):
            j = i+1
            while j < len(leafNodesWithMaxLength):
                labbe = kesh.findMainChain(
                    leafNodesWithMaxLength[i], None, leafNodesWithMaxLength[j])
                if len(labbe) == maxLength:
                    possibleMainChains.append(labbe)
                j += 1
            i += 1

        mainChain = []
        mainChain = kesh.findOrderOfFinalChain(
            kesh.findFinalMainChain(possibleMainChains))
        # return kesh.findOrderOfFinalChain(kesh.findFinalMainChain(possibleMainChains))
        return kesh.getName(mainChain)

    @staticmethod
    def findLongestChainLength(node, prevNode=None):
        shtList = []
        if len(node.getConnectedNodes()) == 1 and node.getConnectedNodes()[0] == prevNode:
            return 1
        else:
            connectedNodes = node.getConnectedNodes()
            if prevNode in connectedNodes:
                connectedNodes.remove(prevNode)
            for connectedNode in connectedNodes:
                shtList.append(
                    kesh.findLongestChainLength(connectedNode, node))
            return max(shtList)+1

    @staticmethod
    def findMainChain(fNode, prevNode, lNode):
        if fNode == lNode:
            return [fNode]
        else:
            connectedNodes = fNode.getConnectedNodes()
            if prevNode in connectedNodes:
                connectedNodes.remove(prevNode)
            if len(connectedNodes) != 0:
                for node in connectedNodes:
                    x = kesh.findMainChain(node, fNode, lNode)
                    if x is not None:
                        if len(x) != 0:
                            x.append(fNode)
                            return x

    @staticmethod
    def findFinalMainChain(possibleMainChains):
        branches = []
        for chain in possibleMainChains:
            chainLength = 0
            for node in chain:
                chainLength += len(node.getConnectedNodes())
            branches.append(chainLength)

        maxBranches = max(branches)

        for chain in possibleMainChains:
            chainLength = 0
            for node in chain:
                chainLength += len(node.getConnectedNodes())
            if chainLength == maxBranches:
                return chain

    @staticmethod
    def findOrderOfFinalChain(finalChain):
        length = len(finalChain)
        sideChains = []
        x = []
        y = 0
        sum = (0, 0)
        for node in finalChain:
            y += 1
            x = list(set(node.getConnectedNodes()).difference(finalChain))
            if len(x) != 0:
                for i in x:
                    sideChains.append((y, i))
        if len(sideChains) != 0:
            for x in sideChains:
                sum = (sum[0]+x[0], sum[1]+length-x[0]+1)

            if sum[0] > sum[1]:
                return finalChain[::-1]
            if sum[1] > sum[0]:
                return finalChain
            if sum[0] is sum[1]:
                return finalChain
        else:
            return finalChain

    @staticmethod
    def getName(mainchain):
        sideChains = []
        smChain = []
        sideChainsOfSideChains = []
        ln = 0
        y = 0
        num = 0
        name = ""
        smallName = ""
        length = len(mainchain)
        smallName = kesh.carbons[length-1]
        name = name + smallName + "ane"
        for node in mainchain:
            y += 1
            x = list(set(node.getConnectedNodes()).difference(mainchain))
            if len(x) != 0:
                for i in x:
                    sideChains.append((y, i))
                    smallName = kesh.carbons[kesh.findLongestChainLength(
                        i, node)-1] + "yl "
                    # name = str(y) + "-" +smallName + name
                    smChain = kesh.findMainOfSideChain(i, node)
                    for smcnode in smChain:
                        num += 1
                        z = list(set(smcnode.getConnectedNodes()
                                     ).difference(smChain+[node]))
                        # print(len(z),len(smChain))
                        if len(z) != 0:
                            var = len(z)
                            while var > 0:
                                if (var > 0):
                                    ln = kesh.findLongestChainLength(
                                        z[var-1], smcnode) - 1
                                var -= 1

                                smallName = str(
                                    num) + "-" + kesh.carbons[ln] + "yl " + smallName
                    name = str(y) + "-" + smallName + name

        return name

    @staticmethod
    def findMainOfSideChain(node, prevNode):

        mainChainLength = kesh.findLongestChainLength(node, prevNode)
        nodeLists = []
        depth = 0
        msc = []

        def lanja(currentNode, previousNode, depth):
            x = currentNode.getConnectedNodes()
            x.remove(previousNode)
            depth += 1
            if len(x) == 0:
                if depth == mainChainLength:
                    nodeLists.append(currentNode)
                    return None
            else:
                for labbe in x:
                    if (lanja(labbe, currentNode, depth) == None):
                        break

                return None
            depth = depth-1

        lanja(node, prevNode, depth)
        nodeList.append(node)
        msc = kesh.findMainChain(nodeList[1], prevNode, nodeList[0])
        return msc[::-1]
