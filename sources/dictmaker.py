import re

class Maker():
  def __init__(self, graph):
    """
    """
    nodes = graph.nodes()
    self.graph = graph
    self.myDict = dict(zip(map(self.getPSIMIAliases, nodes), nodes)) # dict to each node using tuples as key: {('alias1', 'alias2', ...):<node1>, ...}
    
  def getPSIMIAliases(self, node):
    lAliases = self.graph.getNodePropertiesValues(node)['PSIMI-25.aliases'] # this is a string like: "[abc, def, gddd]"
    lAliases = lAliases[1:] # removes first char ('[')
    splits = re.split(r'\s*,+\s*', lAliases.rstrip(']')) # splits is now a list like: ['abc', 'def', 'gddd']
    return tuple(splits)
    
  def find(self, gene_alias):
    for key in self.myDict:
      if gene_alias in key:
        return self.myDict[key]
    return False
    
  def getDict(self):
    return self.myDict
