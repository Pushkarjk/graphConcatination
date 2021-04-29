import sys
import os
import os.path
from os import path
f = open("main.txt", "r")

class graph:
    def __init__(self,gdict=None):
        if gdict is None:
            gdict = []
        self.gdict = gdict

# Get the keys of the dictionary
    def getVertices(self):
        return list(self.gdict.keys())
    
    def edges(self):
        return self.findedges()

    def findedges(self):
        edgename = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]:
                if {nxtvrtx, vrtx} not in edgename:
                    edgename.append({vrtx, nxtvrtx})
        return edgename

# Create the dictionary with graph elements

def getNodeElements(node):
	node = node.strip('\n').split(",")

	if node[1]=="epoint" or node[1]=="ret":
		return node[0],[node[1],[] if node[2] == 0 else node[3].split(":")]
	else:
		return node[0],[node[1],node[2], [] if node[3] == 0 else node[4].split(":")]

# Creating a graph

def createGraph(fileName):
	f = open(fileName + ".txt", "r")
	lines = f.readlines()
	graph_elements = {}
	for vertex in lines:
		(key,value) = getNodeElements(vertex,)
		graph_elements[key] = value
		
	return graph_elements

def removeDuplicate(vertexCurr, prevVertices):
	# # prevVertices.append("0x23681c0_1_copy")
	# prevVertices.append("0x23681c0_copy")
	# # prevVertices.append("0x23681c0_1_copy_01")
	# prevVertices.append("0x23681c0_copy_01")
	# vertexCurr = '0x23681c0_1'
	vertArray = vertexCurr.split("_")
	filter_list = [k for k in prevVertices if vertArray[0] in k]
	if(len(filter_list) > 0 and ((len(vertArray) >= 2 and vertArray[1] == "copy") or len(vertArray) == 1 )):
		filter_list = [0 if len(k.split("_")) <= 2 else int(k.split("_")[2]) for k in filter_list if vertArray[0] + '_copy' in k]
		if len(filter_list) >= 1:
			val = max(filter_list) + 1
			if len(vertArray) == 1:
				# print(vertArray[0] + "_copy_" + str(val))
				result = vertArray[0] + "_copy_" + str(val)
			if len(vertArray) >= 2:
				# print(vertArray[0] + "_copy_" + str(val))
				result = vertArray[0] + "_copy_" + str(val)
		else:
			# print(vertArray[0] + "_copy")
			result = vertArray[0] + "_copy"
		
	elif(len(filter_list) > 0 and len(vertArray) >= 2 and vertArray[1] != "copy" and "copy" in vertexCurr):
		filter_list = [0 if len(k.split("_")) <= 3 else int(k.split("_")[3]) for k in filter_list if vertArray[0] + "_" + vertArray[1] + '_copy' in k]
		val = max(filter_list) + 1
		if len(vertArray) >= 3:
			# print(vertArray[0] + "_" + vertArray[1] + "_copy_" + str(val))
			result = vertArray[0] + "_" + vertArray[1] + "_copy_" + str(val)

	elif len(filter_list) == 0:
		result = vertexCurr

	else:
		filter_list = [0 if len(k.split("_")) <= 3 else int(k.split("_")[3]) for k in filter_list if vertexCurr + '_copy' in k]
		if len(filter_list) >= 1:
			val = max(filter_list) + 1
			if len(vertArray) == 1:
				# print(vertArray[0] + "_" + vertArray[1] + "_copy_" + str(val))
				result = vertArray[0] + "_" + vertArray[1] + "_copy_" + str(val)
			if len(vertArray) >= 2:
				# print(vertArray[0] + "_" + vertArray[1] + "_copy_" + str(val))
				result = vertArray[0] + "_" + vertArray[1] + "_copy_" + str(val)
		else:
			# print(vertArray[0] + "_copy")
			result = vertexCurr + "_copy"

	flag = 0 if result == vertexCurr else 1

	return result,flag,vertexCurr


