import re

class Maker():
  ALIASES_COL_NAME = 'PSIMI-25.aliases' # Name of the column where the aliases are stored
  
  def __init__(self, graph):
    """
    """
    nodes = graph.nodes()
    self.graph = graph
    self.myDict = dict(zip(map(self.getPSIMIAliases, nodes), nodes)) # dict to each node using tuples as key: {('alias1', 'alias2', ...):<node1>, ...}
    
  def getPSIMIAliases(self, node):
    lAliases = self.graph.getNodePropertiesValues(node)[self.ALIASES_COL_NAME] # this is a string like: "[abc, def, gddd]"
    lAliases = lAliases[1:] # removes first char ('[')
    splits = re.split(r'\s*,+\s*', lAliases.rstrip(']')) # splits is now a list like: ['abc', 'def', 'gddd']
    # Finding gene's name in splits to display it in its viewLabel
    r = re.compile('AT\dG\d*')
    names = filter(r.search, splits)
    if len(names) > 0: 
      self.graph.setNodePropertiesValues(node, {'viewLabel': names[0]})
    return tuple(splits)
    
  def find(self, gene_alias):
    for key in self.myDict:
      if gene_alias in key:
        return self.myDict[key]
    return False
    
  def getDict(self):
    return self.myDict
