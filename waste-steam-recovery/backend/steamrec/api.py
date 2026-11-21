"""FastAPI backend: JSON API plus static hosting of the frontend dashboard."""

from __future__ import annotations

from dataclasses import asdict, fields
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import __version__
from .system import Inputs, analyze, sensitivity

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

app = FastAPI(
    title="Waste Steam Recovery API",
    version=__version__,
    description="Energy, exergy and economic model for combined heating + condensate recovery.",
)

_defaults = Inputs()


class InputsModel(BaseModel):
    """Request body. Every field is optional and falls back to the project defaults."""

    steam_flow_lbm_h: float = Field(_defaults.steam_flow_lbm_h, gt=0)
    steam_pressure_psia: float = Field(_defaults.steam_pressure_psia, gt=0.2, lt=14.6)
    steam_temp_F: float = Field(_defaults.steam_temp_F, gt=60, lt=700)
    dead_temp_F: float = Field(_defaults.dead_temp_F, gt=0, lt=120)
    dead_pressure_psia: float = Field(_defaults.dead_pressure_psia, gt=10, lt=16)
    building_load_MW: float = Field(_defaults.building_load_MW, ge=0, le=100)
    recovery_efficiency: float = Field(_defaults.recovery_efficiency, gt=0, le=1)
    hw_return_F: float = Field(_defaults.hw_return_F, gt=40, lt=210)
    hw_supply_F: float = Field(_defaults.hw_supply_F, gt=40, lt=210)
    hw_loop_pressure_psia: float = Field(_defaults.hw_loop_pressure_psia, gt=14, lt=200)
    hw_pump_dp_psi: float = Field(_defaults.hw_pump_dp_psi, ge=0, lt=200)
    hx_U_W_m2K: float = Field(_defaults.hx_U_W_m2K, gt=0)
    cw_in_F: float = Field(_defaults.cw_in_F, gt=40, lt=150)
    cw_out_F: float = Field(_defaults.cw_out_F, gt=40, lt=150)
    condenser_U_W_m2K: float = Field(_defaults.condenser_U_W_m2K, gt=0)
    cooling_tower_kW_per_MW: float = Field(_defaults.cooling_tower_kW_per_MW, ge=0, le=100)
    pump_outlet_psia: float = Field(_defaults.pump_outlet_psia, gt=0, lt=500)
    pump_efficiency: float = Field(_defaults.pump_efficiency, gt=0, le=1)
    vacuum_pump_kW: float = Field(_defaults.vacuum_pump_kW, ge=0)
    operating_hours: float = Field(_defaults.operating_hours, gt=0, le=8760)
    heating_hours: float = Field(_defaults.heating_hours, ge=0, le=8760)
    electricity_price: float = Field(_defaults.electricity_price, ge=0)
    heat_price: float = Field(_defaults.heat_price, ge=0)
    water_price_per_100gal: float = Field(_defaults.water_price_per_100gal, ge=0)

    def to_inputs(self) -> Inputs:
        return Inputs(**{f.name: getattr(self, f.name) for f in fields(Inputs)})


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.get("/api/defaults")
def defaults() -> dict:
    return asdict(_defaults)


@app.post("/api/analyze")
def analyze_endpoint(body: InputsModel) -> dict:
    try:
        inp = body.to_inputs()
        result = analyze(inp)
        result["sensitivity"] = sensitivity(inp)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