def concatenateGraph(fileName, edges, prevVertices):
	nextGraph = createGraph(fileName)
	temp = {}
	prevVertex = ""
	for vertex in nextGraph:
		vertexCurr,flag,originalVertex = removeDuplicate(vertex, prevVertices)
		val = nextGraph[vertex]
		if prevVertex != "" and flag == 1:
			newEdges = [k for k in temp[prevVertex] if isinstance(k,list)]
			prevValues = [k for k in temp[prevVertex] if not isinstance(k,list)]
			newEdges = [vertexCurr if k == originalVertex else k for k in newEdges[0]]
			prevValues.append(newEdges)
			temp.update({prevVertex:prevValues})
			# newEdges = [vertexCurr if k == originalVertex else k for k in newEdges[0] if]

			# temp.update(concGrp)
			# functionDetected = 1
			# prevVal = temp[prevVertex]
			# updtVal = [prevVal[0],replacePrevVertexEdges(concGrp,prevVal[1],vertex)]
			# temp.update({prevVertex:updtVal})
		if val[0] == 'ret':
			temp[vertexCurr]=[val[0],edges]
		else:
			
			temp[vertexCurr]=nextGraph[vertex]
		prevVertex = vertexCurr

	return temp


def replacePrevVertexEdges(concGraph, prevVal, currNode):
	head = ''
	for vertex in concGraph:
		head = vertex
		break
	temp = []
	for val in prevVal:
		if val == currNode:
			temp.append(head)
		else:
			temp.append(val)
	return temp



def fileCrawl(graphOut):
	functionDetected = 0
	temp = {}
	prevVertex = ""
	for vertex in graphOut:
		val = graphOut[vertex]
		if val[0] == 'funccall' and functionDetected == 0:
			g = graph(temp)
			
			concGrp = concatenateGraph(val[1],val[2],g.getVertices())
			
			# print("if \n")
			# print(concGrp)
			# print("end if \n")

			temp.update(concGrp)
			functionDetected = 1
			prevVal = graphOut[prevVertex]

			if prevVal[0] == 'epoint' or prevVal[0]=="ret":
				updtVal = [prevVal[0],replacePrevVertexEdges(concGrp,prevVal[1],vertex)]
				temp.update({prevVertex:updtVal})
		else:
			temp[vertex]=graphOut[vertex]
		
		prevVertex = vertex

	if functionDetected == 1:
			fileCrawl(temp)
	else:
		result = temp
		writeOutput(result)

def writeOutput(result):
	if(path.exists("result.txt")):
		os.remove("result.txt")
	original_stdout = sys.stdout
	for adjList in result:
		val = result[adjList]
		typeCall = val[0]
		if typeCall == 'epoint' or typeCall == 'ret':
			if result[adjList][1] == ['']:
				leng = 0
			else:
				leng = len(result[adjList][1])
			# print(adjList+','+ result[adjList][0]+ ',' + str(leng) + ',' + ':'.join(result[adjList][1]))
			
			with open('result.txt', 'a+') as f:
			    sys.stdout = f # Change the standard output to the file we created.
			    print(adjList+','+ result[adjList][0]+ ',' + str(leng) + ',' + ':'.join(result[adjList][1]))
			    sys.stdout = original_stdout # Reset the standard output to its original value
		else:
			if result[adjList][2] == ['']:
				leng = 0
			else:
				leng = len(result[adjList][2])
			
			with open('result.txt', 'a+') as f:
			    sys.stdout = f # Change the standard output to the file we created.
			    print(adjList+','+ result[adjList][0]+ ',' + str(result[adjList][1]) + ',' + str(leng) + ',' + ':'.join(result[adjList][2]))
			    sys.stdout = original_stdout # Reset the standard output to its original value

	print('\n')
	

	exit()

def main(mainGraph):
	fileCrawl(mainGraph)
	print(result)

mainGraph = createGraph("main")
main(mainGraph)

result = {}
