r"""
================================================
Solving a differential equation with time events
================================================

Time-events are events that occur at a specified time, like `t=[0.5, 1, 1.5 ...]`. An example of a time-event could be
control logic, which is executed on a different timescale than the physics which is modelled.

In this model, liquid flows in and out of a continuously stirred tank. The input flow rate varies, but the level of the
tank is desired to be the same, so the outlet valve is controlled using a PID controller. The model demonstrates the
use of solver time events.

This model also illustrates how to generate more advanced object-oriented models using the
:meth:`Model.component` decorator.


Model of a continously stirred tank
------------------------------------

The non-steady state mass-balance for a continuously stirred tank reactor (or CSTR) to which a homogeneous liquid  with
constant density, flows is:

.. math::

    \frac{dV}{dt} = \dot{Q}_{in}-\dot{Q}_{out}

where :math:`\dot{Q}_i` is the volumetric flow coming in to, or going out from, the tank. We wish to control the tank
level so that the liquid height :math:`h` of the tank remains approximately constant, in spite of disturbances to the
inlet flow rate :math:`\dot{Q}_{in}`. First we re-write the equation in terms of liquid column height :math:`h`:

.. math::

    \frac{dh}{dt} = \frac{1}{A} \left ( \dot{Q}_{in} - \dot{Q}_{out} \right )

where :math:`A` is the cross-sectional area of the tank.

To control the liquid height, a PID controller is implemented that controls the outlet flow-rate by adjusting the
outlet valve following the `control law`_:

.. _`control law`:

    .. math::

        K_v = k_p (h-h_{set}) + k_i \int (h-h_{set}) dt + k_d \frac{dh}{dt}


where :math:`K_v` is the lumped flow-coefficient of the valve. The flow-rate out follows `Toricelli's law`_:

.. math::

    \dot{Q}_{out} = K_v \sqrt{V}

when the flow is driven by the static pressure inside the tank, and the valve is located at the bottom of the tank.

The inlet flow-rate is assumed to be:

.. math::

    \dot{Q}_{in} = \dot{Q}_{in, nom} \cdot \left ( 1+f_N \cdot N(t) \right )

where :math:`\dot{Q}_{in, nom}` is the nominal flow-rate, :math:`N(t)` is the gaussian white noise (i.e. :math:`\mu=0`,
:math:`\sigma=1`), and :math:`f_N` is the noise level as a fraction of the nominal inlet flow-rate.

A perfect controller of this tank would simply set :math:`\dot{Q}_{out} = \dot{Q}_{in}`, but we are assuming that in a
practical implementation this is not possible, due to difficulties in measuring the flow-rate exactly. This would cause
small errors to eventually build up as large deviations. We shall later show this to be the case, by looking at the case
where we do not control the liquid level, but simply set :math:`\dot{Q}_{out} = \dot{Q}_{in, nom}`.


Implementation in numerous solver
--------------------------------------

To adjust the inlet flow-rate and the controller valve setting, we implemented two methods: :meth:`update_controller`
and :meth:`update_inlet_flow` in the :class:`Tank` model, while the `Model of a continously stirred tank`_ was
implemented in the :meth:`diff` method. The controller was implemented in the :class:`Controller` model, which contained
the `control law`_.

The model :class:`Tank` takes the following inputs:

==================  ==============================================
Parameter           Description
==================  ==============================================
v0                  The initial volume of the tank
a                   The cross-sectional area of the tank
controller          An instance of the :class:`Controller` class
noise_level         The white noise level as a percentage of the input flow
flow_in_0           Inlet flow-rate
==================  ==============================================

Likewise, :class:`Controller` model takes the following inputs:

==================  ==========================================================
Parameter           Description
==================  ==========================================================
k_p                 P-part of the PID controller, i.e. proportional gain
k_i                 I-part of the PID controller, i.e. integral gain
k_d                 D-part of the PID controller, i.e. differential gain
dt_controller       | The time-interval between controller updates.
                    Also used to find the next time event in the \
                    :meth:`~solver.interface.Interface.get_next_time_event` method
h_set               Liquid height set-point
==================  ==========================================================

In the model interface :class:`TankInterface`, we implemented the two methods, :meth:`update_controller`
and :meth:`update_inlet_flow`, inside the :meth:`~solver.interface.Interface.run_time_event_action` method.
As a simplification we assumed that the inlet flow was updated discretely, at the same timescale as the controller is
updated.

The interface class :class:`TankInterface` contains the following methods:

* :meth:`~solver.interface.Interface.get_deriv`
* :meth:`~solver.interface.Interface.set_states`
* :meth:`~solver.interface.Interface.get_states`
* :meth:`~solver.interface.Interface.get_next_time_event`
* :meth:`~solver.interface.Interface.run_time_event_action`

Most of these methods have already been discussed elsewhere e.g. :ref:`sphx_glr_auto_examples_exponential_approach.py`.
The methods we haven't taken a look at this far is :meth:`~solver.interface.Interface.get_next_time_event` and
:meth:`~solver.interface.Interface.run_time_event_action`. :meth:`~solver.interface.Interface.get_next_time_event`
returns to the solver the next time, at which a time event takes place, while
:meth:`~solver.interface.Interface.run_time_event_action` executes the action whenever the time-event occurs.
The solver makes sure that the solution passes through the time-event steps set by the
:meth:`~solver.interface.Interface.get_next_time_event` method.


A note about jitting and the :meth:`Model.component` decorator
    ------------------------------------------------------------------------------------

The model of the CSTR has been implemented below in the :class:`Tank` model, while the controller has been implemented
as :class:`Controller`, with the main model being the former. The :class:`Tank` model is decorated by the
:meth:`Model.with_interface` decorator, while the :class:`Controller` model is decorated with the
:meth:`Model.component` decorator. The reason being there can only be one interface per model, and that is the
one specified by the :class:`Tank` class, i.e. the :class:`TankInterface`. Since we want to allow the model to be
jitted by `numba`, we used the :meth:`Model.component` decorator on the :class:`Controller`. Without
this decorator, `numerous solver` cannot be jitted. Allowing jitting is also the reason why the instantiated
:class:`Controller` is fed to the :class:`Tank` as an input, since `numba` currently cannot infer the type of
:class:`Controller` without this, and attempting to use jitting will result in an error.

Examples
--------------
Below is an example code that runs the model, and creates a plot of the tank volume. The inlet volume is assumed to
follow a sinusoidal curve. Initially the liquid height is assumed to be at it's desired set-point.

It is clear from the results, that adding a controller is much better than simply relying on measurement of the nominal
flow-rate, in terms of keeping the liquid level as constant as possible.



.. _`Toricelli's law`:
    https://en.wikipedia.org/wiki/Toricelli%27s_law


"""
import numpy as np
import pandas as pd

