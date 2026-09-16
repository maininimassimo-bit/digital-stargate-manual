import crypto from "node:crypto";
import fs from "node:fs";
import https from "node:https";
import path from "node:path";
import process from "node:process";
import { Transform } from "node:stream";
import { pipeline } from "node:stream/promises";

const sourceUrl = new URL("https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de442s.bsp");
const expected = {
  sizeBytes: 32701440,
  sha256: "54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c",
  md5: "cc49327e06088124c0e39d8dde9f0b58",
  magic: "DAF/SPK",
};

const args = process.argv.slice(2);
const valueFor = (name) => {
  const index = args.indexOf(name);
  if (index < 0 || index + 1 >= args.length) throw new Error(`missing ${name}`);
  return args[index + 1];
};

const destination = path.resolve(valueFor("--destination"));
const evidencePath = path.resolve(valueFor("--evidence"));
const partial = `${destination}.part`;

for (const target of [destination, evidencePath, partial]) {
  if (fs.existsSync(target)) throw new Error(`refusing to overwrite existing path: ${target}`);
}
fs.mkdirSync(path.dirname(destination), { recursive: true });
fs.mkdirSync(path.dirname(evidencePath), { recursive: true });

const sha256 = crypto.createHash("sha256");
const md5 = crypto.createHash("md5");
let sizeBytes = 0;
let responseHeaders;
let tlsPeer;

try {
  await new Promise((resolve, reject) => {
    const request = https.request(
      sourceUrl,
      {
        method: "GET",
        headers: {
          Accept: "application/octet-stream",
          "Accept-Encoding": "identity",
          "User-Agent": "Digital-StarGate-BKL-031-F3-A3-Governed-Acquisition/1.0",
        },
      },
      async (response) => {
        try {
          if (response.statusCode !== 200) {
            response.resume();
            throw new Error(`official source returned HTTP ${response.statusCode}; redirects are not accepted`);
          }
          if (response.headers.location) throw new Error("official source unexpectedly returned a redirect location");
          if (response.headers["content-encoding"] && response.headers["content-encoding"] !== "identity") {
            throw new Error(`unexpected content encoding: ${response.headers["content-encoding"]}`);
          }
          const declaredLength = Number(response.headers["content-length"]);
          if (!Number.isSafeInteger(declaredLength) || declaredLength !== expected.sizeBytes) {
            throw new Error(`unexpected Content-Length: ${response.headers["content-length"]}`);
          }
          responseHeaders = {
            contentLength: response.headers["content-length"],
            contentType: response.headers["content-type"] ?? null,
            etag: response.headers.etag ?? null,
            lastModified: response.headers["last-modified"] ?? null,
          };
          const certificate = response.socket.getPeerCertificate();
          tlsPeer = {
            subjectCommonName: certificate.subject?.CN ?? null,
            issuerOrganization: certificate.issuer?.O ?? null,
            fingerprint256: certificate.fingerprint256 ?? null,
            validFrom: certificate.valid_from ?? null,
            validTo: certificate.valid_to ?? null,
          };
          const verifier = new Transform({
            transform(chunk, _encoding, callback) {
              sizeBytes += chunk.length;
              if (sizeBytes > expected.sizeBytes) {
                callback(new Error(`download exceeded expected size: ${sizeBytes}`));
                return;
              }
              sha256.update(chunk);
              md5.update(chunk);
              callback(null, chunk);
            },
          });
          await pipeline(response, verifier, fs.createWriteStream(partial, { flags: "wx", mode: 0o600 }));
          resolve();
        } catch (error) {
          reject(error);
        }
      },
    );
    request.setTimeout(120_000, () => request.destroy(new Error("official source request timed out")));
    request.on("error", reject);
    request.end();
  });

  const observedSha256 = sha256.digest("hex");
  const observedMd5 = md5.digest("hex");
  const magic = fs.readFileSync(partial).subarray(0, expected.magic.length).toString("ascii");
  if (sizeBytes !== expected.sizeBytes) throw new Error(`size mismatch: ${sizeBytes}`);
  if (observedSha256 !== expected.sha256) throw new Error(`SHA-256 mismatch: ${observedSha256}`);
  if (observedMd5 !== expected.md5) throw new Error(`MD5 mismatch: ${observedMd5}`);
  if (magic !== expected.magic) throw new Error(`SPICE header mismatch: ${JSON.stringify(magic)}`);
  fs.renameSync(partial, destination);

  const evidence = {
    evidenceId: "BKL-031-F3-A3-KERNEL-ACQUISITION-TRANSIENT-EVIDENCE",
    acquiredAtUtc: new Date().toISOString(),
    source: sourceUrl.href,
    redirectAccepted: false,
    requestCount: 1,
    sizeBytes,
    sha256: observedSha256,
    md5: observedMd5,
    spiceHeader: magic,
    responseHeaders,
    tlsPeer,
  };
  fs.writeFileSync(evidencePath, `${JSON.stringify(evidence, null, 2)}\n`, { encoding: "utf8", flag: "wx", mode: 0o600 });
  console.log(JSON.stringify(evidence, null, 2));
} catch (error) {
  fs.rmSync(partial, { force: true });
  fs.rmSync(destination, { force: true });
  throw error;
}
