#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 17:26:02 2019

@author: binggu
"""

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, kron, identity, linalg

from pyqed.units import au2fs, au2k, au2ev
from pyqed import dag, coth, ket2dm, comm, anticomm, sigmax, sort
from pyqed.optics import Pulse
from pyqed.wpd import SPO2
# from pyqed.cavity import Cavity

import proplot as plt




def ham_ho(freq, n, ZPE=False):
    """
    input:
        freq: fundemental frequency in units of Energy
        n : size of matrix
    output:
        h: hamiltonian of the harmonic oscilator
    """

    if ZPE:
        energy = np.arange(n + 0.5) * freq
    else:
        energy = np.arange(n) * freq

    return np.diagflat(energy)


# class Mol:
#     def __init__(self, ham, dip, rho=None):
#         self.ham = ham
#         #self.initial_state = psi
#         self.dm = rho
#         self.dip = dip
#         self.n_states = ham.shape[0]
#         self.ex = np.tril(dip.toarray())
#         self.deex = np.triu(dip.toarray())
#         self.idm = identity(ham.shape[0])
#         self.size = ham.shape[0]

#     def set_dip(self, dip):
#         self.dip = dip
#         return

#     def set_dipole(self, dip):
#         self.dip = dip
#         return

#     def get_ham(self):
#         return self.ham

#     def get_dip(self):
#         return self.dip

#     def get_dm(self):
#         return self.dm


def fft(t, x, freq=np.linspace(0,0.1)):

    t = t/au2fs

    dt = (t[1] - t[0]).real

    sp = np.zeros(len(freq), dtype=np.complex128)

    for i in range(len(freq)):
        sp[i] = x.dot(np.exp(1j * freq[i] * t - 0.002*t)) * dt

    return sp


def obs(A, rho):
    """
    compute observables
    """
    return A.dot( rho).diagonal().sum()

# def rk4_step(a, fun, dt, *args):

#     dt2 = dt/2.0

#     k1 = fun(a, *args)
#     k2 = fun(a + k1*dt2, *args)
#     k3 = fun(a + k2*dt2, *args)
#     k4 = fun(a + k3*dt, *args)

#     a += (k1 + 2*k2 + 2*k3 + k4)/6. * dt
#     return a

# def comm(a,b):
#     return a.dot(b) - b.dot(a)

# def anticomm(a,b):
#     return a.dot(b) + b.dot(a)


# class Pulse:
#     def __init__(self, delay, sigma, omegac, amplitude=0.01, cep=0.):
#         """
#         Gaussian pulse exp(-(t-T)^2/2 * sigma^2)
#         """
#         self.delay = delay
#         self.sigma = sigma
#         self.omegac = omegac # central frequency
#         self.unit = 'au'
#         self.amplitude = amplitude
#         self.cep = cep

#     def envelop(self, t):
#         return np.exp(-(t-self.delay)**2/2./self.sigma**2)

#     def spectrum(self, omega):
#         omegac = self.omegac
#         sigma = self.sigma
#         return sigma * np.sqrt(2.*np.pi) * np.exp(-(omega-omegac)**2 * sigma**2/2.)

#     def field(self, t):
#         '''
#         electric field
#         '''
#         omegac = self.omegac
#         delay = self.delay
#         a = self.amplitude
#         sigma = self.sigma
#         return a * np.exp(-(t-delay)**2/2./sigma**2)*np.cos(omegac * (t-delay))


class Cavity():
    def __init__(self, freq, n_cav):
        self.freq = self.omega = freq
        self.resonance = freq
        self.ncav = self.n_cav = n_cav
        self.n = n_cav

        self.idm = identity(n_cav)
        # self.create = self.get_create()

        # self.a = self.get_annihilate()
        self.hamiltonian = self.get_ham()

