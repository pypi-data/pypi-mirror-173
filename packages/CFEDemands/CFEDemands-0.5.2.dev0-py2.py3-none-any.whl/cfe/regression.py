#!/usr/bin/env python
# [[file:../Empirics/regression.org::*Outer product of two series][Outer product of two series:1]]
# Tangled on Tue Oct 25 17:14:15 2022
import numpy as np
import pandas as pd

def outer(a,b):
    """
    Outer product of two series.
    """

    if type(a) is pd.DataFrame:
        a = a.squeeze()

    if type(b) is pd.DataFrame:
        b = b.squeeze()

    a = pd.Series(a)
    b = pd.Series(b)

    x = np.outer(a,b)

    try:
        x = pd.DataFrame(x,index=a.index,columns=b.index)
    except AttributeError:
        x = pd.DataFrame(x)

    return x
# Outer product of two series:1 ends here

# [[file:../Empirics/regression.org::*Inner product][Inner product:1]]
# Tangled on Tue Oct 25 17:14:15 2022
def to_series(df):
    """
    Stack a dataframe to make a series.
    """
    try:
        df.columns.names = [n if n is not None else "_%d" % i for i,n in enumerate(df.columns.names)]
    except AttributeError: # Already a series?
        return pd.Series(df)

    for n in df.columns.names:
        df = df.stack(n)

    return df

def inner(a,b,idxout,colsout,fill_value=None,method='sum'):
    """
    Compute inner product of sorts, summing over indices of products which don't appear in idxout or colsout.
    """

    a = to_series(a)
    b = to_series(b)

    if fill_value is not None:
        a = a.astype(pd.SparseDtype(fill_value=fill_value))
        b = b.astype(pd.SparseDtype(fill_value=fill_value))

    idxint = list(set(a.index.names).intersection(b.index.names))
    aonly = list(set(a.index.names).difference(idxint))
    bonly = list(set(b.index.names).difference(idxint))

    if fill_value is None: # Non-sparse
        a = a.replace(0.,np.nan).dropna()
        b = b.replace(0.,np.nan).dropna()

    c = pd.merge(a.reset_index(aonly),b.reset_index(bonly),on=idxint)
    c = c.reset_index().set_index(idxint + aonly + bonly)

    sumover = list(set(aonly+bonly+idxint).difference(idxout+colsout))
    keep = list(set(aonly+bonly+idxint).difference(sumover))

    if fill_value is not None:
        foo = c.sparse.to_coo().tocsr()

        foo = foo[:,0].multiply(foo[:,1])
        foo = pd.DataFrame.sparse.from_spmatrix(foo,index=c.index)
    else:
        foo = c.iloc[:,0]*c.iloc[:,1]

    if method=='sum':
        p = foo.groupby(keep).sum()
    elif method=='mean':
        p = foo.groupby(keep).mean()
    else:
        raise ValueError("No method %s." % method)

    p = p.unstack(colsout)

    if len(idxout)>1:
        p = p.reorder_levels(idxout)

    p = p.sort_index()

    if len(colsout):
        p = p.sort_index(axis=1)

    return p
# Inner product:1 ends here

# [[file:../Empirics/regression.org::*SVD with missing data][SVD with missing data:1]]
# Tangled on Tue Oct 25 17:14:15 2022
import pandas as pd
import numpy as np

def svd_missing(X,gls=False):
    """
    Compute rank one approximation to X.
    """
    def ols(y,x,N=None):

        use = y.index.droplevel(['i','t','m'])

        if N is not None:
            N = N[use]
            x = x[use]*N
            y = y*N

        x = pd.DataFrame(x[use])

        b = np.linalg.lstsq(x,y,rcond=None)[0].squeeze()

        return b

    Sigma = X.cov(ddof=0)
    N = X.count()/X.count().sum()

    s2,u = np.linalg.eigh(Sigma)
    b = pd.Series(u[:,-1]*np.sqrt(s2[-1]),index=Sigma.index)

    y = X.stack().dropna()

    if gls:
        v = y.groupby(['i','t','m']).apply(lambda y,x=b: ols(y,x,N))
    else:
        v = y.groupby(['i','t','m']).apply(lambda y,x=b: ols(y,x))

    scale = np.sqrt(v.T@v)
    u = pd.Series(u[:,-1],index=b.index)

    return u,np.sqrt(s2[-1])*scale,v/scale
# SVD with missing data:1 ends here

# [[file:../Empirics/regression.org::*Angle between vectors (or series)][Angle between vectors (or series):1]]
# Tangled on Tue Oct 25 17:14:15 2022
"""
Compute angle between two vectors, thx to https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
"""
import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
# Angle between vectors (or series):1 ends here

# [[file:../Empirics/regression.org::*OLS][OLS:1]]
# Tangled on Tue Oct 25 17:14:15 2022
def ols(y,x):
    try:
        xcols = x.columns
    except AttributeError:
        xcols = x
        x = y[xcols]
        y = y[y.columns.difference(xcols)]

    y,x = drop_missing([y,x])

    b = np.linalg.lstsq(x,y,rcond=None)[0]

    return pd.Series(b.squeeze(),index=x.columns)
