"""Tafelmacher: exact classical and proportional constructions.
Generates Figures 2 and 4 as publication-ready PNG files.
Requires numpy and matplotlib. Run: python tafelmacher_figures.py
"""
import numpy as np
import matplotlib.pyplot as plt

# Parameters: h controls triangle height, a half-width of base.
a, h, n = 1.0, 1.0, 8

# Proportional field on R_+
def E(r):
    return np.exp(r)
def padd(x, y):
    return np.asarray(x) * np.asarray(y)
def psub(x, y):
    return np.asarray(x) / np.asarray(y)
def pmul(x, y):
    return np.exp(np.log(x) * np.log(y))
def pdiv(x, y):
    return np.exp(np.log(x) / np.log(y))
def pscalar(r, x):
    return pmul(E(r), x)
def pinterp(u, v, t):
    return padd(pscalar(1-t, u), pscalar(t, v))
def psquare(x):
    return pmul(x, x)

# Classical construction
A = np.array([0., h])
B = np.array([-a, 0.])
C = np.array([a, 0.])
def P(t):
    return (1-t)*A + t*B
def Q(t):
    return t*A + (1-t)*C
def T(t):
    return np.array([a*(1-2*t), 2*h*t*(1-t)])
def parabola(x):
    return (h/2)*(1-(x/a)**2)
def line_y(x, t):
    return (h/a)*(2*t-1)*x + h*(1-2*t+2*t*t)

# Proportional objects are constructed with proportional operations.
Ap, Bp, Cp = E(A), E(B), E(C)
def Pp(t):
    return pinterp(Ap, Bp, t)
def Qp(t):
    return pinterp(Ap, Cp, 1-t)
def Tp(t):
    return E(T(t))
def proportional_parabola(X):
    H, W = E(h), E(a)
    return pmul(pdiv(H, E(2)),
                psub(np.e, pdiv(psquare(X), psquare(W))))
def proportional_line(X, t):
    # Internal proportional affine equation:
    # [E(h(1-2t)) odot X] oplus [E(a) odot Y]
    #   = E(ah(1-2t+2t^2))
    lhs_x = pmul(E(h*(1-2*t)), X)
    rhs = E(a*h*(1-2*t+2*t*t))
    return pdiv(psub(rhs, lhs_x), E(a))

def draw_classical(ax, tangencies=False):
    for U, V in ((A,B),(A,C),(B,C)):
        ax.plot([U[0],V[0]], [U[1],V[1]], color='0.65', lw=1.2)
    x = np.linspace(-a,a,500)
    ax.plot(x, parabola(x), color='black', lw=2.4, label='Parabola')
    ts = [0.18, 0.38, 0.62, 0.82] if tangencies else np.arange(1,2*n)/ (2*n)
    for t in ts:
        p, q = P(t), Q(t)
        ax.plot([p[0],q[0]], [p[1],q[1]], color='tab:blue',
                lw=1.5 if tangencies else 0.8, alpha=.8)
        if tangencies:
            z=T(t)
            ax.scatter([z[0]],[z[1]],color='tab:red',s=25,zorder=5)
    ax.set(xlabel='$x$',ylabel='$y$',title='(a) Ordinary arithmetic',
           xlim=(-1.12*a,1.12*a),ylim=(-.04*h,1.08*h))
    ax.set_aspect('auto')
    ax.grid(alpha=.16)

def draw_proportional(ax, tangencies=False):
    s=np.linspace(0,1,200)
    for U,V in ((Ap,Bp),(Ap,Cp),(Bp,Cp)):
        path=np.array([pinterp(U,V,t) for t in s])
        ax.plot(path[:,0],path[:,1],color='0.65',lw=1.2)
    X=np.linspace(E(-a),E(a),600)
    ax.plot(X,proportional_parabola(X),color='black',lw=2.4)
    ts = [0.18, 0.38, 0.62, 0.82] if tangencies else np.arange(1,2*n)/(2*n)
    for t in ts:
        # Proportional segment joining the division points
        u,v=Pp(t),Qp(t)
        path=np.array([pinterp(u,v,r) for r in s])
        ax.plot(path[:,0],path[:,1],color='tab:blue',
                lw=1.5 if tangencies else .8,alpha=.8)
        if tangencies:
            z=Tp(t)
            ax.scatter([z[0]],[z[1]],color='tab:red',s=25,zorder=5)
    ax.set(xlabel='$X$',ylabel='$Y$',title='(b) Proportional arithmetic',
           xlim=(E(-a)*.91,E(a)*1.04),ylim=(.94,E(h)*1.04))
    ax.grid(alpha=.16)

def save_figure(filename, tangencies):
    fig,axes=plt.subplots(1,2,figsize=(11.5,4.5),layout='constrained')
    draw_classical(axes[0],tangencies)
    draw_proportional(axes[1],tangencies)
    fig.savefig(filename,dpi=300,bbox_inches='tight')
    plt.close(fig)

# Numerical checks: line passes through P,Q; T is on line and parabola.
for t in np.linspace(.05,.95,19):
    p,q,z=P(t),Q(t),T(t)
    for v in (p,q,z):
        assert np.isclose(h*(1-2*t)*v[0]+a*v[1],
                          a*h*(1-2*t+2*t*t),atol=1e-12)
    assert np.isclose(z[1],parabola(z[0]),atol=1e-12)
    zp=Tp(t)
    assert np.isclose(zp[1],proportional_parabola(zp[0]),rtol=1e-12)
    assert np.isclose(zp[1],proportional_line(zp[0],t),rtol=1e-12)
    assert np.allclose(np.log(Pp(t)),P(t),atol=1e-12)
    assert np.allclose(np.log(Qp(t)),Q(t),atol=1e-12)

save_figure("figure2_tafelmacher_PYTHON.png",False)
save_figure("figure4_tangency_PYTHON.png",True)
print("Verified tangencies; generated both figures.")
