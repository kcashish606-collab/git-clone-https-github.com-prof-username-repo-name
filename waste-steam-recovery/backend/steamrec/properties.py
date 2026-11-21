"""Water/steam property states using CoolProp (IAPWS-95 formulation)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from CoolProp.CoolProp import PropsSI

from .units import k_to_f, pa_to_psia

FLUID = "Water"
PROPERTY_SOURCE = "CoolProp 6.x (IAPWS-95 formulation for water)"


@dataclass(frozen=True)
class State:
    """Thermodynamic state point. All values in SI."""

    label: str
    description: str
    P: float  # Pa
    T: float  # K
    h: float  # J/kg
    s: float  # J/kg-K
    v: float  # m^3/kg
    x: Optional[float]  # quality, None if single phase

    @property
    def rho(self) -> float:
        return 1.0 / self.v

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "description": self.description,
            "P_kPa": self.P / 1e3,
            "P_psia": pa_to_psia(self.P),
            "T_C": self.T - 273.15,
            "T_F": k_to_f(self.T),
            "h_kJ_kg": self.h / 1e3,
            "s_kJ_kgK": self.s / 1e3,
            "v_m3_kg": self.v,
            "x": self.x,
        }


def _state(label: str, description: str, k1: str, v1: float, k2: str, v2: float) -> State:
    P = PropsSI("P", k1, v1, k2, v2, FLUID)
    T = PropsSI("T", k1, v1, k2, v2, FLUID)
    h = PropsSI("H", k1, v1, k2, v2, FLUID)
    s = PropsSI("S", k1, v1, k2, v2, FLUID)
    rho = PropsSI("D", k1, v1, k2, v2, FLUID)
    q = PropsSI("Q", k1, v1, k2, v2, FLUID)
    x = q if 0.0 <= q <= 1.0 else None
    return State(label, description, P, T, h, s, 1.0 / rho, x)


def state_PT(label: str, description: str, P: float, T: float) -> State:
    return _state(label, description, "P", P, "T", T)


def state_Px(label: str, description: str, P: float, x: float) -> State:
    return _state(label, description, "P", P, "Q", x)


def state_Ph(label: str, description: str, P: float, h: float) -> State:
    return _state(label, description, "P", P, "H", h)


def t_sat(P: float) -> float:
    """Saturation temperature [K] at pressure P [Pa]."""
    return PropsSI("T", "P", P, "Q", 0, FLUID)


def flow_exergy(st: State, dead: State) -> float:
    """Specific physical flow exergy [J/kg]: (h - h0) - T0 (s - s0)."""
    return (st.h - dead.h) - dead.T * (st.s - dead.s)
