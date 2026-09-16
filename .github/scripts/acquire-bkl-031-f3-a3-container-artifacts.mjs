import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const containerDir = path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "container");
const manifestPath = path.join(containerDir, "BKL-031-F3-A3-CONTAINER-MANIFEST-002.json");
const allowedDestination = path.join(containerDir, ".build", "wheels");
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) args.set(process.argv[index], process.argv[index + 1]);
const destination = path.resolve(args.get("--destination") || "");
const evidencePath = path.resolve(args.get("--evidence") || "");

const fail = (message) => { throw new Error(message); };
if (destination !== allowedDestination) fail(`destination must be ${allowedDestination}`);
if (evidencePath !== path.join(containerDir, ".build", "acquisition-evidence.json")) {
  fail("evidence path must remain inside the ignored container .build directory");
}
if (fs.existsSync(destination) && fs.readdirSync(destination).length) fail("destination must be empty");
fs.mkdirSync(destination, { recursive: true });

const rawManifest = fs.readFileSync(manifestPath);
const manifest = JSON.parse(rawManifest.toString("utf8"));
const sha256 = (value) => crypto.createHash("sha256").update(value).digest("hex");
const records = [];

for (const artifact of manifest.packages) {
  const source = new URL(artifact.source);
  if (source.protocol !== "https:" || source.hostname !== "files.pythonhosted.org") {
    fail(`${artifact.name} source is outside official PyPI file hosting`);
  }
  if (path.basename(source.pathname) !== artifact.artifact || path.basename(artifact.artifact) !== artifact.artifact) {
    fail(`${artifact.name} artifact name does not match its source URL`);
  }

  const response = await fetch(source, { redirect: "follow" });
  if (!response.ok || response.url !== artifact.source) fail(`${artifact.name} acquisition failed or redirected`);
  const bytes = Buffer.from(await response.arrayBuffer());
  const digest = sha256(bytes);
  if (digest !== artifact.sha256) fail(`${artifact.name} SHA-256 mismatch`);
  if (artifact.name === "astropy-iers-data" && bytes.length !== manifest.iersSnapshot.sizeBytes) {
    fail("IERS artifact size mismatch");
  }
  fs.writeFileSync(path.join(destination, artifact.artifact), bytes, { flag: "wx" });
  records.push({
    name: artifact.name,
    version: artifact.version,
    artifact: artifact.artifact,
    sizeBytes: bytes.length,
    sha256: digest,
    source: artifact.source,
  });
}

const evidence = {
  schemaVersion: "1.0",
  evidenceId: "BKL-031-F3-A3-ACQUISITION-EVIDENCE-001",
  status: "ACQUIRED_AND_HASH_VERIFIED_EPHEMERAL_NOT_UPLOADED",
  sourceManifestId: manifest.manifestId,
  sourceManifestSha256: sha256(rawManifest),
  acquiredAtUtc: new Date().toISOString(),
  sourceCommit: process.env.GITHUB_SHA || "LOCAL_UNCOMMITTED_OR_COMMITTED_CHECKOUT",
  destinationPolicy: "EPHEMERAL_IGNORED_BUILD_INPUT",
  artifactUpload: "NOT_EXECUTED",
  records,
};
fs.mkdirSync(path.dirname(evidencePath), { recursive: true });
fs.writeFileSync(evidencePath, `${JSON.stringify(evidence, null, 2)}\n`, { flag: "wx" });
console.log(JSON.stringify(evidence, null, 2));
