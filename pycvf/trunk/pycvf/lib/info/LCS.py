def lcs_brute(xs, ys):
    '''Return a longest common subsequence of xs and ys.
    
    Example
    >>> lcs("HUMAN", "CHIMPANZEE")
    ['H', 'M', 'A', 'N']
    '''
    if xs and ys:
        xb, xe = xs[:-1], xs[-1]
        yb, ye = ys[:-1], ys[-1]
        if xe == ye:
            return lcs(xb, yb) + [xe]
        else:
            return max(lcs(xs, yb), lcs(xb, ys), key=len)
    else:
        return []

def memoize(fn):
    '''Return a memoized version of the input function.
    
    The returned function caches the results of previous calls.
    Useful if a function call is expensive, and the function 
    is called repeatedly with the same arguments.
    '''
    cache = dict()
    def wrapped(*v):
        key = tuple(v) # tuples are hashable, and can be used as dict keys
        if key not in cache:
            cache[key] = fn(*v)
        return cache[key]
    return wrapped

def lcs_memoize(xs, ys):
    '''Return the longest subsequence common to xs and ys.
    
    Example
    >>> lcs("HUMAN", "CHIMPANZEE")
    ['H', 'M', 'A', 'N']
    '''
    @memoize
    def lcs_(i, j):
        if i and j:
            xe, ye = xs[i-1], ys[j-1]
            if xe == ye:
                return lcs_(i-1, j-1) + [xe]
            else:
                return max(lcs_(i, j-1), lcs_(i-1, j), key=len)
        else:
            return []
    return lcs_(len(xs), len(ys))


from collections import defaultdict, namedtuple
from itertools import product

def lcs_grid(xs, ys):
    '''Create a grid for longest common subsequence calculations.
    
    Returns a grid where grid[(j, i)] is a pair (n, move) such that
    - n is the length of the LCS of prefixes xs[:i], ys[:j]
    - move is \, ^, <, or e, depending on whether the best move
      to (j, i) was diagonal, downwards, or rightwards, or None.
    
    Example:
    T  A  R  O  T
    A 0< 1\ 1< 1< 1<
    R 0< 1^ 2\ 2< 2<
    T 1\ 1< 2^ 2< 3\
    '''
    Cell = namedtuple('Cell', 'length move')
    grid = defaultdict(lambda: Cell(0, 'e'))
    sqs = product(enumerate(ys), enumerate(xs))
    for (j, y), (i, x) in sqs:
        if x == y:
            cell = Cell(grid[(j-1, i-1)].length + 1, '\\')
        else:
            left = grid[(j, i-1)].length
            over = grid[(j-1, i)].length
            if left < over:
                cell = Cell(over, '^')
            else:
                cell = Cell(left, '<')
        grid[(j, i)] = cell
    return grid

def lcs(xs, ys):
    '''Return a longest common subsequence of xs, ys.'''
    # Create the LCS grid, then walk back from the bottom right corner
    grid = lcs_grid(xs, ys)
    i, j = len(xs) - 1, len(ys) - 1
    lcs = list()
    for move in iter(lambda: grid[(j, i)].move, 'e'):
        if move == '\\':
            lcs.append(xs[i])
            i -= 1
            j -= 1
        elif move == '^':
            j -= 1
        elif move == '<':
            i -= 1
    lcs.reverse()
    return lcs

import itertools

def lcs_length(xs, ys):
    '''Return the length of the LCS of xs and ys.
    
    Example:
    >>> lcs_length("HUMAN", "CHIMPANZEE")
    4
    '''
    ny = len(ys)
    curr = list(itertools.repeat(0, 1 + ny))
    for x in xs:
        prev = list(curr)
        for i, y in enumerate(ys):
            if x == y:
                curr[i+1] = prev[i] + 1
            else:
                curr[i+1] = max(curr[i], prev[i+1])
    return curr[ny]



def LCSubstr_len(S, T):
     " longuest common substring (I.E. not subsequence)"
     m = len(S); n = len(T)
     L = [[0] * (n+1) for i in xrange(m+1)]
     lcs = 0
     for i in xrange(m):
         for j in xrange(n):
             if S[i] == T[j]:
                 L[i+1][j+1] = L[i][j] + 1
                 lcs = max(lcs, L[i+1][j+1])
     return lcs
 
def LCSubstr_set(S, T):
     " longuest common substring (I.E. not subsequence)"
     m = len(S); n = len(T)
     L = [[0] * (n+1) for i in xrange(m+1)]
     LCS = set()
     longest = 0
     for i in xrange(m):
         for j in xrange(n):
             if S[i] == T[j]:
                 v = L[i][j] + 1
                 L[i+1][j+1] = v
                 if v > longest:
                     longest = v
                     LCS = set()
                 if v == longest:
                     LCS.add(S[i-v+1:i+1])
     return LCS

edit_distance(xs, ys) == len(xs) + len(ys) - 2 * lcs(xs, ys)