#    @property
#    def hamiltonian(self):
#        return self._hamiltonian
#
#    @hamiltonian.setter
#    def hamiltonian(self):
#        self._hamiltonian = ham_ho(self.resonance, self.n)

    def get_ham(self, zpe=False):
        return ham_ho(self.freq, self.n_cav)

    def create(self):
        n_cav = self.n_cav
        c = lil_matrix((n_cav, n_cav))
        c.setdiag(np.sqrt(np.arange(1, n_cav)), -1)
        return c.tocsr()

    def annihilate(self):
        n_cav = self.n_cav
        a = lil_matrix((n_cav, n_cav))
        a.setdiag(np.sqrt(np.arange(1, n_cav)), 1)

        return a.tocsr()

    def get_dm(self):
        """
        get initial density matrix for cavity
        """
        vac = np.zeros(self.n_cav)
        vac[0] = 1.
        return ket2dm(vac)

    def get_num(self):
        """
        number operator
        """
        ncav = self.n_cav
        a = lil_matrix((ncav, ncav))
        a.setdiag(range(ncav), 0)
        return a.tocsr()





class Polariton:
    def __init__(self, mol, cav, g):
        self.g = g
        self.mol = mol
        self.cav = cav
        self._ham = None
        self.dip = None
        self.cav_leak = None
        #self.dm = kron(mol.dm, cav.get_dm())

    def getH(self, RWA=True):
        mol = self.mol
        cav = self.cav

        g = self.g

        hmol = mol.get_ham()
        hcav = cav.get_ham()

        Icav = identity(self.cav.n_cav)
        Imol = identity(self.mol.n_states)

        if RWA == True:
            hint = g * (kron(mol.ex, cav.get_annihilate()) + kron(mol.deex, cav.get_create()))
        elif RWA == False:
            hint = g * kron(mol.dip, cav.get_create() + cav.get_annihilate())

        return kron(hmol, Icav) + kron(Imol, hcav) + hint

    def get_ham(self, RWA=False):
        print('Deprecated. Please use getH()')
        return

    def get_dip(self):
        return kron(self.mol.dip, self.cav.idm)

    def get_dm(self):
        return kron(self.mol.dm, self.cav.vacuum_dm())

    def get_cav_leak(self):
        """
        damp operator for the cavity mode
        """
        if self.cav_leak == None:
            self.cav_leak = kron(self.mol.idm, self.cav.annihilate)

        return self.cav_leak

    def spectrum(self, nstates, RWA=False):
        """
        compute the polaritonic spectrum
        """
        ham = self.get_ham(RWA=RWA)
        ham = csr_matrix(ham)
        return linalg.eigsh(ham, nstates, which='SA')

    def rdm_photon(self):
        """
        return the reduced density matrix for the photons
        """


class VibronicPolariton:
    """
    a 1D vibronic model coupled to a single-mode cavity
    """
    # def __init__(self, x, y, masses, nstates=2, coords='linear', G=None, abc=False):

    #     super.__init__(x, y, masses, nstates, coords, G, abc)

    def __init__(self, mol, cav):

        self.mol = mol
        self.cav = cav
        self.x = mol.x
        self.nx = mol.nx

        self.nstates = mol.nstates * cav.ncav # number of polariton states

        self.v = None
        self.va = None

    # def build(self):
    #     mol = self.mol
    #     cav = self.cav

    #     nx = mol.nx
    #     nstates = mol.states

    #     nc = cav.nx
    #     v = np.zeros((nx, nc, nstates))

    #     for n in range(nc):
    #         v[:, n, :] = mol.v

    def dpes(self, g, rwa=False):

        # if rwa == False:
        #     raise NotImplementedError('Counterrotating terms are not included yet.\
        #                               Please contact Bing Gu to add.')

        mol = self.mol
        cav = self.cav

        omegac = cav.omega
        nx = mol.nx
        nel = mol.nstates
        ncav = cav.ncav

        nstates = self.nstates

        v = np.zeros((nx, nstates, nstates), dtype=complex)


        for j in range(nstates):
            a, n = np.unravel_index(j, (nel, ncav))
            v[:, j, j] = mol.v[:, a, a] + n * omegac


        # cavity-molecule coupling
        a = cav.annihilate()
        # for i in range(nx):
        #     v[i, :, :] += g * kron(mol.edip, a + dag(a))

        v += np.tile(g * kron(mol.edip, a + dag(a)).toarray(), (nx, 1, 1))

        self.v = v
        return v

    def ppes(self):

        E = np.zeros((self.nx, self.nstates))
        for i in range(self.nx):
            V = self.v[i, :, :]
            w, u = sort(*np.linalg.eigh(V))
            # E, U = sort(E, U)
            E[i, :] = w

        self.va = E
        return E

    def ground_state(self, rwa=False):
        if rwa:
            v = self.mol.v[:, 0, 0]
        else:
            # construct the ground-state polaritonic PES
            v = self.va[:, 0, 0]

        # DVR
        from pyqed.dvr.dvr_1d import SincDVR
        L = self.x.max() - self.x.min()
        dvr = SincDVR(128, L)


    def draw_surfaces(self, n=None, representation='diabatic'):
        if self.v is None:
            raise ValueError('Call dpes() first.')

        if n is None:
            n = self.nstates

        if representation == 'diabatic':
            v = self.v

            fig, ax = plt.subplots()
            for j in range(n):
                ax.plot(self.x, v[:, j,j].real)

            fig, ax = plt.subplots()
            for j in range(n):
                for i in range(j):
                    ax.plot(self.x, v[:, i, j].real)

        elif representation == 'adiabatic':
            v = self.va

            fig, ax = plt.subplots()
            for j in range(n):
                ax.plot(self.x, v[:, j].real)

        return

    def run(self, psi0, dt, Nt=1, t0=0, nout=1):

        from pyqed.wpd import SPO

        spo = SPO(self.x, mass=self.mol.mass, ns=self.nstates)
        return spo.run(psi0=psi0, dt=dt, Nt=Nt, t0=t0, nout=nout)




