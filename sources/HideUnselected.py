from tulip import tlp
import tulipplugins
import time, dictmaker

class HideUnrelated(tlp.BooleanAlgorithm):
  TIME_EXEC = False; # used to get algorithm running time in case of performance testing
  SAMPLE_DIFF_NAME = 'isPatient' # Name of the property that will be added to every sample node to differentiate them
  PARAM_MIN_LENGTH = 'Min length'
  PARAM_MAX_LENGTH = 'Max length'
  PARAM_USE_SELECTION = 'Use selected'
  PARAM_AUTO_SUB = 'Auto subgraph'
  
  def __init__(self, context):
    tlp.BooleanAlgorithm.__init__(self, context)
    self.addIntegerParameter(self.PARAM_MIN_LENGTH, "Minimal number of nodes between two of the selected nodes.", '1')
    self.addIntegerParameter(self.PARAM_MAX_LENGTH, "Maximal number of nodes between two of the selected nodes.", '1')
    self.addBooleanParameter(self.PARAM_USE_SELECTION, "Use manually selected nodes as sample data nodes", "False")
    self.addBooleanParameter(self.PARAM_AUTO_SUB, "Automatically creates a subgraph with found paths", "False")
    # you can add parameters to the plugin here through the following syntax
    # self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
    # (see documentation of class tlp.WithParameter to see what types of parameters are supported)
  def check(self):
    # This method is called before applying the algorithm on the input graph.
    # You can perform some precondition checks here.
    # See comments in the run method to know how to access to the input graph.

    # Must return a tuple (boolean, string). First member indicates if the algorithm can be applied
    # and the second one can be used to provide an error message
    if self.dataSet[self.PARAM_MIN_LENGTH] > self.dataSet[self.PARAM_MAX_LENGTH]:
      return (False, "Min length should be less or equal to max length.")
    if self.dataSet[self.PARAM_MIN_LENGTH] < 0 or self.dataSet[self.PARAM_MAX_LENGTH] < 0:
      return (False, "Min length and max length should be greater than 0; a min length of 0 would mean every nodes to be selected")
    if not self.graph.existProperty('isPatient'):
      return (False, "There are no patient node in the selected graph.")
    return (True, "Ok")

  def run(self):
    # This method is the entry point of the algorithm when it is called
    # and must contain its implementation.

    # The graph on which the algorithm is applied can be accessed through
    # the "graph" class attribute (see documentation of class tlp.Graph).

    # The parameters provided by the user are stored in a dictionnary
    # that can be accessed through the "dataSet" class attribute.

    # The result of this selection algorithm must be stored in the
    # boolean property accessible through the "result" class attribute
    # (see documentation to know how to work with graph properties).

    # The method must return a boolean indicating if the algorithm
    # has been successfully applied on the input graph.
    
    # Get patients nodes either through 'isPatient' property added by 'mergeSamples' plugin or through 'viewSelection' which has to be set by the user. 1st solution seems better
    g = self.graph
    start_time = time.time()
    ns = g.nodes()
    patientsNodes = list()
    bool_property = self.SAMPLE_DIFF_NAME
    if self.dataSet[self.PARAM_USE_SELECTION]:
      bool_property = 'viewSelection'
    
    for n in ns:
      if g.getNodePropertiesValues(n)[bool_property]:
        #self.result.setNodeValue(n, True)
        patientsNodes.append(n)
      
    min = self.dataSet[self.PARAM_MIN_LENGTH]
    max = self.dataSet[self.PARAM_MAX_LENGTH]
    self.p_list = patientsNodes
    """
    res = list()
    for p in patientsNodes:
      l = self.applyFilter(p, min, max, 0, [], p)
      res += l
    """
    self.pluginProgress.progress(0, len(patientsNodes))
    for i in xrange(0, len(patientsNodes)):      
      # add progress bar
      self.pluginProgress.progress((i+1), len(patientsNodes))
      for j in xrange(i+1, len(patientsNodes)):
        paths = self.findPathsBetween(patientsNodes[i], patientsNodes[j], min, max, 0, [])
        if not paths == []:
          for p in paths:
            for e in p:
              self.result.setEdgeValue(e, True)
              ends = self.graph.ends(e)
              for n in ends:
                self.result.setNodeValue(n, True)
             
    # Auto subgraph creation if user wants it
    if self.dataSet[self.PARAM_AUTO_SUB]:
      subgraph = self.graph.addSubGraph(self.result)
      subgraph.setName("VisuDNA-subgraph")
    """  
    for e in res:
      self.result.setEdgeValue(e, True)
    """
    # Now we know every patients nodes in the graph
    # To be selected a node has to be directly connected to at least 1 patient node
    # get all edges connected to a node with: graph.allEdges(node). See also graph.existEdge(n1,n2,directed=True) {returns an invalid edge if none are found}
    # es = g.edges()
    # for n in ns:
    #  for p in patientsNodes:
    #    if g.existEdge(p, n, False).isValid():
    #      self.result.setNodeValue(n, True) 
    print(time.time() - start_time)
    return True
    
  def findPathsBetween(self, node_a, node_b, min_length, max_length, length, visited):
    if length > max_length or node_a in visited:
      return []
    e = self.graph.existEdge(node_a, node_b, False)
    if e.isValid(): # return path with length=0
      return [[e]]
      
    visited.append(node_a)
    elist = list()
    neighs = self.graph.getInOutNodes(node_a) # length 1 neighbours
    for n in neighs:
      l = self.findPathsBetween(n, node_b, min_length, max_length, (length+1), visited)
      if not l == []:
#        print "(non-empty) List received from ", n, " to ", node_b, l
        e1 = self.graph.existEdge(node_a, n, False) # we already know there's at least one, no need to Edge.isValid 
        for subl in l:
          if length == 0 and len(subl) < min_length:
              continue            
          subl.append(e1)
          elist.append(subl)
      
    return elist
    
  # @Deprecated
  def applyFilter(self, node, min, max, niv, visited, pStart):
    if node in visited or niv > max:
      return list()

    visited.append(node)
    neighs = self.graph.getInOutNodes(node)
    res_list = list()
    if niv < max:
      for n in neighs:
        l = self.applyFilter(n, min, max, (niv+1), visited, pStart)
        if not l == []:
          res_list += l
          e = self.graph.existEdge(node, n, False)
          res_list.append(e)
    
    if niv >= min and niv <= max:
      for n in neighs:
        for p in self.p_list:
          if not p == pStart and n == p:
            e = self.graph.existEdge(node, n, False)
            res_list.append(e)
          
    return res_list

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("HideUnrelated", "VisuDNA - Select Related", "SB", "13/12/2017", "info", "1.0", "Python")
