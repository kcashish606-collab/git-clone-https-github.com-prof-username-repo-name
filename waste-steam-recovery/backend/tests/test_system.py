from dataclasses import replace

import pytest

from steamrec.system import Inputs, analyze

BASE = Inputs()


@pytest.fixture(scope="module")
def result():
    return analyze(BASE)


def test_saturation_temperature(result):
    # T_sat at 3.8 psia is about 150.8 °F (steam tables)
    assert result["baseline"]["T_sat_F"] == pytest.approx(150.8, abs=0.3)


def test_inlet_is_superheated(result):
    assert result["baseline"]["superheat_F"] > 70
    assert result["states"][1]["x"] is None


def test_condensing_heat(result):
    assert result["baseline"]["condensing_heat_MW"] == pytest.approx(19.7, rel=0.01)


def test_exergy_much_smaller_than_energy(result):
    b = result["baseline"]
    assert 0.05 < b["exergy_to_energy_ratio"] < 0.2


def test_exergy_balance_closes(result):
    x = result["exergy"]
    out = x["to_hot_water_MW"] + x["destroyed_hx_MW"] + x["lost_trim_condenser_MW"] + x["condensate_retained_MW"]
    assert out == pytest.approx(x["inlet_MW"], rel=1e-6)
    assert x["destroyed_hx_MW"] > 0


def test_energy_balance_heating_mode(result):
    h, b = result["heating_mode"], result["baseline"]
    assert h["hx_duty_MW"] + h["trim_condenser_duty_MW"] == pytest.approx(b["condensing_heat_MW"], rel=1e-9)
    assert h["useful_heat_MW"] == pytest.approx(BASE.building_load_MW)


def test_water_value(result):
    # 64,500 lbm/h / 8.34 lbm/gal × 8,000 h × $0.70/100 gal ≈ $433k
    assert result["economics"]["water_value_usd"] == pytest.approx(433_000, rel=0.01)


def test_no_heating_credit_without_heating_hours():
    r = analyze(replace(BASE, heating_hours=0))
    assert r["economics"]["heating_value_usd"] == 0
    assert r["economics"]["water_value_usd"] > 0


def test_heating_is_steam_limited():
    r = analyze(replace(BASE, building_load_MW=50))
    assert r["heating_mode"]["useful_heat_MW"] < r["baseline"]["condensing_heat_MW"]
    assert any("steam-limited" in w for w in r["warnings"])


def test_infeasible_supply_temperature_warns():
    r = analyze(replace(BASE, hw_supply_F=148))
    assert any("infeasible" in w for w in r["warnings"])


def test_invalid_hours_rejected():
    with pytest.raises(ValueError):
        analyze(replace(BASE, heating_hours=9000, operating_hours=8000))