# OLS:1 ends here

# [[file:../Empirics/regression.org::code:Mp][code:Mp]]
# Tangled on Tue Oct 25 17:14:15 2022
import pandas as pd
import numpy as np
from warnings import warn

def Mp(X):
    """
    Construct X-E(X|p) = (I-S(S'S)^{-1}S')X.

    Drop any categorical variables where taking means isn't sensible.
    """
    if len(X.shape) > 1:
        X = X.loc[:,X.dtypes != 'category']
    else:
        if X.dtype == 'category': warn('Taking mean of categorical variable.')

    use = list(set(['t','m','j']).intersection(X.index.names))

    if len(use):
        return X - X.groupby(use).transform(np.mean)
    else:
        return X - X.mean()
# code:Mp ends here

# [[file:../Empirics/regression.org::code:Mpi][code:Mpi]]
# Tangled on Tue Oct 25 17:14:15 2022

def Mpi(X):
    """
    Construct X-E(X|pi).

    Drop any categorical variables where taking means isn't sensible.
    """
    if len(X.shape) > 1:
        X = X.loc[:,X.dtypes != 'category']
    else:
        if X.dtype == 'category': warn('Taking mean of categorical variable.')

    return X - X.groupby(['t','m']).transform(np.mean)
# code:Mpi ends here

# [[file:../Empirics/regression.org::code:kmeans][code:kmeans]]
# Tangled on Tue Oct 25 17:14:15 2022
from sklearn.model_selection import GroupKFold
from .df_utils import use_indices, drop_missing
from scipy.optimize import minimize_scalar
from sklearn.cluster import KMeans

def kmean_controls(n_clusters,Mpy,Mpd,shuffles=0,classifiers=None,verbose=False):
    n_clusters = int(n_clusters)
    Mpd = Mpd.copy()

    km = KMeans(n_clusters=n_clusters,init='k-means++',n_init=10*int(np.ceil(np.sqrt(n_clusters))))
    tau = km.fit_predict(Mpd)

    if classifiers is not None:
        c = classifiers.values.T.tolist()
        Mpd['tau'] = list(zip(*c,tau))
    else:
        Mpd['tau'] = tau

    Mpd['tau'] = Mpd['tau'].astype('category')

    Mpyg = pd.DataFrame(Mpy).join(Mpd['tau'],how='left').groupby(['t','m','tau'])

    MdMpy = Mp(pd.DataFrame(Mpy) - Mpyg.transform(np.mean)).squeeze()

    # Compare real groups with shuffled groups
    if shuffles:
        Valt = []
        for s in range(shuffles):
            Mpd_alt = Mpd.copy()
            Mpd_alt['tau'] = Mpd['tau'].sample(frac=1).reset_index(drop=True).values

            Mpyg_alt = pd.DataFrame(Mpy).join(Mpd_alt['tau'],how='left').groupby(['tau'])

            Valt.append((pd.DataFrame(Mpy) - Mpyg_alt.transform(np.mean)).squeeze().var())

        lr = 2*(np.log(np.mean(Valt)) - np.log(MdMpy.var()))

        if verbose:
            print('K=%d\tLR=%f\tCoeff of variation=%f' % (n_clusters,lr,np.std(Valt)/np.mean(Valt)))

        return lr,MdMpy
    else:
        return Mpd['tau'],MdMpy


# Construct Md operator which goes with k-means clusters tau.
def Md_generator(X,tau,method='categorical',Mp=False):
    """
    Md operator, for either categorical or linear expectations.
    """

    if method=='categorical': # assuming conditioning is on groups tau
        if 'j' in X.index.names:
            if Mp:
                Xg = pd.DataFrame({'X':X}).join(tau,how='left').groupby(['tau','j','t','m'])
            else:
                Xg = pd.DataFrame({'X':X}).join(tau,how='left').groupby(['tau','j'])
        else:
            if Mp:
                Xg = pd.DataFrame({'X':X}).join(tau,how='left').groupby(['tau','t','m'])
            else:
                Xg = pd.DataFrame({'X':X}).join(tau,how='left').groupby(['tau'])

        MdX = X - Xg.transform(np.mean).squeeze()
    elif method=='linear':
        try:
            taucols = tau.columns
            X = pd.DataFrame(X).join(tau,how='outer')
        except AttributeError:  # tau a Series
            taucols = tau

        if 'j' in X.index.names:
            MdX = X.groupby('j').apply(lambda y,x=taucols: Md_generator(y.droplevel('j'),x,method='linear',Mp=Mp)).T
            try:
                MdX = MdX.stack()
            except AttributeError:
                pass

            MdX = MdX.reorder_levels(['i','t','m','j']).sort_index()
        else:
            # Difference out kmeans if tau provided
            ycols = X.columns.difference(taucols)
            xcols = taucols
            if 'tau' in tau and Mp: # kmeans categories provided
                xcols = taucols.drop('tau')
                group = ['tau']
                if Mp:
                    X = X - X.groupby(['tau','t','m']).transform(np.mean)
                else:
                    X = X - X.groupby(['tau']).transform(np.mean)
            else:
                if Mp:
                    X = X - X.groupby(['t','m']).transform(np.mean)
                else:
                    X = X - X.mean()

            y = X[ycols]
            x = X[xcols]
            y,x = drop_missing([y,x])
            x['Constant'] = 1
            b = np.linalg.lstsq(x,y,rcond=None)[0]
            MdX = pd.Series(y.squeeze() - (x@b).squeeze(),index=y.index)
    else: raise ValueError("No method %s." % method)

    return MdX
