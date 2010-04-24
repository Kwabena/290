from numpy import *
from scipy import sparse
from scipy import linalg


def path(n): # edge list of path on n vertices
  e = []
  for i in range(n-1):
    e.append([i, i+1])

  return e


def randGraph(n, m): # generate random graph on n verts with close to m edges
  e = []
  for i in range(m):
    edge = [random.randint(n), random.randint(n)]
    if (edge[0] != edge[1]):
      e.append(edge)

  return e


def edges2adjmat(e): # convert edge list to adjacency matrix
  ea = array(e)
  numverts = ea.max() + 1
  a = sparse.lil_matrix((numverts,numverts))

  for edge in e:
    a[edge[0].__int__(),edge[1].__int__()] = 1
    a[edge[1].__int__(),edge[0].__int__()] = 1

  return a
  
def edges2incmat(e): 
	#convert edge list to signed incidence matrix B(e, v) where 
	#b_ij = -1 if vertex j is the tail of edge i
	#b_ij = +1 if vertex j is the head of edge i
	#b_ij = 0 otherwise
	#if this is correct, we should have B^T * B = L (B_transpose * B = Laplacian)
  ea = array(e)
  numverts = ea.max() + 1
  numedges = ea.size / 2
  a = sparse.lil_matrix((numedges, numverts))
	
  for i in range(numedges):
    edge = e[i]
    a[i, edge[0].__int__()] = -1
    a[i, edge[1].__int__()] = 1
    
  return a
  

def solveResistances(e): #given an edge list, compute the effective resistaces
  b = edges2incmat(e)
  a = edges2adjmat(e)
  l = adjmat2lap(a)
  R = b * linalg.pinv(l.todense()) * b.transpose()
  
  return diag(R)
  
 
def solveResistances2(e): #given edge list, compute effective resistances using 'old' method
  a = edges2adjmat(e)
  l = adjmat2lap(a)
  n = l.shape[0]
  b = zeros(n)
  b[0] = 1
  b[-1] = -1
  ans = sparse.linalg.iterative.cg(l, b)
  x = ans[0]
  
  res = zeros(n - 1)
  for i in range(n - 1):
    res[i] = x[i] - x[i + 1]
    
  return res
  

def adjmat2lap(a): # convert adjacency matrix to a laplacian
  numverts = a.shape[0]
  degrees = a*ones(numverts)
  degmat = sparse.lil_matrix((numverts,numverts))
  degmat.setdiag(degrees)
  lap = degmat - a

  return lap
  

def randMatrix(m, n):  # generate an mxn matrix with entries +/- 1 uniformly distributed
  q = random.uniform(0, 1, (m, n))
  for i in range(m):
    for j in range(n):
      if (q[i, j] < 0.5):
        q[i, j] = -1
      else:
        q[i, j] = +1
        
  return mat(q)
  
  
def reff(M, u, v):  # effective resistance between two vertices, u and v
  diff = M[:,u] - M[:,v]
  res = (linalg.norm(diff)) ** 2
  
  return res

  
def generateData(r, Z, npairs, datafile):  # r = B*Linv, Z = Q*B*Linv
  f = open(datafile, 'w')
  tot_err = 0
  data = []
  k, l = Z.shape
  bucket = range(npairs)
  for n in bucket:
    i, j = [random.randint(0, l - 1), random.randint(0, l - 1)]
    if i != j:  # prevents addition of nan
      real = reff(r, i, j)
      est = reff(Z, i, j) / k
      err = abs(real - est) / real
      tot_err += err
      n = n + 1 # pythonic?
      data.append([i, j, real, est, err])
      f.write("%s %s %s %s %s\n" %(i, j, real, est, err))
      #print i, j, real, est, err
    else:
      bucket.append(n)  #throw something into bucket
      
  f.close()      
  return data

  
def solvePotentials(e, verts, pots): 
  # given edge list e, compute the graph, then
  # set the potentials of verts to pots,
  # and return the resulting potential
  # note that verts are numbered from 0

  a = edges2adjmat(e)
  l = adjmat2lap(a)
  l = l.tocsc()

  n = l.shape[0]

  b = zeros([n,1]) + 0.0


  for i in range(verts.__len__()):
    v = verts[i]
    for j in range(n):
      l[v,j] = 0

    l[v,v] = 1
    b[v] = pots[i]

  ans = linalg.iterative.gmres(l,b)
  x = ans[0]

  return x

