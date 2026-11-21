// Waste Steam Recovery dashboard: talks to the FastAPI backend at /api.

const API = "/api";
const form = document.getElementById("inputs-form");
const statusEl = document.getElementById("status");
const charts = {};
let defaults = {};
let debounceTimer;

const fmt = {
  mw: (v) => `${v.toFixed(2)} MW`,
  usd: (v) => (Math.abs(v) >= 1e6 ? `$${(v / 1e6).toFixed(2)} M` : `$${Math.round(v / 1e3)} k`),
  num: (v, d = 2) => (v === null || v === undefined ? "–" : Number(v).toFixed(d)),
};

const COLORS = {
  steam: "#ff7a45", hot: "#ffb020", cold: "#38bdf8", green: "#34d399",
  violet: "#a78bfa", red: "#f87171", muted: "#93a4bd", grid: "#26364f",
};

function setStatus(text, cls) {
  statusEl.textContent = text;
  statusEl.className = `pill ${cls || ""}`;
}

function readForm() {
  const body = {};
  for (const el of form.elements) {
    if (el.name && el.value !== "") body[el.name] = Number(el.value);
  }
  return body;
}

function fillForm(values) {
  for (const el of form.elements) {
    if (el.name && el.name in values) el.value = values[el.name];
  }
  syncOutputs();
}

function syncOutputs() {
  form.querySelectorAll("output[data-for]").forEach((o) => {
    const input = form.elements[o.dataset.for];
    o.textContent = input.name === "recovery_efficiency"
      ? `${Math.round(input.value * 100)}%`
      : Number(input.value).toFixed(2);
  });
}