# code:kmeans ends here

# [[file:../Empirics/regression.org::code:beta_from_MdMpy][code:beta_from_MdMpy]]
# Tangled on Tue Oct 25 17:14:15 2022
from .estimation import svd_rank1_approximation_with_missing_data as mysvd
import numpy as np

def estimate_beta(MdMpy,return_se=False,bootstrap_tol=None,Mdp=None,verbose=False):
    if verbose:
        print("estimate_beta")

    if Mdp:
        MdMpy = Mdp(MdMpy)
    try:
        MdMpY = MdMpy.unstack('j')
    except KeyError:
        MdMpY = MdMpy

    # Estimate beta
    s2,u = np.linalg.eigh(MdMpY.cov(ddof=0))

    assert s2[0]<s2[-1]  # numpy returns eigenvalues in /ascending/ order
    u = u[:,-1]
    s2 = s2[-2]

    if (np.sign(u)<0).mean(): # Fix sign of u.
        u = -u

    b = pd.DataFrame(u*np.sqrt(s2),index=MdMpY.columns,columns=['beta'])

    if return_se:
        if bootstrap_tol is None:
            raise ValueError("Not implemented. Specify bootstrap_tol>0.")
            V = (((e-e.mean())**2).mul(v**2,axis=0)).mean() # See p. 150 of Bai (2003)
            seb = np.sqrt(V)
        else:
            its = 0
            B = pd.DataFrame(index=b.index)
            seb=0
            while its < 30 or np.linalg.norm(seb-last) > bootstrap_tol:
                last = seb
                B[its] = estimate_beta(MdMpY.iloc[np.random.randint(0,MdMpY.shape[0],size=MdMpY.shape[0]),:])[0]
                seb = B.std(axis=1)
                if verbose: print(f"On iteration {its} standard error is {seb}.")
                its += 1
    else:
        seb = None

    return b,seb
# code:beta_from_MdMpy ends here

# [[file:../Empirics/regression.org::*Estimation of \beta and $\M{p}w$][Estimation of \beta and $\M{p}w$:1]]
# Tangled on Tue Oct 25 17:14:15 2022
from scipy import sparse
import warnings

