import { cp, mkdir, rm } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const target = path.join(root, "dist", "runtime");
await rm(target, { recursive: true, force: true });
await mkdir(path.join(target, "src"), { recursive: true });
await cp(path.join(root, "package.json"), path.join(target, "package.json"));
for (const file of ["index.mjs", "voice.mjs", "forecast.mjs", "sources.mjs"]) {
  await cp(path.join(root, "src", file), path.join(target, "src", file));
}
console.log(`Runtime bundle rebuilt from allowlist at ${target}`);
