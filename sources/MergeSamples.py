# When the plugin development is finished, you can copy the associated Python file 
# to /home/sebastien/.Tulip-5.0/plugins/python
# or /home/sebastien/Downloads/tulip_install_release/lib/tulip/python/
# and it will be automatically loaded at Tulip startup

from tulip import tlp
from tulipgui import tlpgui
import tulipplugins
import csv, time, re
import Tkinter as tkinter
import dictmaker as dm

class MergeSamples(tlp.Algorithm):
  # You can add parameters to the plugin here through the following syntax:
  # self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
  # (see the documentation of class tlp.WithParameter to see what parameter types are supported).
  PARAM_SAMPLE_FILE = 'Samples data'
  PARAM_NODES_COLOR = 'Nodes color'
  PARAM_EDGES_COLOR = 'Edges color'
  PARAM_DEBUG = 'Debug mode'
  TIME_EXEC = False; # used to get algorithm running time in case of performance testing
  EDGE_TYPE_COL = "PSIMI-25.interaction type"; # The name of the column in edges where the connection type between a sample node and a gene will be written
  
  def __init__(self, context):
    tlp.Algorithm.__init__(self, context)
    self.addFileParameter(self.PARAM_SAMPLE_FILE, True, "Path to the TSV data file")
    self.addColorParameter(self.PARAM_NODES_COLOR, "The color that will be used for the newly created nodes", "(255,0,0,255)")
    self.addColorParameter(self.PARAM_EDGES_COLOR, "The color that will be used for the newly created edges", "(180,180,180,255)")
    # self.addStringParameter('Nodes size', "The size of the newly created nodes", "(1,1,1)")
    self.addBooleanParameter(self.PARAM_DEBUG, "Show debug infos", "false")

  # This method is called before applying the algorithm on the input graph.
  # You can perform some precondition checks here.
  # See comments in the run method to know how to have access to the input graph.
  # Must return a tuple (Boolean, string). First member indicates if the algorithm can be applied
  # and the second one can be used to provide an error message.
  def check(self):
    if self.dataSet[self.PARAM_SAMPLE_FILE] == "":
      return (False, "Filepath is empty")
    return (True, "")
    
 
  # This method is the entry point of the algorithm when it is called
  # and must contain its implementation.
  # The graph on which the algorithm is applied can be accessed through
  # the "graph" class attribute (see documentation of class tlp.Graph).
  # The parameters provided by the user are stored in a dictionnary
  # that can be accessed through the "dataSet" class attribute.
  # The method must return a boolean indicating if the algorithm
  # has been successfully applied on the input graph.
  def run(self):
    
    if self.dataSet[self.PARAM_DEBUG]:
      top = tkinter.Tk()
      text = tkinter.Text(top)
      text.insert(tkinter.INSERT, "Hello...")
      text.pack()
      top.mainloop() # Do this in new thread
          
    """
    self.prompt = tkinter.Label(self, text="Test", anchor="w")
    self.entry = tkinter.Entry(self)
    self.submit = tkinter.Button(self, text="submit", command=self.test)
    self.output = tkinter.Label(self, text="asdf")
    
    self.prompt.pack(side="top", fill="x")
    self.entry.pack(side="top", fill="x")
    self.output.pack(side="top", fill="x", expand=True)
    self.submit.pack(side="right")
    """
    
    try:
      tsvfile = open(self.dataSet['Samples data'], 'rb')
    except IOError:
      self.printerr("The provided filepath could not be opened");
      return 0
    print('file open')
          
    if (self.TIME_EXEC): start_time = time.time()
    nodesC = self.getUserColor(self.PARAM_NODES_COLOR)
    edgesC = self.getUserColor(self.PARAM_EDGES_COLOR)
    createParams = {"nodesColor":nodesC, "nodesSize":"", "edgesColor":edgesC, "edgesSize":""}
    
    #fieldNames = ['gene_name', 'gene_id', 'Parental', 'L1', 'L2', 'L3', ...]
    fieldnames = re.split(r'\t+', tsvfile.readline().rstrip('\t\n'))
    rows = self.parseLinesTSV(tsvfile, fieldnames)
    if rows == False:
      return 0
    self.createNodes(rows, fieldnames, createParams)
    if (self.TIME_EXEC): print(time.time() - start_time)
    return True
  
    
  def create_node(self, node, nodeName, userParams):
      nColor = userParams['nodesColor']
      eColor = userParams['edgesColor']
      params = dict.fromkeys(["viewLabel", "name", "sharedName"], nodeName)
      params["viewColor"] = nColor
      params["viewSize"] = tlp.Vec3f(1,1,1)
      params["viewLayout"] = userParams['coords']
      params["isPatient"] = True
      new_node = self.graph.addNode(params)
      return new_node 
      
   # Returns a list of lines after the file has been parse as a TSV file according to the fieldnames.
  def parseLinesTSV(self, tsvfile, fieldnames):
    try:
      firstLine = tsvfile.readline() # First line contains field names
      fieldNames = re.split(r'\t+', firstLine.rstrip('\t\n'))
      # print len(filedNames)
      dictread = csv.DictReader(tsvfile, fieldnames=fieldnames, dialect='excel-tab')
      rows = list(dictread)
      return rows
    except Exception:
      printerr("The provided file could not be parsed, it's probably not a TSV file")
      return False
    
  def findNodeInDict(self, gene_id, hashDict):
    for key in hashDict:
      if gene_id in key:
        return hashDict[key]
    return False
      
  def createNodes(self, rows, fieldnames, createParams):
    """
    Create a new node for each patient in the provided data file and add an edge to every different node (gene).
    @param rows: a list containing each row of the samples data file (without first row)
    @param fieldnames: a list containing the name of columns for each row in rows; fieldnames=['gene_name', 'gene_id', 'Patient1', 'Patient2', ..., 'PatientN']
    @param createParams: parameters used for the creation of new nodes and edges; createParams.keys=["nodesColor", "edgesColor"]
    """
    ns = self.graph.nodes()
    dmdict = dm.Maker(self.graph)
    rlen = len(rows)
    createParams['coords'] = tlp.Vec3f(0,0,0)
    addedNodes = dict()
    for i, row in enumerate(rows):
      rid = row[fieldnames[1]] # fieldnames[1] should be 'gene_id'
      node = dmdict.find(rid)
      if node == False:
        continue;
      for num in xrange(2, len(fieldnames)):
        patient = fieldnames[num]
        if row[patient] == '':
          continue
        if not patient in addedNodes:
          addedNodes[patient] = self.create_node(node, patient, createParams)
          createParams['coords'] -= tlp.Vec3f(10,0,0)
        edge = self.graph.addEdge(addedNodes[patient], node, {self.EDGE_TYPE_COL:row[patient], "viewColor":createParams['edgesColor']})
      self.pluginProgress.progress(i, rlen) 
    if self.pluginProgress.state() == tlp.TLP_CANCEL:
      self.graph.delNodes(addedNodes.values(), True)
    return 0;
  
  def getUserColor(self, param):
    try:
      c = self.dataSet[param]
      color = tlp.Color(c.getR(),c.getG(),c.getB(),c.getA())
      return color
    except Exception:
      return tlp.Color(0,0,0,255);
    
  def printerr(self, message):
    self.pluginProgress.setError(message)
    return True
  
 
# The line below does the magic to register the plugin into the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("MergeSamples", "VisuDNA - Merge Samples", "SB", "27/11/2017", "", "1.0")