def estimate_beta_and_Mpw(y,Mdp,return_se=False,bootstrap_tol=None,verbose=False):

    MdMpy = Mdp(y)
    try:
        MdMpY = MdMpy.unstack('j')
    except KeyError:
        MdMpY = MdMpy

    if not np.allclose(MdMpy.groupby(['t','m','j']).mean(),0):
        warn("MdMpy means not close to zero.")

    b,seb = estimate_beta(MdMpy,return_se=return_se,bootstrap_tol=bootstrap_tol,verbose=verbose)

    # Construct regression to compute Mpw
    cols = y.groupby(['i','t','m']).mean().index

    # This is VERY SLOW.  Find a better way!
    index = pd.MultiIndex.from_tuples([(i[0],i[1],i[2],j) for i in cols.tolist() for j in b.index.tolist()])

    B = sparse.kron(sparse.eye(len(cols)),b,format='csr')
    B = pd.DataFrame.sparse.from_spmatrix(B,index=index,columns=cols)
    B.index.names = ['i','t','m','j']

    # This is VERY, VERY SLOW!  Find a better way!
    #B = B.loc[y.index,:]
    B = B.reindex(y.index,axis=0)  #Maybe?

    N = y.index.levels[y.index.names.index('i')]

    TM = [(np.nan,t,m) for t in y.index.levels[y.index.names.index('t')] for m in y.index.levels[y.index.names.index('m')]]

    ITM = [(i,t,m) for i in N for t in y.index.levels[y.index.names.index('t')] for m in y.index.levels[y.index.names.index('m')]]

    R = sparse.kron(np.ones((1,len(N))),sparse.eye(len(TM)),format='csr')
    R = pd.DataFrame.sparse.from_spmatrix(R,index=TM,columns=ITM)
    #R = R.loc[:,cols]
    R = R.reindex(cols,axis=1)

    Zeros = pd.DataFrame(np.zeros((len(TM),len(TM))),index=TM,columns=TM)

    # Matrix multiplication too expensive for pd.DataFrame.sparse...
    B = B.sparse.to_coo()
    BB = B.T@B
    BBdf = pd.DataFrame.sparse.from_spmatrix(BB,index=cols,columns=cols)

    zig = pd.concat([BBdf,R.T],axis=1)
    zag = pd.concat([R,Zeros],axis=1)

    zag.index = pd.MultiIndex.from_tuples(zag.index)
    zag.columns = pd.MultiIndex.from_tuples(zag.columns)

    X0 = pd.concat([zig,
                    zag],axis=0)

    y0 = pd.concat([pd.Series(B.T@MdMpy,index=cols),pd.Series(np.zeros(len(TM)),index=TM)],axis=0)

    X0 = X0.sparse.to_coo().tocsc()

    result = sparse.linalg.lsqr(X0,y0,calc_var=False,atol=1e-16,btol=1e-16)


    coeffs = result[0].squeeze()

    Mpw = pd.Series(coeffs[:len(cols)],index=cols)

    mults = pd.Series(coeffs[len(cols):],
                      index=pd.MultiIndex.from_tuples([tm[1:] for tm in TM],names=['t','m']),name='mult')

    scale = Mpw.std(ddof=0)
    Mpw = Mpw/scale
    b = (b*scale).squeeze()

    if return_se: # See Greene-Seaks (1991)
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            # X0inv = sparse.linalg.inv(X0)  # Too expensive!
            # se = np.sqrt(sparse.csr_matrix.diagonal(X0inv))

            # Use partioned matrix inverse to get just se of b
            BB = BB*(scale**2)
            # Note that BB is diagonal
            R = R.sparse.to_coo()
            n = B.shape[1]
            m = R.shape[0]
            Ainv = sparse.spdiags(1/BB.diagonal(),0,n,n)
            V22 = sparse.spdiags(1/(R@Ainv@R.T).diagonal(),0,m,m)
            V11 = Ainv - Ainv@R.T@V22@R@Ainv

            se = np.sqrt(V11.diagonal())

            if 'j' in Mpw.index.names:
                Mpw = Mpw[MdMpy.index]

            e1 = (MdMpy - B@Mpw)
            sigma2 = e1.var(ddof=0)

            se_mult = np.sqrt(V22.diagonal())*sigma2

            seb_alt = pd.Series(se[:len(b)]*sigma2,index=b.index)
            se_mult = pd.Series(se_mult,
                                index=pd.MultiIndex.from_tuples([tm[1:] for tm in TM],
                                                                names=['t','m']),
                                name='se_mult')
    else:
        se_mult = None
        e1 = None

    return b,Mpw,seb,mults,se_mult,e1
# Estimation of \beta and $\M{p}w$:1 ends here

# [[file:../Empirics/regression.org::code:gamma][code:gamma]]
# Tangled on Tue Oct 25 17:14:15 2022
def estimate_gamma(y,beta,w,tau,method='categorical'):
    """
    Estimate $gamma(tau) = E[Mp(Y -hat{beta}hat{w}) | tau]$.
    """

    if beta is not None:
        e = y.unstack('j') - pd.DataFrame({0:w})@pd.DataFrame({0:beta}).T
    else:
        e = y.unstack('j')

    if method=='categorical':
        gamma = Mp(e).join(tau,how='left').groupby('tau').mean()
        gamma.columns.name = 'j'

        # Construct gamma(d)
        gamma_d = pd.DataFrame(tau).join(gamma,on='tau')
        gamma_d.columns.name = 'j'
        gamma_d = gamma_d.drop('tau',axis=1)
        gamma_d = gamma_d.stack()
        gamma_d.name = 'gamma_d'

        e = e.stack('j')
    elif method=='linear':
        e = e.stack('j')
        tau['Constant'] = 1

        foo = pd.DataFrame(e).join(tau,how='outer')

        gamma = foo.groupby('j').apply(lambda y,x=tau.columns: ols(y.droplevel('j'),x))
        if gamma.columns.name is None:
            gamma.columns.name = 'k'

        try:
            gamma_d = (tau*gamma).sum(axis=1).dropna()
        except ValueError:
            gamma_d = (tau@gamma.T).stack()

        gamma_d.name = 'gamma_d'
    else: raise ValueError("No method %s." % method)

    #e2 = e - gamma_d.loc[e.index]
    e2 = e - gamma_d.reindex_like(e)

    return gamma, gamma_d, e2
# code:gamma ends here

# [[file:../Empirics/regression.org::code:Ar_w][code:Ar_w]]
# Tangled on Tue Oct 25 17:14:15 2022
from scipy import sparse
from timeit import default_timer as timer

