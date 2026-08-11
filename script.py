"""
Validation Script: Archachatina marginata Endotoxin Kit
==========================================================
Built from the ACTUAL project data (SUMMARY_of_project_experiment.xlsx)

PART A: Protein Coagulation Assay
  - Reproduce the calibration curve from Sheet5 ("Final coagulation reaction for plasma")
  - Apply it to the real IVF results (Sheet7)
  - Compare against the original paper's reported curve (y = 0.0109x + 0.0644)
    and Table 1 results

PART B: Phenoloxidase Kinetic Assay
  - Reproduce the calibration curve from Sheet8 (EU vs absorbance/min)
  - Apply it to the phenoloxidase IVF data (Sheet9) -- this wasn't in the
    original paper's results chapter, so this is a genuinely new analysis
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# =====================================================================
# PART A: PROTEIN COAGULATION ASSAY
# =====================================================================

print("=" * 70)
print("PART A: PROTEIN COAGULATION ASSAY")
print("=" * 70)

# --- A1. Calibration data, taken directly from Sheet5 ---
# ("Final coagulation reaction for plasma" -- EU vs mean change in absorbance)
pc_eu = np.array([0, 1, 2, 4, 5, 7, 8, 9, 10])
pc_abs = np.array([0, 0.122, 0.146, 0.066, 0.108, 0.104, 0.216, 0.192, 0.126])

slope, intercept, r_value, p_value, std_err = stats.linregress(pc_eu, pc_abs)

print("\n--- A1. Calibration curve (from Sheet5 raw data) ---")
print(f"  Our calculated equation : y = {slope:.4f}x + {intercept:.4f}")
print(f"  Paper's reported equation: y = 0.0109x + 0.0644")
print(f"  R^2 of our fit          : {r_value**2:.4f}")
print("  NOTE: R^2 is low -- the plasma data is noisy across EU levels,")
print("  which the original paper does not report R^2 for either.")
print("  This is worth flagging to your supervisor: the fit is real but weak.")

# --- A2. Apply calibration curve to real IVF data (Sheet7) ---
ivf_names = [
    "Dextrose 5% 78", "Dextrose 5% 79", "Dextrose 4.3% 84", "Dextrose 4.3% 82",
    "Dextrose 5% 00", "Dextrose 5% 98", "normal Saline 11", "normal Saline 12",
]
ivf_abs = np.array([0.015, 0, 0, 0, 0.009, 0, 0, 0])

# solve y = mx + c for x  ->  x = (y - c) / m
ivf_estimated_eu = (ivf_abs - intercept) / slope

print("\n--- A2. IVF endotoxin estimates (protein coagulation) ---")
print(f"{'Batch':<20}{'Absorbance':>12}{'Estimated EU/mL':>18}")
for name, abs_val, eu in zip(ivf_names, ivf_abs, ivf_estimated_eu):
    print(f"{name:<20}{abs_val:>12.4f}{eu:>18.2f}")

print("\n  Original paper (Table 1) reported all IVFs as negative x-values")
print("  (i.e. below detection, inferred as 0 EU/mL). Our script reproduces")
print("  this pattern: all estimates are negative or near-zero, consistent")
print("  with 'no detectable endotoxin' -- matching the original conclusion.")

# =====================================================================
# PART B: PHENOLOXIDASE KINETIC ASSAY
# =====================================================================

print("\n" + "=" * 70)
print("PART B: PHENOLOXIDASE KINETIC ASSAY")
print("=" * 70)

# --- B1. Calibration data, taken directly from Sheet8 ---
# (EU standards vs absorbance/min, already calculated in the raw sheet)
po_eu = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
po_rate = np.array([0.04, 0.0282, 0.0338, 0.031, 0.0327, 0.0345,
                     0.0346, 0.0353, 0.0456, 0.0593, 0.0484])

slope_po, intercept_po, r_po, p_po, se_po = stats.linregress(po_eu, po_rate)

print("\n--- B1. Calibration curve (phenoloxidase, from Sheet8) ---")
print(f"  Equation : y = {slope_po:.5f}x + {intercept_po:.4f}")
print(f"  R^2      : {r_po**2:.4f}")
print("  NOTE: This curve was NOT reported anywhere in the original PDF --")
print("  the paper only used the protein coagulation assay for its main")
print("  results. This is a genuinely new calibration, not a reproduction.")

# --- B2. Apply to phenoloxidase IVF data (Sheet9) ---
po_ivf_names = [
    "Dextrose 5% 78", "Dextrose 5% 79", "Dextrose 4.3% 84", "Dextrose 4.3% 82",
    "Dextrose 5% 00", "Dextrose 5% 98", "normal Saline 11", "normal Saline 12", "MET",
]
po_ivf_abs = np.array([0, 0.055, 0.048, 0.043, 0.072, 0.156, 0.04, 0.055, 0.032])

po_ivf_estimated_eu = (po_ivf_abs - intercept_po) / slope_po

print("\n--- B2. IVF endotoxin estimates (phenoloxidase) ---")
print(f"{'Batch':<20}{'Absorbance':>12}{'Estimated EU/mL':>18}")
for name, abs_val, eu in zip(po_ivf_names, po_ivf_abs, po_ivf_estimated_eu):
    print(f"{name:<20}{abs_val:>12.4f}{eu:>18.2f}")

print("\n  IMPORTANT: some phenoloxidase IVF readings (e.g. 'Dextrose 5% 98'")
print("  at 0.156) are noticeably higher than the protein coagulation")
print("  readings for the same batch. This is worth flagging to your")
print("  supervisor -- it may suggest the two assays disagree on some")
print("  samples, which is a real and useful validation observation.")

# =====================================================================
# PLOTS
# =====================================================================

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: protein coagulation calibration
axes[0].scatter(pc_eu, pc_abs, color="tab:blue", label="Raw data (Sheet5)")
fit_x = np.linspace(0, 10, 100)
axes[0].plot(fit_x, slope * fit_x + intercept, color="tab:red",
             label=f"Our fit (R²={r_value**2:.3f})")
axes[0].plot(fit_x, 0.0109 * fit_x + 0.0644, color="tab:green", linestyle="--",
             label="Paper's reported line")
axes[0].set_xlabel("Endotoxin (EU)")
axes[0].set_ylabel("Change in absorbance")
axes[0].set_title("Protein coagulation calibration")
axes[0].legend(fontsize=8)

# Right: phenoloxidase calibration
axes[1].scatter(po_eu, po_rate, color="tab:blue", label="Raw data (Sheet8)")
axes[1].plot(fit_x, slope_po * fit_x + intercept_po, color="tab:red",
             label=f"Our fit (R²={r_po**2:.3f})")
axes[1].set_xlabel("Endotoxin (EU)")
axes[1].set_ylabel("Absorbance/min")
axes[1].set_title("Phenoloxidase calibration (new)")
axes[1].legend(fontsize=8)

plt.tight_layout()
plt.savefig("/home/claude/real_data_validation_plot.png", dpi=150)
print("\nPlot saved.")
