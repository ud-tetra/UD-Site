# Gap 2 Final Status: What Is Resolved and What Remains

## Benjamin Mayes — Distinction Theory v2.1 | Working Document

---

## 1. What This Session Established

Three simulations were run: v0.7 (500 steps), v0.7b (5000 steps, extended), and v0.7c (5000 steps, direct P(k)). Together they established:

### Confirmed

1. **Theorem 1 is numerically confirmed.** The near-uniform state is unstable. Amplitudes grow exponentially with γ = 0.129 (R² = 0.995).

2. **Spatial structure emerges from near-uniformity.** Wave patterns → localised features → saturated clusters. This is the genesis process working as described.

3. **Ω evolves during genesis.** Over 57 genesis levels, Ω converges from ~0.63 toward ~0.99, then settles to a post-genesis equilibrium of ~0.81. The envelope convergence follows Ω(n) = Ω_∞ − ΔΩ₀·ρⁿ with ρ = 0.891, R² = 0.99.

4. **The Ω-convergence mechanism qualitatively produces a red tilt.** Earlier genesis levels have lower Ω, giving larger perturbation amplitudes at those scales → more power at large scales → n_s < 1.

5. **The spectral running dn_s/d ln k ≈ −0.008 to −0.010 is consistent with Planck** (−0.0045 ± 0.0067). This is a genuine prediction, independent of n_CMB.

### Falsified

6. **The original Gap 2 formula (inflationary analogy) is wrong.** Φ ~ 0.7, not 10⁻³. The slow-roll condition μ ≪ 1 is violated (μ ~ 8). The formula n_s = 1 − 4Φ_g/(3κ ln²(1/r)) is dead.

### Unresolved

7. **The direct P(k) measurement cannot resolve the primordial tilt.** The equilibrium power spectrum has slope ≈ −2.5 from nonlinear cluster dynamics. The primordial 3.5% tilt is buried under orders-of-magnitude nonlinear reshaping. This is analogous to why the primordial spectrum is invisible in the present-day galaxy distribution.

8. **n_CMB remains a free parameter.** The Ω-convergence formula n_s = 1 − A·ρ^{n_CMB} matches Planck at n_CMB ≈ 3–8 (depending on the fit method). This parameter plays the same role as N_* in inflation.

---

## 2. Honest Comparison with Inflation

The spectral index in DT has the same parameter structure as in single-field slow-roll inflation:

| | Inflation | DT (Ω-convergence) |
|---|---|---|
| Mechanism | Slow-roll of V(φ) | Ω convergence to attractor |
| Mathematical basis | Potential flatness | Banach fixed-point theorem |
| Formula | n_s = 1 − 6ε + 2η | n_s = 1 − A·ρ^{n_CMB} |
| Parameters from theory | ε, η (from V(φ)) | A, ρ (from simulation) |
| Free parameter | N_* (reheating history) | n_CMB (genesis-level of CMB mode) |
| Running | −2ε(2η − 4ε − 2ξ) | −(n_s − 1)·|ln ρ|/ln(1/r) |
| Tensor ratio | 16ε | ≈ 0 (from IFS contraction) |

**Both theories have exactly one free parameter for n_s.** This is the standard for this class of theory. The DT theory is at the same level of predictive power as the leading inflationary models.

---

## 3. What Would Eliminate the Free Parameter

### Path A: Larger simulation with linear-regime P(k)

A 400×400 or larger grid with the P(k) measured *during* the linear growth phase (before nonlinear saturation) would directly resolve the primordial tilt. The 80×80 grid has ≈1.5 decades of k-range; a 400×400 grid would have ≈2.5 decades, which should suffice for a 3.5% slope measurement.

The measurement must be done at a specific simulation time: after enough genesis levels for the Ω-evolution to imprint the tilt, but before nonlinear saturation erases it. This is the DT analog of the CMB — a snapshot of the perturbation field at the end of the linear regime.

### Path B: Theoretical determination of ΔN

