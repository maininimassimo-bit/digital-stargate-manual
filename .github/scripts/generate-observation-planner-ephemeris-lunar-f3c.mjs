import fs from 'node:fs';
import { canonicalJson } from './observation-planner-ephemeris-lunar-f3b-contract.mjs';
import { buildF3CProjection } from './observation-planner-ephemeris-lunar-f3c-adapter.mjs';

const sourcePath = 'docs/data/observation-planner-ephemeris-lunar-f3b-fixture.json';
const outputPath = 'docs/data/observation-planner-ephemeris-lunar-f3c-projection.json';
const fixture = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
const expected = `${JSON.stringify(buildF3CProjection(fixture), null, 2)}\n`;

if (process.argv.includes('--write')) {
  fs.writeFileSync(outputPath, expected);
  console.log(`Generated ${outputPath} from accepted F3-B synthetic evidence.`);
} else if (process.argv.includes('--check')) {
  const actual = fs.readFileSync(outputPath, 'utf8');
  if (canonicalJson(JSON.parse(actual)) !== canonicalJson(JSON.parse(expected))) throw new Error(`${outputPath} is not aligned with the deterministic F3-C adapter.`);
  console.log(`F3-C projection aligned: ${buildF3CProjection(fixture).projectionDigest}`);
} else {
  process.stdout.write(expected);
}
