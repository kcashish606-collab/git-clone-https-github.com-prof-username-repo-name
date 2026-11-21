"""Unit conversions between US customary (project inputs) and SI (calculations)."""

PSI_TO_PA = 6894.757
LBM_TO_KG = 0.45359237
M3_TO_GAL = 264.172
W_TO_BTU_H = 3.412142
KG_S_TO_LBM_H = 3600.0 / LBM_TO_KG
M3_S_TO_GPM = M3_TO_GAL * 60.0


def f_to_k(t_f: float) -> float:
    return (t_f - 32.0) / 1.8 + 273.15


def k_to_f(t_k: float) -> float:
    return (t_k - 273.15) * 1.8 + 32.0


def psia_to_pa(p_psia: float) -> float:
    return p_psia * PSI_TO_PA


def pa_to_psia(p_pa: float) -> float:
    return p_pa / PSI_TO_PA


def lbm_h_to_kg_s(m_lbm_h: float) -> float:
    return m_lbm_h * LBM_TO_KG / 3600.0