def estimate_w(y,beta,return_se=False):
    """
    Estimate regression $Y - widehat{gamma(d)}  =  A(r) + hat{beta}w + e$.
    """
    try:
        y0 = y.stack()
    except AttributeError:
        y0 = y

    J = len(beta)

    beta = pd.DataFrame(beta)

    tm = [(t,m) for t in y0.index.levels[1] for m in y0.index.levels[2]]

    if len(y0.shape)==1 and y0.name is None: y0.name = 'y0'

    N = y0.index.levels[0]

    A = sparse.kron(sparse.kron(np.ones((len(N),1)),sparse.eye(len(tm))),np.ones((J,1)),format='csr')

    index = pd.MultiIndex.from_tuples([(i,t,m,j) for i in N for t,m in tm for j in beta.index.tolist()])

    A = pd.DataFrame.sparse.from_spmatrix(A,index=index)
    A.columns = pd.MultiIndex.from_tuples([(t,m) for t,m in tm])
    A.index.names = ['i','t','m','j']
    A.columns.names = ['t','m']

    cols = y0.groupby(['i','t','m']).mean().index

    index = pd.MultiIndex.from_tuples([(i[0],i[1],i[2],j) for i in cols.tolist() for j in beta.index.tolist()])

    B = sparse.kron(sparse.eye(len(cols)),beta,format='csr')
    B = pd.DataFrame.sparse.from_spmatrix(B,index=index,columns=cols)
    B.index.names = ['i','t','m','j']

    A = A.reindex(y0.index,axis=0)
    B = B.reindex(y0.index,axis=0)

    X0 = pd.concat([A,B],axis=1)
    cols = X0.columns

    X0 = X0.sparse.to_coo()

    #start = timer()
    b = sparse.linalg.lsqr(X0,y0,atol=1e-16,btol=1e-16)[0]
    #end = timer()
    #print("Time for lsqr %g" % (end-start,))
    b = pd.Series(b,index=cols)

    e = y0 - X0@b

    eg = e.groupby(['t','m','j'])

    Ar = eg.mean()
    Ar.name = 'Ar'

    Ar_se = eg.std()/np.sqrt(eg.count())

    e3 = e - e.groupby(['t','m','j']).transform(np.mean)

    what = pd.Series(b[len(A.columns):(len(A.columns)+len(B.columns))],index=B.columns)

    return what,Ar,Ar_se,e3
# code:Ar_w ends here

# [[file:../Empirics/regression.org::code:pi][code:pi]]
# Tangled on Tue Oct 25 17:14:15 2022
def estimate_pi(y,b,w,Ar,gamma_d):

    try:
        y0 = y.stack()
    except AttributeError:
        y0 = y.copy()

    wb = outer(w,b).stack()

    e = y0 - Ar - wb - gamma_d

    e = e.dropna()

    pi_g = e.groupby(['t','m'])

    pi = pi_g.mean()
    pi.name = 'pi'

    pi_se = pi_g.std()/np.sqrt(pi_g.count())

    e4 = e - pi
    e4 = e4.reorder_levels(['i','t','m','j']).sort_index()

    return pi, pi_se, e4
# code:pi ends here

# [[file:../Empirics/regression.org::code:predict][code:predict]]
# Tangled on Tue Oct 25 17:14:15 2022
def predict_y(pi,Ar,gamma_d,beta,wr):
    bwr = outer(wr,beta).stack()

    yhat = pi + Ar + gamma_d + bwr

    return yhat.reorder_levels(['i','t','m','j']).sort_index()
# code:predict ends here

# [[file:../Empirics/regression.org::code:data_preparation][code:data_preparation]]
# Tangled on Tue Oct 25 17:14:15 2022
from .df_utils import broadcast_binary_op
from .estimation import drop_columns_wo_covariance
import matplotlib.pyplot as plt
from types import SimpleNamespace

def prepare_data(y,d,min_obs=None):
    assert y.index.names == ['i','t','m','j']

    # Make d a dataframe, with columns k
    if 'k' in d.index.names:
        d = d.unstack('k')

    # Match up rows of d with y
    YD = pd.DataFrame({'y':y}).join(d,how='left')

    YD = YD.dropna()

    y = YD['y']  # Drops expenditures that lack corresponding d

    # Drop goods from y if not enough observations to calculate
    # covariance matrix
    Y = drop_columns_wo_covariance(y.unstack('j'),min_obs=min_obs)

    y = Y.stack('j').dropna()

    # If no variation in d across j, collapse
    dg = YD.iloc[:,1:].groupby(['i','t','m'])
    if dg.std().mean().max()<1e-12:
        d = dg.head(1).droplevel('j') # And vice versa
        assert d.index.names == ['i','t','m']
        d.columns.name='k'

    return y,d

def find_optimal_K(y,d,shuffles=30,verbose=False):
    nstar = int(minimize_scalar(lambda k: -kmean_controls(k,Mp(y),Mp(d),
                                                          shuffles=30,
                                                          classifiers=d.loc[:,d.dtypes == 'category'],
                                                          verbose=verbose)[0],
                                    bracket=[1,20]).x)
    return nstar
