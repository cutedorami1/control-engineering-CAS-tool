import control as ct
import matplotlib.pyplot as plt
import numpy as np

# 1. 전달함수(Transfer Function) 정의
# 예: G(s) = 10 / (s * (s + 2) * (s + 5))
s = ct.tf('s')
G = 1 / ((s + 3) * (s + 5) * (s + 10))

print("=== Open-Loop Transfer Function G(s) ===")
print(G)

# 2. 안정도 여유(Stability Margins) 계산
gm, pm, wcg, wcp = ct.margin(G)
gm_db = 20 * np.log10(gm) if gm > 0 else np.inf  # 이득 여유를 dB로 변환

print("\n=== Stability Analysis ===")
print(f"Gain Margin   : {gm:.2f} ({gm_db:.2f} dB) at {wcg:.2f} rad/s")
print(f"Phase Margin  : {pm:.2f} deg at {wcp:.2f} rad/s")

# 3. 그래프 그리기 설정 (근궤적 & 보드 선도)
fig = plt.figure(figsize=(14, 8))
fig.suptitle("Control System Analysis: Root Locus & Bode Plot", fontsize=14, fontweight='bold')

# [서브플롯 1] 근궤적 (Root Locus)
ax1 = plt.subplot(2, 2, (1, 3))  # 왼쪽 전체 영역 사용
ct.root_locus(G, ax=ax1, grid=True)
ax1.set_title("Root Locus")
ax1.set_xlabel("Real Axis (seconds^-1)")
ax1.set_ylabel("Imaginary Axis (seconds^-1)")

# [서브플롯 2 & 3] 보드 선도 (Bode Plot)
ax2_mag = plt.subplot(2, 2, 2)
ax2_phase = plt.subplot(2, 2, 4, sharex=ax2_mag)

# 주파수 범위 설정 (0.1 ~ 100 rad/s)
omega = np.logspace(-1, 2, 500)
mag, phase, omega = ct.frequency_response(G, omega)

# 크기 선도 (Magnitude in dB)
ax2_mag.semilogx(omega, 20 * np.log10(mag), color='b', linewidth=1.5)
ax2_mag.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax2_mag.set_title("Bode Plot")
ax2_mag.set_ylabel("Magnitude (dB)")
ax2_mag.grid(True, which="both", ls="-", alpha=0.5)

# 위상 선도 (Phase in degrees)
ax2_phase.semilogx(omega, np.degrees(phase), color='r', linewidth=1.5)
ax2_phase.axhline(-180, color='gray', linestyle='--', linewidth=0.8)
ax2_phase.set_xlabel("Frequency (rad/s)")
ax2_phase.set_ylabel("Phase (deg)")
ax2_phase.grid(True, which="both", ls="-", alpha=0.5)

plt.tight_layout()
plt.show()

# 4. 단위 피드백 폐루프 계단 응답 (Closed-Loop Step Response)
T = ct.feedback(G, 1)  # H(s) = 1 인 단위 피드백
t, y = ct.step_response(T)

plt.figure(figsize=(8, 4))
plt.plot(t, y, linewidth=2, color='g', label='Step Response')
plt.axhline(1, color='r', linestyle='--', label='Reference (1.0)')
plt.title("Closed-Loop Step Response")
plt.xlabel("Time (sec)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.show()
