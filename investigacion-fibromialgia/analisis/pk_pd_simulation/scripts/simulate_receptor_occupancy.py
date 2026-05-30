#!/usr/bin/env python3
"""
Pramipexole PK/PD Simulator - DRD2 vs. DRD3 Receptor Occupancy
Simulates peripheral DRD2 (PBMCs) vs. central limbic DRD3 receptor occupancy
under low-dose Fibromyalgia (0.125 - 1.0 mg/day) and high-dose Parkinson (3.0 mg/day) regimens.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Create output directories
os.makedirs("plots", exist_ok=True)

# ---------------------------------------------------------
# CONSTANTS & PARAMETERS
# ---------------------------------------------------------
MW_BASE = 211.27  # g/mol (Pramipexole base)
# Pramipexole is typically dosed as pramipexole dihydrochloride monohydrate (MW 302.26 g/mol)
# In clinical settings, doses can be expressed in terms of salt or base.
# Let's assume the doses provided are base equivalent (standard modern clinical labeling).
# To convert plasma concentration C_plasma (ng/mL) to nM:
# C_nM = C_plasma (ug/L) / MW_base (g/mol) * 10^3 = C_plasma * (1000 / 211.27) = C_plasma * 4.733

# PK parameters (Human literature values)
F = 0.90          # Bioavailability (>= 90%)
T_HALF = 8.0      # Half-life (hours)
VD = 500.0        # Volume of distribution (L)
KE = np.log(2) / T_HALF  # Elimination rate constant (h^-1) ~ 0.0866
CL = KE * VD      # Clearance (L/h) ~ 43.3
KA = 1.5          # Absorption rate constant (h^-1) - typical IR Tmax ~ 1-2 hours
KP = 8.0          # Brain-to-plasma partition coefficient (rodent/human tissue ratio ~ 8.0)

# PD parameters (Receptor affinities in nM)
KD_D2 = 3.0       # DRD2 (Periphery, PBMCs) Kd in nM
KD_D3 = 0.5       # DRD3 (Central, Limbic) Kd in nM

# Doses to simulate (in mg of pramipexole base per day)
DOSES_FM = [0.125, 0.250, 0.500, 1.0]  # Fibromyalgia (QD - once daily)
DOSE_PD = 3.0                          # Parkinson's (TID - 1.0 mg three times daily)

SIM_DAYS = 7
T_MAX_SIM = SIM_DAYS * 24  # 168 hours
DT = 0.05                 # Simulation time step (hours)
TIME_STEPS = np.arange(0, T_MAX_SIM + DT, DT)

# ---------------------------------------------------------
# PK MODEL SOLVER (1-Compartment, Oral Multi-dose)
# ---------------------------------------------------------
def simulate_pk(dose_mg, interval_h, total_hours, dose_times=None):
    """
    Simulates plasma concentration of Pramipexole over time using an analytical
    1-compartment model with first-order absorption and elimination.
    """
    if dose_times is None:
        dose_times = np.arange(0, total_hours, interval_h)
        
    C_plasma = np.zeros_like(TIME_STEPS)
    
    # Superposition of multiple doses
    for d_time in dose_times:
        # Time relative to this specific dose
        t_rel = TIME_STEPS - d_time
        mask = t_rel >= 0
        
        # Dose in micrograms (to get ng/mL in 500 L)
        dose_ug = dose_mg * 1000.0
        
        # Analytical 1-compartment open model equation for single oral dose:
        # C(t) = (F * Dose * Ka) / (Vd * (Ka - Ke)) * (exp(-Ke * t) - exp(-Ka * t))
        coeff = (F * dose_ug * KA) / (VD * (KA - KE))
        C_single = coeff * (np.exp(-KE * t_rel[mask]) - np.exp(-KA * t_rel[mask]))
        C_plasma[mask] += C_single
        
    return C_plasma

# ---------------------------------------------------------
# PD MODEL (Receptor Occupancy)
# ---------------------------------------------------------
def compute_occupancy(C_plasma_ng_ml):
    """
    Computes occupancy for DRD2 in PBMCs and DRD3 in Brain.
    """
    # Convert ng/mL to nM
    C_plasma_nM = C_plasma_ng_ml * (1000.0 / MW_BASE)
    
    # PBMCs Periphery (DRD2): Occupancy = C_plasma / (Kd_D2 + C_plasma)
    occ_D2 = (C_plasma_nM / (KD_D2 + C_plasma_nM)) * 100.0
    
    # Brain Limbic (DRD3): Occupancy = (C_plasma * Kp) / (Kd_D3 + C_plasma * Kp)
    C_brain_nM = C_plasma_nM * KP
    occ_D3 = (C_brain_nM / (KD_D3 + C_brain_nM)) * 100.0
    
    return occ_D2, occ_D3

# ---------------------------------------------------------
# RUN SIMULATIONS
# ---------------------------------------------------------
results = {}

# Simulate Fibromyalgia Doses (QD - Once Daily at t = 0, 24, 48, ...)
for dose in DOSES_FM:
    C_plasma = simulate_pk(dose, 24.0, T_MAX_SIM)
    occ_D2, occ_D3 = compute_occupancy(C_plasma)
    results[f"FM_{dose}mg"] = {
        "dose": dose,
        "regimen": "QD",
        "C_plasma": C_plasma,
        "occ_D2": occ_D2,
        "occ_D3": occ_D3
    }

# Simulate Parkinson's Dose (TID - 1.0 mg every 8 hours)
C_plasma_PD = simulate_pk(1.0, 8.0, T_MAX_SIM)
occ_D2_PD, occ_D3_PD = compute_occupancy(C_plasma_PD)
results["PD_3.0mg"] = {
    "dose": 3.0,
    "regimen": "1.0mg TID",
    "C_plasma": C_plasma_PD,
    "occ_D2": occ_D2_PD,
    "occ_D3": occ_D3_PD
}

# ---------------------------------------------------------
# STYLISH GRAPHICS GENERATION (Matplotlib)
# ---------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16,
    'lines.linewidth': 2.0
})

# Color palette definition
COLORS = {
    "D2_periphery": "#00ADB5",  # Cyan/Teal
    "D3_central": "#FF2E63",     # Vibrant Rose/Pink
    "plasma": "#303841",         # Dark Charcoal
    "safety_bg": "#EAEAEA",
    "FM_doses": ["#A6D1C9", "#4DB3A2", "#1E8272", "#0A4E44"]
}

# Plot 1: Steady-state Profile over last 24 hours (Days 6 to 7)
fig, axes = plt.subplots(3, 2, figsize=(15, 12), sharex='col', sharey='row')
fig.suptitle("Pramipexole Dynamic PK/PD: Steady-State Receptor Occupancy", y=0.98, fontweight='bold')

# We look at the last 24 hours (hours 144 to 168)
ss_mask = (TIME_STEPS >= 144) & (TIME_STEPS <= 168)
t_ss = TIME_STEPS[ss_mask] - 144  # Normalized to 0-24h

fm_keys = [f"FM_{d}mg" for d in DOSES_FM]

# Row 1: Fibromyalgia Low Doses (e.g. 0.125 mg QD vs 1.0 mg QD)
# Col 1: 0.125 mg QD (Typical starting dose)
r1_c1_data = results["FM_0.125mg"]
axes[0, 0].plot(t_ss, r1_c1_data["occ_D3"][ss_mask], color=COLORS["D3_central"], label="Central DRD3 (Limbic)")
axes[0, 0].plot(t_ss, r1_c1_data["occ_D2"][ss_mask], color=COLORS["D2_periphery"], label="Peripheral DRD2 (PBMCs)")
axes[0, 0].set_title("Fibromyalgia Starting Dose: 0.125 mg QD (Steady State)", fontweight='bold')
axes[0, 0].set_ylabel("Occupancy (%)")
axes[0, 0].legend(loc="right")
axes[0, 0].set_ylim(0, 100)

# Col 2: 1.0 mg QD (Highest FM target dose)
r1_c2_data = results["FM_1.0mg"]
axes[0, 2 - 1].plot(t_ss, r1_c2_data["occ_D3"][ss_mask], color=COLORS["D3_central"])
axes[0, 2 - 1].plot(t_ss, r1_c2_data["occ_D2"][ss_mask], color=COLORS["D2_periphery"])
axes[0, 2 - 1].set_title("Fibromyalgia Target Dose: 1.0 mg QD (Steady State)", fontweight='bold')
axes[0, 2 - 1].set_ylim(0, 100)

# Row 2: Parkinson's High Dose (3.0 mg/day TID, i.e., 1.0 mg Q8H)
r2_data = results["PD_3.0mg"]
# Plot TID on both columns or spanning
# Let's plot the TID profile over last 24 hours (hours 144 to 168)
axes[1, 0].plot(t_ss, r2_data["occ_D3"][ss_mask], color=COLORS["D3_central"], label="Central DRD3")
axes[1, 0].plot(t_ss, r2_data["occ_D2"][ss_mask], color=COLORS["D2_periphery"], label="Peripheral DRD2")
axes[1, 0].set_title("Parkinson's Standard Dose: 3.0 mg/day (1.0 mg TID)", fontweight='bold')
axes[1, 0].set_ylabel("Occupancy (%)")
axes[1, 0].set_ylim(0, 100)

# Right plot on Row 2: Comparison of DRD3 occupancy across all Fibromyalgia doses
for idx, key in enumerate(fm_keys):
    axes[1, 1].plot(t_ss, results[key]["occ_D3"][ss_mask], label=f"{DOSES_FM[idx]} mg QD", color=COLORS["FM_doses"][idx])
axes[1, 1].plot(t_ss, r2_data["occ_D3"][ss_mask], label="3.0 mg TID (PD)", color="black", linestyle="--")
axes[1, 1].set_title("Central DRD3 Occupancy Comparison", fontweight='bold')
axes[1, 1].legend(loc="lower right")
axes[1, 1].set_ylim(0, 100)

# Row 3: Selectivity Delta Window (Occupancy_D3 - Occupancy_D2)
# Col 1: Delta for 0.125 mg QD vs 1.0 mg QD
delta_0125 = results["FM_0.125mg"]["occ_D3"][ss_mask] - results["FM_0.125mg"]["occ_D2"][ss_mask]
delta_10 = results["FM_1.0mg"]["occ_D3"][ss_mask] - results["FM_1.0mg"]["occ_D2"][ss_mask]
axes[2, 0].plot(t_ss, delta_0125, color="#8F43EE", label="0.125 mg QD")
axes[2, 0].plot(t_ss, delta_10, color="#2D033B", label="1.0 mg QD")
axes[2, 0].set_title("Selectivity Delta (Central D3 - Peripheral D2)", fontweight='bold')
axes[2, 0].set_xlabel("Time at Steady State (hours)")
axes[2, 0].set_ylabel("Delta Occupancy (%)")
axes[2, 0].legend()
axes[2, 0].set_ylim(0, 100)

# Col 2: Delta comparison for Parkinson's 3.0 mg TID
delta_PD = r2_data["occ_D3"][ss_mask] - r2_data["occ_D2"][ss_mask]
axes[2, 1].plot(t_ss, delta_PD, color="black", linestyle="--", label="3.0 mg TID")
# Add the intermediate FM doses delta
axes[2, 1].plot(t_ss, results["FM_0.25mg"]["occ_D3"][ss_mask] - results["FM_0.25mg"]["occ_D2"][ss_mask], color=COLORS["FM_doses"][1], label="0.250 mg QD")
axes[2, 1].plot(t_ss, results["FM_0.5mg"]["occ_D3"][ss_mask] - results["FM_0.5mg"]["occ_D2"][ss_mask], color=COLORS["FM_doses"][2], label="0.500 mg QD")
axes[2, 1].set_title("Selectivity Delta Comparison", fontweight='bold')
axes[2, 1].set_xlabel("Time at Steady State (hours)")
axes[2, 1].legend()
axes[2, 1].set_ylim(0, 100)

plt.tight_layout()
plt.savefig("plots/steady_state_occupancy_profile.png", dpi=300)
plt.close()

# Plot 2: Safety Window / Selectivity Threshold Analysis
# We want to plot the steady-state mean, min, and max occupancy for D3 and D2 as a function of daily dose.
daily_doses = DOSES_FM + [3.0]
labels = [f"{d}\n(QD)" for d in DOSES_FM] + ["3.0\n(TID)"]

d3_means = []
d3_mins = []
d3_maxs = []

d2_means = []
d2_mins = []
d2_maxs = []

for key in fm_keys + ["PD_3.0mg"]:
    d3_means.append(np.mean(results[key]["occ_D3"][ss_mask]))
    d3_mins.append(np.min(results[key]["occ_D3"][ss_mask]))
    d3_maxs.append(np.max(results[key]["occ_D3"][ss_mask]))
    
    d2_means.append(np.mean(results[key]["occ_D2"][ss_mask]))
    d2_mins.append(np.min(results[key]["occ_D2"][ss_mask]))
    d2_maxs.append(np.max(results[key]["occ_D2"][ss_mask]))

plt.figure(figsize=(10, 6))
# DRD3 central curves
plt.errorbar(range(len(daily_doses)), d3_means, 
             yerr=[np.array(d3_means)-np.array(d3_mins), np.array(d3_maxs)-np.array(d3_means)], 
             fmt='-o', color=COLORS["D3_central"], capsize=6, elinewidth=2, label="Central DRD3 (Limbic)")
# DRD2 peripheral curves
plt.errorbar(range(len(daily_doses)), d2_means, 
             yerr=[np.array(d2_means)-np.array(d2_mins), np.array(d2_maxs)-np.array(d2_means)], 
             fmt='-o', color=COLORS["D2_periphery"], capsize=6, elinewidth=2, label="Peripheral DRD2 (PBMCs)")

plt.xticks(range(len(daily_doses)), labels)
plt.xlabel("Daily Dose of Pramipexole (mg / regimen)")
plt.ylabel("Steady-State Occupancy (%)")
plt.title("Pramipexole Safety & Selectivity Window: Central DRD3 vs. Peripheral DRD2", fontweight='bold', pad=15)
plt.ylim(-5, 105)
plt.legend(loc="lower right")

# Annotate safety window (delta)
for i, (d3_m, d2_m) in enumerate(zip(d3_means, d2_means)):
    delta = d3_m - d2_m
    plt.annotate(f"Δ={delta:.1f}%", (i, (d3_m + d2_m)/2), textcoords="offset points", 
                 xytext=(15, -5), ha='center', fontweight='bold', color="#6C00FF", fontsize=9,
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#6C00FF", lw=0.5, alpha=0.8))

plt.tight_layout()
plt.savefig("plots/safety_window_dose_response.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# GENERATE JSON SUMMARY FOR CLINICAL REPORT
# ---------------------------------------------------------
print("PK/PD Simulation Completed Successfully!")
print(f"Figures exported to 'plots/steady_state_occupancy_profile.png' and 'plots/safety_window_dose_response.png'.")

for dose_lbl, key in zip(["0.125mg QD", "0.250mg QD", "0.500mg QD", "1.0mg QD", "3.0mg TID"], fm_keys + ["PD_3.0mg"]):
    d3_m = np.mean(results[key]["occ_D3"][ss_mask])
    d2_m = np.mean(results[key]["occ_D2"][ss_mask])
    print(f"Regimen: {dose_lbl:10} | Mean Central DRD3: {d3_m:5.2f}% | Mean Peripheral DRD2: {d2_m:5.2f}% | Delta Selectivity: {(d3_m-d2_m):5.2f}%")
