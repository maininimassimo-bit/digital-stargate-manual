// Arithmetic helper for passive, validated declarations. No scientific policy.
export function conditionalCovarianceSigma(variances, covariances, gradient, fail) {
  const n = variances.length, pairs = [];
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) pairs.push([i, j]);
  for (let k = 0; k < pairs.length; k++) {
    const [i, j] = pairs[k], c = covariances[k];
    if (c === null) continue;
    if ((variances[i] === 0 || variances[j] === 0) && c !== 0) fail();
    if (variances[i] !== null && variances[j] !== null
        && Math.abs(c) > Math.sqrt(variances[i]) * Math.sqrt(variances[j])) fail();
  }
  if (variances.includes(null) || covariances.includes(null)) return null;
  const tolerance = 64 * Number.EPSILON;
  const std = variances.map(Math.sqrt);
  const corr = variances.map((v, i) => Array.from({length: n}, (_, j) => i === j && v > 0 ? 1 : 0));
  for (let k = 0; k < pairs.length; k++) {
    const [i, j] = pairs[k];
    corr[i][j] = corr[j][i] = std[i] === 0 || std[j] === 0 ? 0 : covariances[k] / (std[i] * std[j]);
  }
  const lower = Array.from({length: n}, () => Array(n).fill(0));
  for (let i = 0; i < n; i++) for (let j = 0; j <= i; j++) {
    let residual = corr[i][j];
    for (let k = 0; k < j; k++) residual -= lower[i][k] * lower[j][k];
    if (i === j) {
      if (residual < -tolerance) fail();
      lower[i][j] = Math.sqrt(Math.max(0, residual));
    } else if (lower[j][j] === 0) {
      if (Math.abs(residual) > tolerance) fail();
    } else lower[i][j] = residual / lower[j][j];
  }
  const weights = gradient.map((g, i) => g * std[i]);
  if (!weights.every(Number.isFinite)) fail();
  const transformed = Array.from({length: n}, (_, j) => weights.reduce((sum, w, i) => sum + w * lower[i][j], 0));
  const sigma = Math.hypot(...transformed);
  if (!Number.isFinite(sigma)) fail();
  return sigma;
}
