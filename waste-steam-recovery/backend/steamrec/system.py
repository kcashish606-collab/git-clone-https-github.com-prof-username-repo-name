"""Combined space-heating + condensate-recovery model for sub-atmospheric waste steam.

Operating modes
---------------
Heating mode (``heating_hours``): part of the steam condenses in a vacuum
steam-to-water heat exchanger that serves a low-temperature building hot-water
loop. Steam beyond the building load goes to a trim surface condenser.

Cooling mode (``operating_hours - heating_hours``): all steam condenses in the
surface condenser, which rejects heat to a cooling tower. There is no heating credit.

In both modes, condensate is collected in a hotwell under vacuum, pumped to
return pressure, and credited as recovered water. Heat and water are separate
benefits, so nothing is double counted.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, replace

from . import units as u
from .properties import (
    PROPERTY_SOURCE,
    State,
    flow_exergy,
    state_Ph,
    state_PT,
    state_Px,
    t_sat,
)

MIN_APPROACH_F = 5.0  # minimum condensing-temperature approach for heat exchangers


@dataclass
class Inputs:
    # Waste steam (project statement)
    steam_flow_lbm_h: float = 64_500.0
    steam_pressure_psia: float = 3.8
    steam_temp_F: float = 224.0
    # Reference (dead) state
    dead_temp_F: float = 77.0
    dead_pressure_psia: float = 14.696
    # Heating system
    building_load_MW: float = 5.0
    recovery_efficiency: float = 0.85  # fraction of HX duty usefully delivered to the building
    hw_return_F: float = 110.0
    hw_supply_F: float = 140.0
    hw_loop_pressure_psia: float = 30.0
    hw_pump_dp_psi: float = 20.0
    hx_U_W_m2K: float = 2500.0
    # Condenser / cooling tower
    cw_in_F: float = 85.0
    cw_out_F: float = 105.0
    condenser_U_W_m2K: float = 3000.0
    cooling_tower_kW_per_MW: float = 10.0  # fan + CW pump parasitic per MW rejected
    # Condensate return
    pump_outlet_psia: float = 25.0
    pump_efficiency: float = 0.70
    vacuum_pump_kW: float = 15.0
    # Economics (project statement)
    operating_hours: float = 8000.0
    heating_hours: float = 3000.0
    electricity_price: float = 0.08  # $/kWh
    heat_price: float = 0.08  # $/kWh of useful heat
    water_price_per_100gal: float = 0.70

    def validate(self) -> list[str]:
        errors = []
        if self.heating_hours > self.operating_hours:
            errors.append("heating_hours cannot exceed operating_hours")
        if self.hw_supply_F <= self.hw_return_F:
            errors.append("hot-water supply temperature must exceed return temperature")
        if self.cw_out_F <= self.cw_in_F:
            errors.append("cooling-water outlet temperature must exceed inlet temperature")
        if not 0 < self.recovery_efficiency <= 1:
            errors.append("recovery_efficiency must be in (0, 1]")
        if not 0 < self.pump_efficiency <= 1:
            errors.append("pump_efficiency must be in (0, 1]")
        return errors


def _lmtd_condensing(t_sat_k: float, t_in_k: float, t_out_k: float) -> float:
    dt1, dt2 = t_sat_k - t_in_k, t_sat_k - t_out_k
    if dt1 <= 0 or dt2 <= 0:
        return float("nan")
    return dt1 if math.isclose(dt1, dt2) else (dt1 - dt2) / math.log(dt1 / dt2)


def analyze(inp: Inputs) -> dict:
    errors = inp.validate()
    if errors:
        raise ValueError("; ".join(errors))
    warnings: list[str] = []

    # ---------- Baseline state ----------
    m = u.lbm_h_to_kg_s(inp.steam_flow_lbm_h)
    P1 = u.psia_to_pa(inp.steam_pressure_psia)
    T1 = u.f_to_k(inp.steam_temp_F)
    Tsat = t_sat(P1)
    if T1 <= Tsat:
        raise ValueError("Inlet steam must be superheated at the given pressure for this model")

    dead = state_PT("0", "Dead state (environment)", u.psia_to_pa(inp.dead_pressure_psia), u.f_to_k(inp.dead_temp_F))
    s1 = state_PT("1", "Waste steam inlet (superheated, sub-atmospheric)", P1, T1)
    s2 = state_Px("2", "Condensate leaving HX/condenser (sat. liquid)", P1, 0.0)
    P3 = u.psia_to_pa(inp.pump_outlet_psia)
    h3 = s2.h + s2.v * (P3 - P1) / inp.pump_efficiency
    s3 = state_Ph("3", "Condensate pump discharge", P3, h3)

    P_hw = u.psia_to_pa(inp.hw_loop_pressure_psia)
    s4 = state_PT("4", "Hot-water loop return (to HX)", P_hw, u.f_to_k(inp.hw_return_F))
    s5 = state_PT("5", "Hot-water loop supply (to building)", P_hw, u.f_to_k(inp.hw_supply_F))
    P_cw = u.psia_to_pa(14.696)
    s6 = state_PT("6", "Cooling water in (from tower)", P_cw, u.f_to_k(inp.cw_in_F))
    s7 = state_PT("7", "Cooling water out (to tower)", P_cw, u.f_to_k(inp.cw_out_F))

    if u.k_to_f(Tsat) - inp.hw_supply_F < MIN_APPROACH_F:
        warnings.append(
            f"Hot-water supply {inp.hw_supply_F:.0f} °F is within {MIN_APPROACH_F:.0f} °F of "
            f"T_sat = {u.k_to_f(Tsat):.1f} °F, so the HX is infeasible or very large."
        )
    if u.k_to_f(Tsat) - inp.cw_out_F < MIN_APPROACH_F:
        warnings.append("Cooling-water outlet is too close to T_sat; condenser is infeasible.")

    psi = {st.label: flow_exergy(st, dead) for st in (s1, s2, s3, s4, s5, s6, s7)}

    q_cond = s1.h - s2.h  # J/kg, desuperheat + latent
    Q_avail = m * q_cond  # W
    E_total = m * (s1.h - dead.h)  # W, energy relative to dead state
    X_in = m * psi["1"]  # W, physical exergy rate

    # ---------- Heating mode ----------
    Q_load = inp.building_load_MW * 1e6
    Q_hx = min(Q_avail, Q_load / inp.recovery_efficiency)  # HX duty
    Q_useful = inp.recovery_efficiency * Q_hx  # heat delivered to building
    Q_dist_loss = Q_hx - Q_useful
    m_hx = Q_hx / q_cond
    m_trim = m - m_hx
    Q_trim = m_trim * q_cond
    m_hw = Q_hx / (s5.h - s4.h)
    W_hw_pump = m_hw * s4.v * u.psia_to_pa(inp.hw_pump_dp_psi) / inp.pump_efficiency

    if Q_load / inp.recovery_efficiency > Q_avail:
        warnings.append("Building load exceeds recoverable steam heat, so heating is steam-limited.")

    # ---------- Cooling mode ----------
    dh_cw = s7.h - s6.h
    m_cw_heating = Q_trim / dh_cw
    m_cw_max = Q_avail / dh_cw

    # ---------- Condensate pump ----------
    W_cond_pump = m * (s3.h - s2.h)

    # ---------- Exergy accounting (heating mode, rates in W) ----------
    X_to_hw = m_hw * (psi["5"] - psi["4"])
    X_dest_hx = dead.T * (m_hx * (s2.s - s1.s) + m_hw * (s5.s - s4.s))
    X_lost_trim = m_trim * (psi["1"] - psi["2"])
    X_condensate = m * psi["2"]
    X_dest_pump = dead.T * m * (s3.s - s2.s)
    eta_II_hx = X_to_hw / (m_hx * (psi["1"] - psi["2"])) if m_hx > 0 else 0.0
    X_lost_cooling_mode = m * (psi["1"] - psi["2"])

    # ---------- Equipment sizing ----------
    lmtd_hx = _lmtd_condensing(Tsat, s4.T, s5.T)
    lmtd_cd = _lmtd_condensing(Tsat, s6.T, s7.T)
    A_hx = Q_hx / (inp.hx_U_W_m2K * lmtd_hx) if lmtd_hx == lmtd_hx else float("nan")
    A_cd = Q_avail / (inp.condenser_U_W_m2K * lmtd_cd) if lmtd_cd == lmtd_cd else float("nan")
    cond_gpm = m * s2.v * u.M3_S_TO_GPM
    hw_gpm = m_hw * s4.v * u.M3_S_TO_GPM
    cw_gpm = m_cw_max * s6.v * u.M3_S_TO_GPM

    equipment = [
        {"tag": "HX-101", "name": "Vacuum steam-to-water heat exchanger",
         "spec": f"Duty {Q_hx/1e6:.2f} MW; shell {inp.steam_pressure_psia:.1f} psia; "
                 f"LMTD {lmtd_hx*1.8:.1f} °F; U {inp.hx_U_W_m2K:.0f} W/m²K; area ≈ {A_hx:.0f} m²"},
        {"tag": "E-201", "name": "Surface condenser (sized for 100% steam)",
         "spec": f"Duty {Q_avail/1e6:.2f} MW; LMTD {lmtd_cd*1.8:.1f} °F; "
                 f"U {inp.condenser_U_W_m2K:.0f} W/m²K; area ≈ {A_cd:.0f} m²"},
        {"tag": "CT-301", "name": "Cooling tower",
         "spec": f"Max rejection {Q_avail/1e6:.2f} MW; CW {cw_gpm:,.0f} gpm "
                 f"({inp.cw_in_F:.0f}→{inp.cw_out_F:.0f} °F); parasitic ≈ {inp.cooling_tower_kW_per_MW*Q_avail/1e6:.0f} kW"},
        {"tag": "P-401", "name": "Condensate pump (from vacuum hotwell)",
         "spec": f"{cond_gpm:,.0f} gpm; {inp.steam_pressure_psia:.1f}→{inp.pump_outlet_psia:.0f} psia; "
                 f"{W_cond_pump/1e3:.2f} kW; low-NPSH design, hotwell elevated above pump"},
        {"tag": "P-402", "name": "Hot-water circulation pump",
         "spec": f"{hw_gpm:,.0f} gpm; ΔP {inp.hw_pump_dp_psi:.0f} psi; {W_hw_pump/1e3:.1f} kW"},
        {"tag": "VP-501", "name": "Liquid-ring vacuum pump / steam-jet ejector",
         "spec": f"Removes non-condensables, holds {inp.steam_pressure_psia:.1f} psia; ≈ {inp.vacuum_pump_kW:.0f} kW"},
    ]

    # ---------- Economics ----------
    H, Hh = inp.operating_hours, inp.heating_hours
    Hc = H - Hh
    heat_kWh = Q_useful / 1e3 * Hh
    heat_value = heat_kWh * inp.heat_price

    rho_std = state_PT("std", "Water at 60 °F", P_cw, u.f_to_k(60.0)).rho
    gal_per_h = m * 3600.0 / rho_std * u.M3_TO_GAL
    water_gal_yr = gal_per_h * H
    water_value = water_gal_yr / 100.0 * inp.water_price_per_100gal

    ct_kWh = inp.cooling_tower_kW_per_MW * (Q_trim / 1e6 * Hh + Q_avail / 1e6 * Hc)
    pump_kWh = W_cond_pump / 1e3 * H + W_hw_pump / 1e3 * Hh
    vac_kWh = inp.vacuum_pump_kW * H
    parasitic_kWh = ct_kWh + pump_kWh + vac_kWh
    parasitic_cost = parasitic_kWh * inp.electricity_price

    gross = heat_value + water_value
    net = gross - parasitic_cost
    total_energy_kWh = E_total / 1e3 * H

    return {
        "inputs": asdict(inp),
        "property_source": PROPERTY_SOURCE,
        "states": [st.to_dict() for st in (dead, s1, s2, s3, s4, s5, s6, s7)],
        "baseline": {
            "mass_flow_kg_s": m,
            "T_sat_F": u.k_to_f(Tsat),
            "superheat_F": inp.steam_temp_F - u.k_to_f(Tsat),
            "energy_rate_MW": E_total / 1e6,
            "condensing_heat_MW": Q_avail / 1e6,
            "exergy_rate_MW": X_in / 1e6,
            "exergy_to_energy_ratio": X_in / E_total,
        },
        "heating_mode": {
            "hx_duty_MW": Q_hx / 1e6,
            "useful_heat_MW": Q_useful / 1e6,
            "distribution_loss_MW": Q_dist_loss / 1e6,
            "steam_to_hx_kg_s": m_hx,
            "steam_to_trim_condenser_kg_s": m_trim,
            "trim_condenser_duty_MW": Q_trim / 1e6,
            "hot_water_flow_kg_s": m_hw,
            "cooling_water_flow_kg_s": m_cw_heating,
        },
        "cooling_mode": {
            "condenser_duty_MW": Q_avail / 1e6,
            "cooling_water_flow_kg_s": m_cw_max,
        },
        "pumps": {
            "condensate_pump_kW": W_cond_pump / 1e3,
            "hot_water_pump_kW": W_hw_pump / 1e3,
            "vacuum_pump_kW": inp.vacuum_pump_kW,
        },
        "exergy": {
            "inlet_MW": X_in / 1e6,
            "to_hot_water_MW": X_to_hw / 1e6,
            "destroyed_hx_MW": X_dest_hx / 1e6,
            "lost_trim_condenser_MW": X_lost_trim / 1e6,
            "condensate_retained_MW": X_condensate / 1e6,
            "destroyed_pump_MW": X_dest_pump / 1e6,
            "second_law_eff_hx": eta_II_hx,
            "lost_cooling_mode_MW": X_lost_cooling_mode / 1e6,
        },
        "equipment": equipment,
        "economics": {
            "heating_kWh_yr": heat_kWh,
            "heating_value_usd": heat_value,
            "water_gal_per_h": gal_per_h,
            "water_gal_yr": water_gal_yr,
            "water_value_usd": water_value,
            "parasitic_kWh_yr": parasitic_kWh,
            "parasitic_cost_usd": parasitic_cost,
            "gross_benefit_usd": gross,
            "net_benefit_usd": net,
            "total_stream_energy_kWh_yr": total_energy_kWh,
            "useful_fraction_of_total_energy": heat_kWh / total_energy_kWh,
        },
        "warnings": warnings,
    }


def sensitivity(inp: Inputs, points: int = 21) -> dict:
    """Net annual benefit vs building load for several recovery efficiencies."""
    base = analyze(inp)
    q_max = base["baseline"]["condensing_heat_MW"]
    loads = [q_max * i / (points - 1) for i in range(points)]
    curves = []
    for eff in (0.70, 0.85, 0.95):
        net = []
        for L in loads:
            r = analyze(replace(inp, building_load_MW=L, recovery_efficiency=eff))
            net.append(r["economics"]["net_benefit_usd"])
        curves.append({"recovery_efficiency": eff, "net_benefit_usd": net})
    return {"building_load_MW": loads, "curves": curves}
