import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const infra = path.join(root, "infrastructure", "bkl-031-f3-a3-gcp");
const bootstrap = fs.readFileSync(path.join(infra, "bootstrap", "main.tf"), "utf8");
const bootstrapVariables = fs.readFileSync(path.join(infra, "bootstrap", "variables.tf"), "utf8");
const platform = fs.readFileSync(path.join(infra, "platform", "main.tf"), "utf8");
const variables = fs.readFileSync(path.join(infra, "platform", "variables.tf"), "utf8");
const workflow = fs.readFileSync(path.join(root, ".github", "workflows", "bkl-031-f3-a3-gcp-iac.yml"), "utf8");

const failures = [];
const requireText = (name, text, fragment) => {
  if (!text.includes(fragment)) failures.push(name + " missing: " + fragment);
};
const forbid = (name, text, regex, reason) => {
  if (regex.test(text)) failures.push(name + " forbidden: " + reason);
};

requireText("bootstrap", bootstrap, "assertion.repository == '%s' && assertion.ref == 'refs/heads/main'");
requireText("bootstrap variables", bootstrapVariables, "maininimassimo-bit/digital-stargate-manual");
requireText("bootstrap", bootstrap, "roles/iam.workloadIdentityUser");
requireText("bootstrap", bootstrap, 'public_access_prevention    = "enforced"');
requireText("platform", platform, 'location            = var.region');
requireText("platform", platform, 'deletion_protection = true');
requireText("platform", platform, 'task_count  = 1');
requireText("platform", platform, 'parallelism = 1');
requireText("platform", platform, 'timeout         = "120s"');
requireText("platform", platform, 'max_retries     = 0');
requireText("platform", platform, 'cpu    = "2"');
requireText("platform", platform, 'memory = "2Gi"');
requireText("platform", platform, 'egress = "ALL_TRAFFIC"');
requireText("platform", platform, 'DSG_SITE_PROFILE');
requireText("platform", platform, 'SYNTHETIC_ONLY');
requireText("platform", platform, 'DSG_EXTERNAL_PROVIDER_POLICY');
requireText("platform", platform, 'DENY');
requireText("variables", variables, 'default = "europe-west8"');
requireText("variables", variables, "@sha256:[0-9a-f]{64}$");
requireText("workflow", workflow, "terraform validate -no-color");
requireText("workflow", workflow, "terraform init -backend=false -input=false");

forbid("bootstrap", bootstrap, /allUsers|allAuthenticatedUsers/, "public IAM principal");
forbid("platform", platform, /allUsers|allAuthenticatedUsers/, "public IAM principal");
forbid("bootstrap", bootstrap, /private_key|credentials\s*=/i, "static credential");
forbid("platform", platform, /google_compute_router_nat/, "Cloud NAT/public egress");
forbid("workflow", workflow, /terraform\s+apply/, "cloud mutation in validation workflow");

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log("BKL-031 F3-A3 Google Cloud policy checks passed.");