async function analyze() {
  setStatus("Calculating…");
  try {
    const res = await fetch(`${API}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(readForm()),
    });
    const data = await res.json();
    if (!res.ok) {
      const msg = Array.isArray(data.detail)
        ? data.detail.map((d) => `${d.loc.at(-1)}: ${d.msg}`).join("; ")
        : data.detail;
      throw new Error(msg);
    }
    render(data);
    setStatus("Model up to date", "ok");
  } catch (err) {
    setStatus("Input error", "err");
    document.getElementById("warnings").innerHTML = `<div class="warn">${err.message}</div>`;
  }
}

function render(d) {
  const { baseline: b, heating_mode: h, economics: e, exergy: x } = d;

  document.getElementById("k-cond").textContent = fmt.mw(b.condensing_heat_MW);
  document.getElementById("k-exergy").textContent = fmt.mw(b.exergy_rate_MW);
  document.getElementById("k-heat").textContent = fmt.mw(h.useful_heat_MW);
  document.getElementById("k-water").textContent = `${Math.round(e.water_gal_per_h).toLocaleString()} gal/h`;
  document.getElementById("k-net").textContent = `${fmt.usd(e.net_benefit_usd)} /yr`;
  document.getElementById("prop-src").textContent = d.property_source;

  document.getElementById("warnings").innerHTML =
    d.warnings.map((w) => `<div class="warn">⚠ ${w}</div>`).join("");

  renderStates(d.states);
  renderEquipment(d.equipment);
  renderEcon(e);
  renderExergy(x);
  renderSensitivity(d.sensitivity, d.inputs.building_load_MW);
}

function renderStates(states) {
  const head = `<tr><th>State</th><th>Description</th><th>P (psia)</th><th>T (°F)</th>
    <th>h (kJ/kg)</th><th>s (kJ/kg·K)</th><th>v (m³/kg)</th><th>x</th></tr>`;
  const rows = states.map((s) => `<tr>
      <td class="tag">${s.label}</td><td>${s.description}</td>
      <td class="num">${fmt.num(s.P_psia, 2)}</td><td class="num">${fmt.num(s.T_F, 1)}</td>
      <td class="num">${fmt.num(s.h_kJ_kg, 1)}</td><td class="num">${fmt.num(s.s_kJ_kgK, 4)}</td>
      <td class="num">${s.v_m3_kg > 0.1 ? fmt.num(s.v_m3_kg, 3) : s.v_m3_kg.toExponential(3)}</td>
      <td class="num">${s.x === null ? "–" : fmt.num(s.x, 3)}</td></tr>`).join("");
  document.getElementById("states-table").innerHTML = head + rows;
}

function renderEquipment(items) {
  const head = `<tr><th>Tag</th><th>Equipment</th><th>Preliminary specification</th></tr>`;
  const rows = items.map((i) =>
    `<tr><td class="tag">${i.tag}</td><td>${i.name}</td><td>${i.spec}</td></tr>`).join("");
  document.getElementById("equip-table").innerHTML = head + rows;
}

function upsertChart(id, config) {
  if (charts[id]) {
    charts[id].data = config.data;
    charts[id].options = config.options;
    charts[id].update();
  } else {
    charts[id] = new Chart(document.getElementById(id), config);
  }
}

const baseScales = (yTitle) => ({
  x: { ticks: { color: COLORS.muted }, grid: { color: COLORS.grid } },
  y: { ticks: { color: COLORS.muted }, grid: { color: COLORS.grid },
       title: { display: !!yTitle, text: yTitle, color: COLORS.muted } },
});

function renderEcon(e) {
  upsertChart("econ-chart", {
    type: "bar",
    data: {
      labels: ["Space heating", "Recovered water", "Parasitic power", "Net"],
      datasets: [{
        data: [e.heating_value_usd, e.water_value_usd, -e.parasitic_cost_usd, e.net_benefit_usd].map((v) => v / 1e3),
        backgroundColor: [COLORS.hot, COLORS.cold, COLORS.red, COLORS.green],
        borderRadius: 8,
      }],
    },
    options: {
      plugins: { legend: { display: false },
        tooltip: { callbacks: { label: (c) => `$${Math.round(c.raw).toLocaleString()} k/yr` } } },
      scales: baseScales("k$/yr"),
    },
  });
}

function renderExergy(x) {
  upsertChart("exergy-chart", {
    type: "doughnut",
    data: {
      labels: ["To hot water", "Destroyed in HX", "Lost in trim condenser", "Retained in condensate"],
      datasets: [{
        data: [x.to_hot_water_MW, x.destroyed_hx_MW, x.lost_trim_condenser_MW, x.condensate_retained_MW],
        backgroundColor: [COLORS.hot, COLORS.steam, COLORS.violet, COLORS.cold],
        borderColor: "#151f30", borderWidth: 3,
      }],
    },
    options: {
      cutout: "58%",
      plugins: {
        legend: { position: "right", labels: { color: "#e6edf7" } },
        tooltip: { callbacks: { label: (c) => `${c.label}: ${c.raw.toFixed(3)} MW` } },
        title: { display: true, color: COLORS.muted,
          text: `Inlet ${x.inlet_MW.toFixed(2)} MW · η_II,HX = ${(x.second_law_eff_hx * 100).toFixed(1)}%` },
      },
    },
  });
}

function renderSensitivity(s, currentLoad) {
  const palette = [COLORS.violet, COLORS.hot, COLORS.green];
  upsertChart("sens-chart", {
    type: "line",
    data: {
      labels: s.building_load_MW.map((v) => v.toFixed(1)),
      datasets: s.curves.map((c, i) => ({
        label: `Recovery η = ${Math.round(c.recovery_efficiency * 100)}%`,
        data: c.net_benefit_usd.map((v) => v / 1e6),
        borderColor: palette[i], backgroundColor: palette[i],
        tension: 0.25, pointRadius: 0, borderWidth: 2.5,
      })),
    },
    options: {
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { labels: { color: "#e6edf7" } },
        title: { display: true, color: COLORS.muted, text: `Current building load: ${currentLoad.toFixed(2)} MW` },
      },
      scales: {
        ...baseScales("Net benefit (M$/yr)"),
        x: { ...baseScales().x, title: { display: true, text: "Building heat load (MW)", color: COLORS.muted } },
      },
    },
  });
}

form.addEventListener("input", () => {
  syncOutputs();
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(analyze, 300);
});

document.getElementById("reset-btn").addEventListener("click", () => {
  fillForm(defaults);
  analyze();
});

async function init() {
  try {
    defaults = await (await fetch(`${API}/defaults`)).json();
    fillForm(defaults);
    await analyze();
  } catch {
    setStatus("Backend offline", "err");
  }
}

window.addEventListener("DOMContentLoaded", init);