# code:data_preparation ends here

# [[file:../Empirics/regression.org::*Construct Missing "correction"][Construct Missing "correction":1]]
# Tangled on Tue Oct 25 17:14:15 2022
def missing_correction(y,d,K=None):
    M = 1-np.isnan(y.unstack('j'))  # Non-missing
    M = M.stack()

    M,d = prepare_data(M,d)

    R =  estimation(M,d,K=K,return_se=False)

    Mhat = predict_y(R['pi'],R['Ar'],R['gamma_d'],R['beta'],R['w'])

    R['M'] = M
    R['Mhat'] = Mhat

    e = M - Mhat
    R['R2'] = 1-e.var()/M.var()

    return e,R
# Construct Missing "correction":1 ends here

# [[file:../Empirics/regression.org::*Construct Missing "correction"][Construct Missing "correction":2]]
# Tangled on Tue Oct 25 17:14:15 2022
def estimation(y,d,K=None,bootstrap_tol=None,return_se=False,rectify=False,verbose=False):

    if K is not None:
        d,MdMpy = kmean_controls(K,Mp(y),Mp(d),classifiers=d.loc[:,d.dtypes == 'category'])
        MdMp = lambda x: Md_generator(x,d,Mp=True)
        Md = lambda x: Md_generator(x,d,Mp=False)
        method = 'categorical'
    else:
        method = 'linear'

        # Change categorical vars to numeric
        cats = d.select_dtypes(['category']).columns
        if len(cats):
            d[cats] = d[cats].apply(lambda x: x.cat.codes)

        MdMp = lambda x: Md_generator(x,d,method=method,Mp=True)
        Md = lambda x: Md_generator(x,d,method=method,Mp=False)

        MdMpy = MdMp(y)

    assert MdMpy.index.names == ['i','t','m','j']

    if not np.all(np.abs(MdMpy.groupby(['j','t','m']).mean()) < 1e-6):
        warn('MdMpy means greater than 1e-6')


    # Estimation
    hatb,hatMpw,seb,mults,se_mults,e1 = estimate_beta_and_Mpw(y,MdMp,return_se=return_se,bootstrap_tol=bootstrap_tol,verbose=verbose)

    hatgamma, gamma_d, e2 = estimate_gamma(Mp(y),hatb,hatMpw,d,method=method)
    try:
        if d.columns.name is None:
            d.columns.name = 'k'
    except AttributeError:
        pass

    # y - hatgamma(d)
    y0 = (Mpi(y) - Mpi(gamma_d)).dropna()

    hatw, Ar, Ar_se, e3 = estimate_w(y0,hatb)
    #print('Ar,w')

    hatpi, pi_se, e4 = estimate_pi(y,hatb,hatw,Ar,gamma_d)

    yhat = predict_y(hatpi,Ar,gamma_d,hatb,hatw)
    e = y - yhat.reindex_like(y)

    sigma2 = e.unstack('j').var()

    R2 = 1 - sigma2/y.unstack('j').var()

    if method=='linear':
        try:
            se_gamma = 1/np.sqrt((d.groupby('j').count()*(d.groupby('j').var() + d.groupby('j').mean()**2)).divide(sigma2,level='j',axis=0))
        except KeyError:  # d doesn't vary with j?
            se_gamma = np.sqrt((outer(sigma2,1/((d.var()+d.mean()**2)*d.count()))))
    else:
        se_gamma = None

    if rectify:
        B,X = validate(y,hatpi,Ar,d,hatw,hatb,hatgamma,GramSchmidt=False)
        # Re-orthogonalize
        hatb = hatb*B['bw']
        if seb is not None:
            seb = seb*B['bw']
        Ar = Ar*B['Ar']
        Ar_se = Ar_se*B['Ar']
        hatpi = hatpi*(B['pi']@y.groupby('j').count()/y.shape[0])
        pi_se = pi_se*(B['pi']@y.groupby('j').count()/y.shape[0])
        try:
            hatgamma = (hatgamma.stack()*B['gamma_d']).unstack('k')
            if se_gamma is not None:
                se_gamma = (se_gamma.stack()*B['gamma_d']).unstack('k')
        except AttributeError:
            hatgamma = hatgamma*B['gamma_d']
            if se_gamma is not None:
                se_gamma = se_gamma*B['gamma_d']
    else:
        B = None
        X = None

    # Convert tuples in index  to strings (necessary for persistence in sql)
    if hatgamma.index.name == 'tau':
        hatgamma.index = [str(s) for s in hatgamma.index]
        hatgamma.index.name = 'k'

    if return_se:
        se_mults = se_mults.unstack('m')
        pi_se = pi_se.unstack('m')
        Ar_se = Ar_se.unstack(['t','m'])
    else:
        se_mults = None
        pi_se = None
        Ar_se = None

    return dict(y=y,
                yhat=yhat,
                mse=(e**2).mean(),
                R2=R2,
                d=d,
                beta=hatb,
                beta_se=seb,
                mults = mults.unstack('m'),
                se_mults = se_mults,
                e1 = e1,
                w = hatw,
                e3 = e3,
                Mpw = hatMpw,
                gamma = hatgamma,
                gamma_se = se_gamma,
                e2 = e2,
                gamma_d = gamma_d,
                pi = hatpi.unstack('m'),
                pi_se = pi_se,
                e4 = e4,
                Ar = Ar.unstack(['t','m']),
                Ar_se = Ar_se,
                B=B,
                X=X)

