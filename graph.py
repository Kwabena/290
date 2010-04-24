#produce graphs from file listing edges as pairs of vertices i j

def purgeLines(line):
  res = line.rstrip().split(' ')
  
  return res
  
  
def edgeList(filename):
  f = open(filename, 'r')
  lines = f.readlines()
  a = map(purgeLines, lines)
  e = [[int(i), int(j)] for [i, j] in a]

  return e
  
  
def trimGraph(el, n):  #produce a graph with N nodes from edgelist EL
  e = []
  for [i, j] in el:
    if i < n and j < n:
      e.append([i, j])
      
  return e
  