from numerous.solver.interface import Interface, Model
from numerous.solver.numerous_solver import NumerousSolver
import plotly.graph_objects as go
import plotly
import itertools
import plotly.express as px


@Model.component
class Controller:

    def __init__(self, k_p=1.0, k_i=0.1, k_d=0.1, dt_controller=1.0, h_set=0.5):
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.i_max = 1000.0
        self.e = 0.0
        self.h_set = h_set
        self.y = np.array([0], dtype='float')
        self.update_interval = dt_controller
        self.valve_max = np.array([10.0], dtype='float')
        self.initial = True

    def control_valve(self, t, h):
        e = h - self.h_set
        if self.initial:
            e_old = e
            self.initial = False
        else:
            e_old = self.e
        valve_sp = self.k_p * e + self.k_i * self.y + self.k_d * (e-e_old)/self.update_interval
        if valve_sp < 0:
            valve_sp = np.array([0.0], dtype='float')
        if valve_sp > self.valve_max:
            valve_sp = self.valve_max

        self.e = e
        return valve_sp

    def diff(self, y):
        if y <= self.i_max:
            return self.e
        else:
            return 0

    def reset(self):
        self.initial = True


@Model.with_interface()
class Tank:
    def __init__(self, v0: float = 1.0, a: float = 1.0, noise_level = 1.0, flow_in_0 = 0.1,
                 controller: Controller = None):

        self.a = a  # cross-sectional area of tank
        self.h0 = v0/a
        self.y = np.array([v0, self.h0, v0, self.h0], dtype='float')
        self.flow_in = np.array([0.0], dtype='float')
        self.flow_in_0 = flow_in_0

        self.controller = controller

        self.k_valve = self.controller.control_valve(0, self.h0)
        self.noise_level = noise_level/100  # The level of the noise in percentage of process value.
        self.ix = 0

    def diff(self, t, y) -> np.array:

        dydt = np.empty_like(y, dtype='float')
        vol = y[0]
        h = vol / self.a
        flow_out = self.k_valve * np.sqrt(h)
        flow_in = self.flow_in
        diff_flow = flow_in - flow_out * (flow_out >= 0)
        diff_flow_no_controller = flow_in-self.flow_in_0
        dydt[0] = diff_flow[0]
        dydt[1] = dydt[0] / self.a
        dydt[2] = diff_flow_no_controller[0]
        dydt[3] = dydt[2] / self.a
        return dydt

    def update_inlet_flow(self, t):
        flow_in = self.flow_in_0 * (1+self.noise_level*np.random.normal())
        self.flow_in = np.array([flow_in], dtype='float')

    def update_controller(self, t, y):
        vol = y[0]
        h = vol / self.a
        self.k_valve = self.controller.control_valve(t, h)