def validate(y,pi,Ar,d,w,beta,gamma,GramSchmidt=False):
    def ols(x):
        y = x['y']
        x = x.drop('y',axis=1)

        y,x = drop_missing([y,x])

        b = np.linalg.lstsq(x,y,rcond=None)[0]

        return pd.Series(b.squeeze(),index=x.columns)

    X = pd.merge(Ar.reset_index('j'),pi,on=['t','m']).reset_index().set_index(['t','m','j'])

    if gamma.index.name=='tau':
        gamma_d = pd.DataFrame(d).join(gamma,on='tau')
        gamma_d.columns.name = 'j'
        gamma_d = gamma_d.drop('tau',axis=1)
        gamma_d = gamma_d.stack()
    else:
        gamma_d = inner(d,gamma,['i','t','m','j'],[])

    gamma_d.name = 'gamma_d'
    gamma_d = gamma_d[y.index]

    if GramSchmidt:
        gamma_d = Mp(gamma_d)

    if 'j' in gamma_d.index.names:
        X = pd.merge(X,gamma_d.reset_index(['i']),left_on=['t','m','j'],right_on=['t','m','j'],how='outer')
    else:
        X = pd.merge(X.reset_index('j'),gamma_d.reset_index(['i']),left_on=['t','m'],right_on=['t','m'],how='outer')

    X = X.rename(columns={('i',''):'i'}) # Deal with bug in reset_index for sparse matrices?

    X = X.reset_index().set_index(['i','t','m','j'])

    w.name='w'

    bw = outer(w,beta).stack()
    bw.name = 'bw'

    if GramSchmidt:
        MdMp = lambda x: Md_generator(x,d,Mp=True)
        bw = Mp(MdMp(bw))
        bw.name = 'bw'

    X = X.join(bw[y.index])

    X['y'] = y
    X = X.dropna()
    X.columns.name = 'l'

    B = X.groupby('j').apply(lambda x: ols(x))

    return B,X
# Construct Missing "correction":2 ends here

# [[file:../Empirics/regression.org::regression_class][regression_class]]
# Tangled on Tue Oct 25 17:14:15 2022
import numpy as np
import pandas as pd
import warnings
from sqlalchemy import create_engine
from pathlib import Path
from collections import namedtuple, OrderedDict

# Names of Series & DataFrames which are attributes of a Regression object

arrs = {'y':('itmj',),      # Log expenditures, (itm,j)
        'd':('itm','k'),      # Household characteristics (itm,k)
        'alpha':("j",),
        'beta':("j",),   # Frisch elasticities, (j,)
        'gamma':('j','k'),  # Coefficients on characteristics (k,)
        'alpha_se':('j',),
        'beta_se':('j',),
        'gamma_se':('j','k'),
        'w':('itm',),
        'yhat':('itmj',),
        'e':('itmj',),
        'pi':('t','m'),
        'pi_se':('t','m'),
        'R2':('j',),
        'mults':('t','m'),
        'se_mults':('t','m'),
        'e1':('itmj',),
        'e2':('itmj',),
        'e3':('itmj',),
        'e4':('itmj',),
        'Mpw':('itm',),
        'gamma_d':('j','k'),
        'Ar':('j','tm'),
        'Ar_se':('j','tm'),
        'B':('j','l'),
        'X':('itmj','l')
         }