class VibronicPolariton2:
    """
    2D vibronic model in the diabatic representation coupled to
    a single-mode cavity

    """
    def __init__(self, mol, cav):
        self.mol = mol
        self.cav = cav
        self.x, self.y = mol.x, mol.y
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.nx, self.ny = mol.nx, mol.ny
        self.nel = self.mol.nstates
        self.ncav = self.cav.ncav
        self.nstates = self.nel * self.ncav


        self.v = None
        self.va = None # adiabatic polaritonic PES
        self._transformation = None # diabatic to adiabatic transformation matrix
        self._ground_state = None

    def ground_state(self, representation='adiabatic'):
        # if rwa:
        #     return self.mol.ground_state()
        # else:
        #     # construct the ground-state polaritonic PES

        from pyqed.dvr.dvr_2d import DVR2

        x = self.x
        y = self.y

        if self.va is None:
            self.ppes()

        dvr = DVR2(x, y, mass=self.mol.mass) # for normal coordinates

        if representation == 'adiabatic':
            V = self.va[:, :, 0]
        elif representation == 'diabatic':
            V = self.v[:, :, 0, 0]

        E0, U = dvr.run(V, k=1)

        self._ground_state = U[:, 0].reshape(self.nx, self.ny)

        return E0, self._ground_state


    def dpes(self, g, rwa=False):
        """
        Compute the diabatic potential energy surfaces

        Parameters
        ----------
        g : TYPE
            DESCRIPTION.
        rwa : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        v : TYPE
            DESCRIPTION.

        """
        mol = self.mol
        cav = self.cav

        omegac = cav.omega

        nx, ny = self.nx, self.ny

        nel = mol.nstates
        ncav = cav.ncav

        nstates = self.nstates # polariton states

        v = np.zeros((nx, ny, nstates, nstates))

        for j in range(nstates):
            a, n = np.unravel_index(j, (nel, ncav))
            v[:, :, j, j] = mol.v[:, :, a, a] + n * omegac


        # cavity-molecule coupling
        a = cav.annihilate()

        v += np.tile(g * kron(mol.edip.real, a + dag(a)).toarray(), (nx, ny, 1, 1))

        self.v = v

        return v

    def ppes(self, return_transformation=False):
        """
        Compute the polaritonic potential energy surfaces by diagonalization

        Parameters
        ----------
        return_transformation : TYPE, optional
            Return transformation matrices. The default is False.

        Returns
        -------
        E : TYPE
            DESCRIPTION.

        """

        nx = self.nx
        ny = self.ny
        N = self.nstates

        E = np.zeros((self.nx, self.ny, self.nstates))

        if not return_transformation:

            for i in range(self.nx):
                for j in range(self.ny):
                    V = self.v[i, j, :, :]
                    w = np.linalg.eigvalsh(V)
                    # E, U = sort(E, U)
                    E[i, j, :] = w
        else:

            T = np.zeros((nx, ny, N, N), dtype=complex)

            for i in range(self.nx):
                for j in range(self.ny):
                    V = self.v[i, j, :, :]
                    w, u = sort(*np.linalg.eigh(V))

                    E[i, j, :] = w
                    T[i, j, :, :] = u

            self._transformation = T

        self.va = E

        return E

    def berry_curvature(self, state_id):
        # compute Berry curvature from the A2D transformation matrix
        pass

    def run(self, psi0=None, dt=0.1, Nt=10, t0=0, nout=1):

        if psi0 is None:
            psi0 = np.zeros((self.nx, self.ny, self.nstates))
            psi0[:, :, 0] = self._ground_state

        spo = SPO2(self.x, self.y, mass=self.mol.mass, nstates=self.nstates)
        spo.V = self.v

        return spo.run(psi0=psi0, dt=dt, Nt=Nt, t0=t0, nout=nout)


    def plot_surface(self, state_id=0, representation='adiabatic'):
        from pyqed.style import plot_surface

        if representation == 'adiabatic':
            plot_surface(self.x, self.y, self.va[:, :, state_id])
        else:
            plot_surface(self.x, self.y, self.v[:, :, state_id, state_id])
            
        return

    def plot_wavepacket(self, psilist, **kwargs):

        if not isinstance(psilist, list): psilist = [psilist]


        for i, psi in enumerate(psilist):
            fig, (ax0, ax1) = plt.subplots(nrows=2, sharey=True)

            ax0.contour(self.X, self.Y, np.abs(psi[:,:, 1])**2)
            ax1.contour(self.X, self.Y, np.abs(psi[:, :,0])**2)
            ax0.format(**kwargs)
            ax1.format(**kwargs)
            fig.savefig('psi'+str(i)+'.pdf')
        return ax0, ax1

    def plot_ground_state(self, **kwargs):


        fig, ax = plt.subplots()

        ax.contour(self.X, self.Y, np.real(self._ground_state))
        ax.format(**kwargs)

        fig.savefig('ground_state.pdf')
        return ax

    def promote_op(self, a, kind='mol'):
        """
        promote a local operator to the composite polariton space

        Parameters
        ----------
        a : TYPE
            DESCRIPTION.
        kind : TYPE, optional
            DESCRIPTION. The default is 'mol'.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if kind in ['mol', 'm']:

            return kron(a, self.cav.idm)

        elif kind in ['cav', 'c']:

            return kron(self.mol.idm, a)




class DHO:
    def __init__(self, x, nstates=2):
        self.x = x
        self.nx = len(x)
        self.nstates = nstates

        self.v = None
        self.edip = sigmax()

    def dpes(self, d=1, E0=1.):
        v = np.zeros((self.nx, self.nstates, self.nstates))
        x = self.x

        v[:, 0, 0] = 0.5 * x**2
        v[:, 1, 1] = 0.5 * (x-d)**2 + E0

        self.v = v
        return v





if __name__ == '__main__':

    x = np.linspace(-2, 2, 128)
    y = np.linspace(-2, 2, 128)

    # mol = DHO(x)
    # mol.dpes(d=2, E0=2)

    cav = Cavity(1, 4)
    # pol = VibronicPolariton(mol, cav)
    # pol.dpes(g=0.05)
    # pol.ppes()

    # pol.draw_surfaces(n=4, representation='adiabatic')
    # pol.product_state(0, 0, 0)

    from pyqed.models.pyrazine import DHO2

    mol = DHO2(x, y, mass=[1,1])
    mol.plot_surface()
    pol = VibronicPolariton2(mol, cav)
    pol.dpes(g=0.)
    pol.ppes()
    pol.plot_surface(4, representation='diabatic')

    psi0 = np.zeros((len(x), len(y), pol.nstates), dtype=complex)
    psi0[:, :, 4] = pol.ground_state()[1]
    # pol.plot_ground_state()
    r = pol.run(psi0=psi0, dt=0.05, Nt=20, nout=2)
    r.plot_wavepacket(r.psilist, 4)


# the diabatic potential energy surface

