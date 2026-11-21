"""Command-line summary: python -m steamrec.cli [--load 5 --eff 0.85 --json]."""

from __future__ import annotations

import argparse
import json

from .system import Inputs, analyze


def main() -> None:
    p = argparse.ArgumentParser(description="Waste steam recovery: heating + condensate (Option D)")
    p.add_argument("--load", type=float, default=Inputs.building_load_MW, help="building heat load [MW]")
    p.add_argument("--eff", type=float, default=Inputs.recovery_efficiency, help="recovery efficiency [-]")
    p.add_argument("--json", action="store_true", help="print full JSON result")
    a = p.parse_args()

    r = analyze(Inputs(building_load_MW=a.load, recovery_efficiency=a.eff))
    if a.json:
        print(json.dumps(r, indent=2))
        return

    b, h, x, e = r["baseline"], r["heating_mode"], r["exergy"], r["economics"]
    print("=== Baseline ===")
    print(f"  Mass flow            {b['mass_flow_kg_s']:.3f} kg/s")
    print(f"  T_sat / superheat    {b['T_sat_F']:.1f} °F / {b['superheat_F']:.1f} °F")
    print(f"  Energy rate (vs T0)  {b['energy_rate_MW']:.2f} MW")
    print(f"  Condensing heat      {b['condensing_heat_MW']:.2f} MW")
    print(f"  Exergy rate          {b['exergy_rate_MW']:.2f} MW")
    print("=== Heating mode ===")
    print(f"  HX duty / useful     {h['hx_duty_MW']:.2f} / {h['useful_heat_MW']:.2f} MW")
    print(f"  2nd-law eff (HX)     {x['second_law_eff_hx']*100:.1f} %")
    print("=== Annual economics ===")
    print(f"  Heating value        ${e['heating_value_usd']:,.0f}")
    print(f"  Water value          ${e['water_value_usd']:,.0f}")
    print(f"  Parasitic electricity -${e['parasitic_cost_usd']:,.0f}")
    print(f"  NET BENEFIT          ${e['net_benefit_usd']:,.0f} /yr")
    for w in r["warnings"]:
        print(f"  WARNING: {w}")


if __name__ == "__main__":
    main()
