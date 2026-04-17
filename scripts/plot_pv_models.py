"""p(V) 모델 후보 비교 차트 생성.

출력: docs/design/assets/pv-model-comparison.png
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["figure.dpi"] = 150

V = np.linspace(0, 60, 300)
baseline = 0.5
lam = 0.06

# --- 후보 모델들 ---

# 1. Exponential saturation (현재 채택)
p_exp = baseline + (1 - baseline) * (1 - np.exp(-lam * V))

# 2. Logistic sigmoid (V0=15, k=0.15 로 비슷한 스케일)
V0, k = 15, 0.15
p_logistic = baseline + (1 - baseline) * (1 / (1 + np.exp(-k * (V - V0))))

# 3. Power law (gamma=0.5, V_max=60)
gamma, V_max = 0.5, 60
p_power = baseline + (1 - baseline) * np.clip(V / V_max, 0, 1) ** gamma

# 4. Linear clamp (slope=0.015)
slope = 0.015
p_linear = np.clip(baseline + slope * V, baseline, 1.0)

# --- 플롯 ---

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(V, p_exp, linewidth=2.5, label="Exponential saturation (adopted)", color="#2563eb")
ax.plot(V, p_logistic, linewidth=1.8, linestyle="--", label=f"Logistic sigmoid (V₀={V0}, k={k})", color="#dc2626")
ax.plot(V, p_power, linewidth=1.8, linestyle="-.", label=f"Power law (γ={gamma}, V_max={V_max})", color="#16a34a")
ax.plot(V, p_linear, linewidth=1.8, linestyle=":", label=f"Linear clamp (slope={slope})", color="#9333ea")

ax.axhline(y=baseline, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
ax.text(58, baseline - 0.03, "baseline (0.5)", ha="right", fontsize=8, color="gray")

ax.axhline(y=1.0, color="gray", linewidth=0.8, linestyle="--", alpha=0.3)

ax.set_xlabel("V (pp) — volatility", fontsize=11)
ax.set_ylabel("p(V) — estimated correct rate", fontsize=11)
ax.set_title("p(V) model candidates comparison  (λ = 0.06)", fontsize=13, fontweight="bold")
ax.set_xlim(0, 60)
ax.set_ylim(0.4, 1.05)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("docs/design/assets/pv-model-comparison.png")
print("saved → docs/design/assets/pv-model-comparison.png")