class Regression:
    """
    A class which packages together data and methods for estimating a CFE demand system posed as a regression.

    Data elements (and outputs) are typically pandas Series or DataFrames.  Indexes are kept consistent across objects, with:
       - i :: Indexes households
       - t :: Indexes periods
       - m :: Indexes markets
       - j :: Indexes goods
       - k :: Indexes household characteristics

    Ethan Ligon                               October 2022
    """


    __slots__ = list(arrs.keys()) + ['attrs']

    def __init__(self,
                 correct_miss=False,
                 method='linear',
                 K=None,
                 bootstrap_tol=None,
                 return_se=False,
                 rectify=False,
                 verbose=False,
                 min_obs=30,
                 **kwargs):
        """To load data, use cfe.read_sql().

        To instantiate from data on log expenditures (y) and household
        characteristics (z), supply each as pd.DataFrames, with indices for y
        (i,t,m) and columns (j, and for z indices (i,t,m) and columns (k,).
        """

        for k,v in kwargs.items():
            if k in self.__slots__:
                setattr(self,k,v)

        attrs={}
        attrs['correct_miss'] = correct_miss
        attrs['method'] = method
        attrs['K'] = K
        attrs['bootstrap_tol'] = bootstrap_tol
        attrs['return_se'] = return_se
        attrs['rectify'] = rectify
        attrs['verbose'] = verbose
        attrs['min_obs'] = min_obs

        self.attrs=attrs

        if 'y' in kwargs.keys() and 'd' in kwargs.keys():
            self.y,self.d = prepare_data(self.y,self.d,min_obs=min_obs)

    def mse(self):
        try:
            return (self.y - self.yhat).mean()
        except AttributeError:
            estimate(self)
            return mse(self)

    def optimal_number_of_clusters(self):
        """
        Find optimal number of clusters for K-means.
        """
        self.flags['K'] = find_optimal_K(self.y,self.d)

    def estimate(self):

        R = estimation(self.y,self.d,
                       K=self.attrs['K'],
                       bootstrap_tol=self.attrs['bootstrap_tol'],
                       return_se=self.attrs['return_se'],
                       rectify=self.attrs['rectify'],
                       verbose=self.attrs['verbose'])

        for k,v in R.items():
            try:
                if getattr(self,k) is not None: continue
            except AttributeError:
                setattr(self,k,v)

    def to_sql(self,fn=None,overwrite=False):
        """
        Save to sql database fn.
        """
        if overwrite: if_exists = 'replace'
        else: if_exists = 'fail'

        if fn is not None:
            if not Path(fn).is_absolute():
                fn = str(Path(__file__).absolute().parent.joinpath(fn))
            loc = f'sqlite:///{fn}'
        else:
            loc = f'sqlite://'

        engine = create_engine(loc, echo=False)
        with engine.begin() as connection:
            try:
                for k in arrs.keys():
                    try:
                        x = getattr(self,k)
                        if x is not None:
                            x.to_sql(k,connection,if_exists=if_exists)
                    except AttributeError:
                        continue
                pd.Series(self.attrs).to_sql('attrs',connection,if_exists=if_exists)
            except ValueError:
                raise IOError("To_sql would overwrite existing data.  Pass 'overwrite=True' if this is what you want.") from None

    def to_pickle(self,fn):
        """
        Write dictionary of attributes to a pickle.
        """
        d = {}
        for attr in self.__dir__():
            try:
                x = getattr(self,attr)
                x.shape
                d[attr] = x
            except AttributeError: continue

            d['attrs'] = self.attrs

        pd.to_pickle(d,fn)
# regression_class ends here

# [[file:../Empirics/regression.org::*=read_sql=][=read_sql=:1]]
# Tangled on Tue Oct 25 17:14:15 2022
from sqlalchemy import inspect, create_engine
from ast import literal_eval as make_tuple

def read_sql(fn):
    """
    Read Regression object from file fn.
    """
    if not Path(fn).is_absolute():
        fn = str(Path(__file__).absolute().parent.joinpath(fn))
    loc = f'sqlite:///{fn}'
    engine = create_engine(loc, echo=False)

    inspector = inspect(engine)

    R = {}
    with engine.begin() as connection:
        for t in inspector.get_table_names():
            R[t] = pd.read_sql(t,connection)
            try:
                R[t] = R[t].set_index(list(arrs[t][0])).squeeze()
                if len(R[t].shape)>1: # still a dataframe
                    colnames = []
                    for l in arrs[t][1]:
                        if l not in R[t].columns:
                            colnames.append(l)
                        else:
                            R[t] = R[t].stack(l)
                    if len(colnames)==1: # Just an index
                        R[t].columns.names = colnames
                    else: # Need a multiindex
                        cols = [make_tuple(s) for s in R[t].columns]
                        R[t].columns = pd.MultiIndex.from_tuples(cols,names=colnames)
            except KeyError:
                pass

        if not len(R):
            raise OSError(f'Trying to read empty file?  Check {loc}.')

    return Regression(**R)
# =read_sql=:1 ends here

# [[file:../Empirics/regression.org::*=read_pickle=][=read_pickle=:1]]
# Tangled on Tue Oct 25 17:14:15 2022
import pickle

def read_pickle(fn,cache_dir=None):
    """
    Read pickled dictionary and assign keys as attributes to Regression object.
    """
    import fsspec

    try:
        R = pickle.load(fn)  # Is fn a file?
    except TypeError:  # Maybe a filename?
        if cache_dir is not None:
            if 'filecache::' not in fn:  # May already have caching specified
                fn = 'filecache::' + fn
            storage_options = {'filecache':{'cache_dir':cache_dir}}
            with fsspec.open(fn,mode='rb',
                             storage_options=storage_options) as f:
                R = pickle.load(f)
        else:
            with fsspec.open(fn,mode='rb') as f:
                R = pickle.load(f)

    if type(R) is not dict:
        R = R.__dict__

    return Regression(**R)
# =read_pickle=:1 ends here