In inflation, N_* ≈ 55 is determined by the reheating temperature. The analog in DT: ΔN (= N_gen − n_CMB) is determined by the ratio of the CMB pivot scale to the genesis-end scale. If the genesis-end scale can be computed from the DT parameters (it's related to the saturation amplitude and the lattice spacing), then n_CMB = N_gen − ΔN is determined.

### Path C: Derive ρ analytically

If ρ can be expressed in terms of r_tetra and the lattice geometry (e.g., ρ = r_tetra^{2/z} for coordination number z), and if A can be derived from the initial conditions, then the spectral index formula becomes:

$$
n_s = 1 - f(r_\text{tetra}, z) \cdot \rho^{g(N_\text{gen})}
$$

where f and g are computable functions. This would eliminate all free parameters.

---

## 4. What Goes in the Paper

### The strong claims (fully supported)

- Near-scale-invariance from IFS self-similarity (d_H = 3 → n_s ≈ 1). This is a structural prediction with no free parameters.
- The red tilt arises from Ω-convergence during genesis. This is confirmed by simulation.
- The spectral running is dn_s/d ln k ≈ −0.008, consistent with Planck. This is a parameter-free bonus prediction.
- The tensor-to-scalar ratio is r_T ≈ 0. Also parameter-free.

### The honest framing

"The spectral index n_s = 1 − A·ρ^{n_CMB} depends on one undetermined parameter n_CMB, the genesis level at which the CMB pivot mode's amplitude was set. This parameter plays the same role as N_* in inflationary cosmology and will be determined by larger simulations (in preparation) that resolve the primordial power spectrum directly."

### What NOT to claim

- Do not claim n_s = 0.965 as a parameter-free prediction. It isn't.
- Do not claim the simulation "confirms" n_s = 0.965. It doesn't — it confirms the mechanism and the running, not the specific value.
- Do not present the Ω-convergence formula as eliminating all free parameters. It trades Φ_g (which was wrong) for n_CMB (which is undetermined).

---

## 5. Revised Gap 7 (Falsifiability)

With Gap 2 in its honest final state, the falsifiable predictions are:

| Rank | Prediction | Parameters | Status |
|---|---|---|---|
| 1 | Near-scale-invariance (n_s ≈ 1) | 0 | Confirmed |
| 2 | Red tilt from Ω-convergence | 1 (n_CMB) | Mechanism confirmed |
| 3 | Running ≈ −0.008 | 0 | Consistent with Planck |
| 4 | r_T ≈ 0 | 0 | Consistent with BICEP/Keck |
| 5 | ω_BD,eff > 10^{80} | 0 | Consistent with Cassini |
| 6 | Regge linearity R² > 0.85 | 0 | Awaiting v0.3 data |
| 7 | d_H(3D) ≈ 3.0 | 0 | Awaiting v0.3 data |

The theory makes **four parameter-free predictions** (ranks 1, 3, 4, 5) that are all currently consistent with observation. The spectral index value has one parameter, same as inflation.

---

## 6. Updated Context Document Entries

### Spectral Index (Revised)

$$
n_s = 1 - \mathcal{A} \cdot \rho^{n_\text{CMB}}
\qquad \text{(A.6''')}
$$

Mechanism: Ω-convergence during genesis (Banach fixed-point theorem).
Simulation values: A = 0.051 (envelope), ρ = 0.891. R² = 0.99.
One undetermined parameter: n_CMB (analogous to N_* in inflation).
Planck match at n_CMB ≈ 3–8.

### Running (Prediction — zero free parameters)

$$
\frac{dn_s}{d\ln k} = -(n_s - 1) \cdot \frac{|\ln\rho|}{\ln(1/r)} \approx -0.008
\qquad \text{(A.19'')}
$$

Planck: −0.0045 ± 0.0067. Consistent within 1σ.

### Tensor-to-Scalar Ratio (Prediction — zero free parameters)

$$
r_T \approx 0
$$

---

*This document records an honest assessment after three simulation runs and multiple analytic attempts. The spectral index mechanism is identified and confirmed; the specific value has one free parameter. This is the same status as single-field inflation. The path to eliminating the parameter is clear (larger simulations) but not yet executed.*