class TankInterface(Interface):

    def __init__(self, model: Tank):
        self.model = model
        self.t_event = 0.0
        self.y0 = self.get_states()

    def set_states(self, y: np.array) -> None:
        y_cstr = y[:4]
        y_controller = y[4]
        self.model.y = y_cstr
        self.model.controller.y = np.array([y_controller])

    def get_states(self) -> np.array:
        y = np.empty(5, dtype='float')
        y[:4] = self.model.y
        y[4] = self.model.controller.y[0]
        return y

    def get_deriv(self, t: float, y: np.array) -> np.array:
        dydt = np.empty(5, dtype='float')
        dydt[:4] = self.model.diff(t, y[:4])
        dydt[4] = self.model.controller.diff(y[4])
        return dydt

    def get_next_time_event(self, t) -> tuple[int, float]:
        return 1, self.t_event + self.model.controller.update_interval

    def run_time_event_action(self, t: float, y: np.array, event_idx: int) -> np.array:

        self.model.update_inlet_flow(t)
        self.model.update_controller(t, y)
        self.t_event += self.model.controller.update_interval
        return y


if __name__ == "__main__":
    #  Some plotly stuff to generate the figures
    col_pal = px.colors.qualitative.Safe
    col_pal_iterator = itertools.cycle(col_pal)
    fig = go.Figure()

    time = np.append(np.arange(0, 1000, 1), 1000)  # Time to solve - used also as input to tank model to add white noise
    flow_in_0 = 0.1  # The nominal flow-rate without any noise
    noise_levels = [0, 10, 50, 75]  # Levels of white noise to simulate - percentage of desired input flow-rate

    h_set_0 = 0.5  # Set-point height of liquid column in tank
    h_set = np.ones_like(time) * h_set_0  # Just a line to show later

    controller = Controller(dt_controller=0.1, h_set=h_set_0)  # Create controller and set refresh rate
    model = Tank(controller=controller, v0=0.5, noise_level=0.0,
                 flow_in_0=flow_in_0)  # Create Tank model

    numsol = NumerousSolver(model=model, use_jit=False)  # Compile the model with jit
    compiled_model = model.compiled_model  # The compiled model object is available after compiling the solver
    y0 = numsol.y0  # save the initial states when resetting later
    df = pd.DataFrame()
    for i, noise_level in enumerate(noise_levels):
        new_color = next(col_pal_iterator)  # make sure to get the color of the plotly line
        numsol.reset()
        compiled_model.noise_level = noise_level / 100  # Set the noise level
        numsol.solve(time)  # When providing the state vector y0, the interface is reset as well

        t = np.array(numsol.solution.results).T[0, :]  # Extract the solution time from the solution object
        results = np.array(numsol.solution.results).T[2]  # Extract the results from the solution object

        # as above, but for situation where outlet flow is simply set to nominal inlet flow-rate:
        results_no_controller = np.array(numsol.solution.results).T[4]

        fig.add_trace(go.Scatter(x=t, y=results, name=f"noise level {noise_level} with controller",
                                 line=dict(color=new_color)))  # Add a trace with controller
        fig.add_trace(go.Scatter(x=t, y=results_no_controller, name=f"noise level {noise_level} without controller",
                                 line=dict(dash='dash', color=new_color)))  # Add a trace without controller

        df = pd.concat([df, pd.DataFrame({'noise_level': [noise_level], 'std w. controller': [np.std(results)],
                   'std w.o. controller': [np.std(results_no_controller)]})])


    df = df.set_index('noise_level')
    fig.add_trace(go.Scatter(x=time, y=h_set, name='setpoint'))
    fig.update_layout(xaxis_title='time', yaxis_title='liquid height')  # Add titles

    plotly.io.show(fig)  # Plot figure
    print(df)

