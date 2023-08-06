# This file is part of PyCosmo, a multipurpose cosmology calculation tool in Python.
#
# Copyright (C) 2013-2021 ETH Zurich, Institute for Particle and Astrophysics and SIS
# ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.


import warnings

import numpy as np
from scipy.integrate import solve_ivp

from .Fields import Fields


class ScipySolver:

    _wrappers = {}

    def __init__(
        self,
        cosmology,
        method,
        **extra_args_for_solver,
    ):
        self.extra_args_for_solver = extra_args_for_solver

        self.params = cosmology.params
        self.cosmology = cosmology
        self.background = cosmology.background
        self.method = method

        self.wrapper = cosmology._wrapper

    def initial_conditions(self, k):
        self.wrapper.set_globals(k=k)

        initial_conditions = getattr(
            self.wrapper, "initial_values_" + self.params.initial_conditions, None
        )
        if initial_conditions is None:
            raise ValueError(
                "initial conditions '{}' not implemented.".format(
                    self.initial_conditions
                )
            )

        return initial_conditions()

    def _setup_globals(self, k):
        parameters = {"k": k}
        for key in self.wrapper.get_globals().keys():
            if key == "k":
                continue
            else:
                value = getattr(self.params, key)
            parameters[key] = value
        self.wrapper.set_globals(**parameters)
        return parameters

    def solve(
        self,
        k,
        grid,
    ):
        self._setup_globals(k)

        a_0, _, *y_0 = self.initial_conditions(k)
        lna0 = np.log(a_0)
        y_0 = np.array(y_0)

        if not isinstance(grid, float):
            grid = np.array(grid)

            if np.any(grid <= lna0):
                warnings.warn(
                    "grid starts before initial a0= {:e} resp lna0 = {:e}, removed"
                    " therefore gridpoints".format(a_0, lna0)
                )

            grid = grid[grid > lna0]
            grid = t_eval = np.concatenate(([lna0], grid))
            t_span = (min(grid), max(grid))
        else:
            assert grid > lna0
            t_eval = None
            t_span = (lna0, grid)

        def rhs(lna, y):
            return self.cosmology._wrapper.rhs_linear_perturbation(lna, y)

        def jac(lna, y):
            # transpose result to return array in fortran storage order:
            return np.ascontiguousarray(
                self.cosmology._wrapper.jac_linear_perturbation(lna, y).T
            )

        result = solve_ivp(
            rhs,
            t_span,
            y_0,
            self.method,
            t_eval=t_eval,
            jac=jac,
            **self.extra_args_for_solver,
        )
        meta = dict(result.items())
        assert meta["status"] == 0, meta
        y = meta.pop("y").T

        return grid, y, meta

    def fields(self, k, grid, keep_lna0=False):
        grid, y, meta = self.solve(k, grid)
        if not keep_lna0:
            grid = grid[1:]
            y = y[1:]

        fields = Fields(self.cosmology)
        fields.set_results(grid, y)
        fields.meta = meta
        return fields
