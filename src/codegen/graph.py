import pydot


def graph(node):
	edges = descend(node)
	g=pydot.graph_from_edges(edges) 
	g.write_png('graph_from_edges_dot.png', prog='dot') 
	

def descend(node):	
	edges = []
	if type(node) == type("") or type(node) == type(1):
		return []
	
	for i in node.args:
		edges.append((s(node),s(i)))
		edges += descend(i)
	return edges
	
	
def s(node):
	if type(node) == type("") or type(node) == type(1):
		return "%s (%s)" % (node,id(node))
	return "%s (%s)" % (node.type,id(node))
	