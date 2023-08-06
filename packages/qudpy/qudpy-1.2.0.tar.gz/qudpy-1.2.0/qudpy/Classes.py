from qutip import *
import numpy as np
import matplotlib.pyplot as plt

class System:
    """
    The system class defines the physical system through a model hamiltonian.
    the elements internal to this class are:
    n = Maximum excited state
    H = Hamiltonian of the system
    rho = density matrix of the system
    a = lowering operator for the system
    u = dipole operator
    c_ops = collapse operators that connect the system to the bath
    e_ops = observables, for which expectation values are required
    tlist = a list of time-steps for evolution
    """
    # some default values for parameters of interest
    hbar = 0.658211951  # eV fs
    h = 4.13566766  # eV fs
    E = 2  # eV
    f = E/h  # frequency in per fs
    w = E/hbar  # angular frequency 2*np.pi*f (the units are radians per fs.)

    current_states = None

    def __init__(self, n=None, H=None, rho=None, a=None, u=None, c_ops=None, e_ops=None, tlist=None, diagonalize=False):
        self.n = n if n is not None else 3  # Note: number of energy levels = maximum excited state + 1 = n+1
        self.rho = rho if rho is not None else fock_dm(self.n+1, 0)  # starting density matrix. Default is ground state
        self.a = a if a is not None else destroy(self.n+1)  # lowering operator
        self.u = u if u is not None else self.a.dag()+self.a  # dipole operator
        self.H = H if H is not None else self.hbar*self.w*self.a.dag()*self.a  # hamiltonian, default is harmonic os.
        self.c_ops = c_ops if c_ops is not None else []  # list of collapse operators, default is empty
        self.e_ops = e_ops if e_ops is not None else []  # list of expectation values, default is empty
        self.tlist = tlist if tlist is not None else []  # list of time steps, default is empty
        self.diagonalized = diagonalize
        if self.diagonalized:
            print("diagonalizing Hamiltonian and transforming everything into eigen-basis except rho")
            evals, evecs = self.H.eigenstates()
            self.a = self.a.transform(evecs)
            self.u = self.u.transform(evecs)
            self.H = self.H.transform(evecs)
            self.c_ops = [c.transform(evecs) for c in self.c_ops]
            self.e_ops = [e.transform(evecs) for e in self.e_ops]
        print("system initialized")

    def diagram_donkey(self, interaction_times=None, diagrams=None, r=10):
        """
        Computes and plots a single evolution of the density matrix for a list of double-sided diagrams
        Mainly useful for inspection/instructional purposes.
        :param interaction_times: a list of arrival times for pulses and the last entry is time interval for detection
        of local oscillator. Note, First pulse arrives at t=0
        :param diagrams: A list of double-sided diagrams (ufss diagramGenerator format)
        :param r: temporal resolution (time steps per fs)
        :return: None
        """
        if interaction_times is None:
            print("Error: interaction times not given")
        elif diagrams is None:
            print("Error: diagrams not given")
            return None

        # setting up simulation
        total_diagrams, total_interactions = np.shape(diagrams)[:2]
        print('total diagrams', total_diagrams, ', total interactions ', total_interactions)
        for diagram in diagrams:  # loop over diagrams
            rho = self.rho  # setting initial density matrix (typically the ground state)
            states = []
            # Iterating over pulses
            for pulse in range(len(interaction_times)-1):  # loop over the  pulses
                # applying all the interactions of a given pulse
                for x in diagram:  # loop over interactions in a diagram
                    print(x)
                    if x[1] == pulse:
                        if x[0] == 'Ku':
                            rho = (self.a.dag()*rho)
                        elif x[0] == 'Bu':
                            rho = (rho*self.a)
                        elif x[0] == 'Kd':
                            rho = (self.a*rho)
                        elif x[0] == 'Bd':
                            rho = (rho*self.a.dag())
                delta_t = interaction_times[pulse+1]-interaction_times[pulse]
                results = mesolve(
                    self.H, rho, np.linspace(interaction_times[pulse], interaction_times[pulse+1], delta_t*r),
                    self.c_ops, [])
                rho = results.states[-1]  # using last state of current simulation as initial state of next one
                states += results.states

            time_list = np.linspace(interaction_times[0], interaction_times[-1], len(states))
            plt.figure()
            plt.plot(time_list, np.imag(expect(self.u, states)))
            plt.plot(time_list, np.abs(expect(self.a.dag() * self.a, states)))
            plt.legend(['dipole', 'number'])
            plt.xlabel('Time (fs)')
            plt.ylabel('Value')
            plt.title('Expectation Values for '+str(diagram))
        plt.show()
        return None

    def coherence2d(self, time_delays=None, diagram=None, scan_id=None, r=10, parallel=False):
        """
        computes the 2D coherence plot for a single diagram with only two scan-able delays.
        It can be parallelized if resources are available.
        :param time_delays: list of time delays (Note: provide time delay for each interaction even if zero)
        :param diagram: a double-sided diagram (ufss diagramGenerator format)
        :param scan_id: a list indices for the time delays in interaction_times that have to be scanned
        :param r: time resolution (steps per fs)
        :param parallel: Parallelization control, True or False
        :return: a list of density matrices, numpy array of first scan time and second scan time
        """

        if len(time_delays) != len(diagram):
            print('time delays for each interaction not given')
            print('number of time delays', len(time_delays), ' number of interactions ', len(diagram))
            return None
        if len(scan_id)!=2:
            print('scan id not provided for two tunable delays')
            return None

        if parallel:
            from qutip import parallel as pp

        rho = self.rho  # taking the initial state from the system class

        # go through interactions and time delays, if time delays are zero move to next iteration
        # The loop only goes on till the first scan-able delay is encountered.
        for i in range(scan_id[0]):
            rho = self.apply_pulse(rho, diagram[i])  # applying pulse interaction

            # evolving after pulse interaction in case the delay is non-zero
            delta_t = time_delays[i]
            if delta_t > 0:
                coherence_time = np.linspace(0, delta_t, int(delta_t*r))
                results = mesolve(self.H, rho, coherence_time, self.c_ops, [])
                rho = results.states[-1]  # keeping only the last state

        # At this point all the pulses and delays have been applied that do not need scanning
        # now applying the pulse and the delay that has to be scanned --> therefore saving all states.
        rho = self.apply_pulse(rho, diagram[scan_id[0]])
        delta_t = time_delays[scan_id[0]]
        t_list = np.linspace(0, delta_t, int(delta_t*r))
        results = mesolve(self. H, rho, t_list, self.c_ops, [])
        states = results.states

        # Applying next set of interactions until a scan-able delay is encountered
        for i in range(scan_id[0]+1, scan_id[1]):
            states = [self.apply_pulse(state, diagram[i]) for state in states]  # applying interaction to all states
            delta_t = time_delays[i]
            if delta_t > 0:
                coherence_time = np.linspace(0, delta_t, int(delta_t*r))
                # evolving each state in the list states and storing only the last state
                if parallel:
                    self.tlist = coherence_time
                    states = pp.parallel_map(self.para_mesolve, states, only_last_state=True)
                    #states = [pp.parfor(self.para_mesolve, states, only_last_state=True)]
                    #print('shape of states is ', np.shape(states))
                else:
                    states = [mesolve(self.H, state, coherence_time, self.c_ops, []).states[-1] for state in states]

        # Now at this point only last interaction and last scan-able delay is left.
        print('First scan done, starting second scan. Remaining time = First Scan Time x number of steps in second scan'
              + '/number of processors')
        states = [self.apply_pulse(state, diagram[scan_id[1]]) for state in states]
        delta_t = time_delays[scan_id[1]]
        t_list = np.linspace(0, delta_t, int(delta_t*r))
        final_states = []
        if parallel:
            self.tlist = t_list
            final_states.append(pp.parfor(self.para_mesolve, states, only_last_state=False))
            final_states = final_states[0]
        else:
            final_states = [mesolve(self.H, state, t_list, self.c_ops, []).states for state in states]

        dipole = np.array([expect(self.u, final_states[x][:]) for x in range(len(final_states))])
        #dipole = None
        #plt.figure()
        #plt.imshow(dipole.imag, origin='lower', interpolation='spline36', extent=[0, time_delays[scan_id[0]],
        #                                                                          0, time_delays[scan_id[1]]])
        #plt.show()
        print('second scan done')
        return final_states, np.linspace(0, time_delays[scan_id[0]], int(time_delays[scan_id[0]] * r)), t_list, dipole

    # some small helper functions to keep the coherence2D function readable
    def apply_pulse(self, rho, x):
        """
        Simple function for applying an operator on a density matrix
        :param rho: initial density matrix
        :param x: Operator
        :return: final density matrix
        """
        if x[0] == 'Ku':
            rho = (self.a.dag()*rho)#.unit()
        elif x[0] == 'Bu':
            rho = (rho*self.a)#.unit()
        elif x[0] == 'Kd':
            rho = (self.a*rho)#.unit()
        elif x[0] == 'Bd':
            rho = (rho*self.a.dag())#.unit()
        return rho

    def para_mesolve(self, rho, only_last_state=True):
        """
        Simple function for facilitating parallelization in the function coherence2d
        :param rho: density matrix
        :param only_last_state: Bool for keeping whole array of density matrices or only the last one
        :return: list of states or state
        """
        if only_last_state:
            return mesolve(self.H, rho, self.tlist, self.c_ops, []).states[-1]
        else:
            return mesolve(self.H, rho, self.tlist, self.c_ops, []).states

    # some common plotting functions

    def spectra(self, dipoles=None, resolution=10):
        """
        Converts the list of dipoles into spectra though Fourier transform
        :param dipoles:
        :param resolution:
        :return: List of spectra, minimum and maximum limits of each axis, grid of freq 1 and freq 2
        """
        if dipoles is None:
            print('Input data missing')
            return

        spectra = [np.fft.fftshift(np.fft.fft2(mu)) for mu in dipoles]
        # note the multiplication with 2pi is required because fft works with freq and qutip with omega
        freq1 = np.fft.fftshift(np.fft.fftfreq(np.shape(spectra[0])[1], 1 / resolution)) * 2 * np.pi
        freq2 = np.fft.fftshift(np.fft.fftfreq(np.shape(spectra[0])[0], 1 / resolution)) * 2 * np.pi
        extent = [min(freq1), max(freq1), min(freq2), max(freq2)]
        f1, f2 = np.meshgrid(freq1, freq2)

        return spectra, extent, f1, f2

    def linear_spec(self, scan_time: int, diagram=None, resolution=10):
        """
        For computing simple linear spectra from the system after any number of interaction in the start.
        Note: for increasing the frequency resolution, simply increase the scan_time. For decreasing the range of
        frequencies, decrease the time resolution.
        :param scan_time: Time interval to be simulated
        :param diagram: Double-sided diagram for calculating the system response. Note: all interactions contained in
        the diagram are applied at t=0. If diagram=None, then by default a 'Bu' interaction is applied at t=0.
        :param resolution: Time resolution of simulation
        :return: dipole expectation value, time, spectrum and frequency lists.
        """
        t_list = np.linspace(0, scan_time, resolution * scan_time)
        if diagram:
            rho = self.rho
            for x in diagram:
                rho = self.apply_pulse(rho, x)  # applying pulse interactions term by term
        else:
            rho = self.rho * self.a
            # linear response is created by 'Bu' action on rho initial, alternatively we can apply
        dipole = mesolve(self.H, rho, t_list, self.c_ops, [self.u]).expect[0]

        plt.figure(figsize=(16, 6))
        plt.plot(t_list, np.imag(dipole))
        plt.plot(t_list, np.real(dipole))
        plt.legend(['Imaginary', 'Real'])
        plt.xlabel('Time (fs)')
        plt.ylabel('Dipole')
        plt.title('Expectation Values for linear response')
        plt.show()

        spec = np.fft.fftshift(np.fft.fft(dipole))

        freq = np.fft.fftshift(np.fft.fftfreq(np.shape(spec)[0], 1 / resolution)) * 2 * np.pi
        plt.figure(figsize=(16, 6))
        plt.plot(freq, np.imag(spec))
        plt.plot(freq, np.real(spec))
        plt.legend(['Imaginary', 'Real'])
        plt.xlabel('Freq (eV)')
        plt.ylabel('Dipole')
        plt.title('Spectrum from linear response (Bu)')
        plt.show()
        # print(spec[len(freq)//2:])
        # print(freq[len(freq)//2:])
        return dipole, t_list, spec, freq

    def pop_study(self, pop_time_list=None, pop_index=1, time_delays=None, diagram=None, scan_id=None, r=10, parallel=False):
        """
        For calculating the nonlinear response of a double-sided diagram for a set of population times.
        :param pop_time_list: list of population times
        :param pop_index: index of the population generating interaction
        :param time_delays: list of time delays between interactions
        :param diagram: double-sided diagram to be simulated
        :param scan_id: indices of time delays to be scanned for 2D coherence plot
        :param r: time resolution of simulation
        :param parallel: True/False control of parallelized computation.
        :return: list of 2D coherence response for each population time, t1 and t2 times for 2D coherence,
        list of spectra for each population time, extent of x and y-axis in spectra, f1 and f2 grid for spectra.
        """
        if len(time_delays) != len(diagram):
            print('time delays for each interaction not given')
            print('number of time delays', len(time_delays), ' number of interactions ', len(diagram))
            return None
        if len(scan_id) != 2:
            print('scan id not provided for two tunable delays')
            return None
        if len(pop_time_list) < 2:
            print('Less than two population times requested')

        pop_response = []
        for t_pop in pop_time_list:
            time_delays[pop_index] = t_pop
            states, t1, t2, dipole = self.coherence2d(time_delays, diagram, scan_id, r, parallel)
            pop_response.append(dipole)  # both real and imaginary parts are contained in it.

        spectra_list, extent, f1, f2 = self.spectra(np.imag(pop_response))

        return pop_response, t1, t2, spectra_list, extent, f1, f2
