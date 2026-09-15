import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { extname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const METHOD = "DSG-F3A2-CANONICAL-JSON-SHA256-1";
export const PUBLIC_ALLOWLIST = Object.freeze(["publicSetupRef","publicEvidenceDigest","availabilityState","publicReasonCode","asOfUtc","provenance"]);
const DIGEST_RE = /^sha256:[a-f0-9]{64}$/;
const PUBLIC_REASON_CODES = new Set(["AVAILABLE","UNAVAILABLE","CONFLICTED","INVALID"]);
const UTC_RE = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/;
const SENTINELS = new Set(["9999-12-31T23:59:59Z","9999-12-31T23:59:59.999Z"]);
const ROOT_KEYS=["schemaVersion","recordType","lifecycle","assignmentPayload","payloadDigest","validationEvidence"];
const LIFE_KEYS=["state","eligibleForResolution","approvalEvidenceRef","approvedAtUtc","retiredAtUtc","retirementEvidenceRef","decisionEvidenceRef","statement"];
const PAYLOAD_KEYS=["assignmentId","revision","observatoryId","siteAuthorityReference","setupBaselineReference","authority","validity","scope","classification","retention","publicationPolicy","intendedUse","prohibitedUses","rollback"];
const SITE_REF_KEYS=["recordPath","siteRecordId","revision","observatoryId","payloadDigest","lifecycleState","approvalEvidenceRef"];
const BASE_REF_KEYS=["recordPath","baselineId","baselineVersion","configurationId","payloadDigest","lifecycleState","approvalEvidenceRef"];
const AUTH_KEYS=["authoritySystem","repository","registryRoot","authorityScope","authorityRole","assignmentOwnerRef","assignmentCustodianRef","assignmentApprovalAuthorityRef","custodianMayApprove","separationPolicy","sourceLocator"];
const VALIDITY_KEYS=["validFromUtc","validityEndMode","validToUtc","intervalSemantics"];
const PUBLICATION_KEYS=["publicProjection","internalIdentifiers","protectedDigests","authorityLocators","exactSiteFacts"];
const ROLLBACK_KEYS=["draft","futureApproval","retirement"];
const DIGEST_KEYS=["method","canonicalization","algorithm","value"];
const EVIDENCE_KEYS=["jsonParse","schemaValidatorParity","decisionEvidenceBinding","sourceAuthorityBinding","payloadDigestRecomputation","lifecycleIneligibility","executableContractCases","protectedValueLeakScan","runtimeOat"];
const DECISION_ROOT_KEYS=["schemaVersion","recordType","decisionId","decision","decisionRecordedAtUtc","decidingAuthority","futureCandidateRef","decisions","sourceAuthorization","scopeBoundaries","lifecycleBoundary"];
const DECISION_KEYS=["authoritySystem","authorityRoot","publicationRootExcluded","assignmentOwnerRef","assignmentCustodianRef","assignmentApprovalAuthorityRef","custodianMayApprove","separationPolicy","siteAuthorityReference","setupBaselineReference","validity","retention","publicProjection"];
const DECISION_SITE_KEYS=["recordPath","siteRecordId","revision","observatoryId","payloadDigest","lifecycleState"];
const DECISION_BASE_KEYS=["recordPath","baselineId","baselineVersion","configurationId","payloadDigest","lifecycleState"];
const DECISION_VALIDITY_KEYS=["validFromPolicy","validFromUtc","validityEndMode","validToUtc","intervalSemantics"];
const SOURCE_AUTH_KEYS=["sourceChannel","ownerSelections","exactReferencesStoredOnlyInProtectedEvidence"];
const REQUIRED_PROHIBITIONS=["CURRENT_SETUP_RESOLUTION_BEFORE_APPROVAL","DEVICE_COMMAND","SAFETY_AUTHORITY","READINESS_OR_GO_NO_GO","PUBLIC_PROTECTED_ASSIGNMENT_PROJECTION","EAGLE_WORKLOAD","LATEST_WINS_FALLBACK","HOST_OR_SESSION_STATE_AS_AUTHORITY"];

function obj(v){return v!==null&&typeof v==="object"&&!Array.isArray(v);}
function exact(v,keys){return obj(v)&&Object.keys(v).sort().join("|")===[...keys].sort().join("|");}
function add(errors,condition,code){if(!condition)errors.push(code);}
function unique(errors){return [...new Set(errors)];}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function utc(v){return typeof v==="string"&&UTC_RE.test(v)&&Number.isFinite(Date.parse(v));}
function resolvable(v){return typeof v==="string"&&v.length>0;}
export function canonicalize(v){if(Array.isArray(v))return "["+v.map(canonicalize).join(",")+"]";if(obj(v))return "{"+Object.keys(v).sort().map(k=>JSON.stringify(k)+":"+canonicalize(v[k])).join(",")+"}";return JSON.stringify(v);}
export function digestPayload(v){return "sha256:"+createHash("sha256").update(canonicalize(v),"utf8").digest("hex");}
function validInterval(v,errors){
 add(errors,exact(v,VALIDITY_KEYS),"INVALID_SCHEMA_SHAPE");
 if(!obj(v))return errors.push("INVALID_VALIDITY_INTERVAL");
 add(errors,utc(v.validFromUtc)&&v.intervalSemantics==="HALF_OPEN","INVALID_VALIDITY_INTERVAL");
 if(v.validityEndMode==="EXCLUSIVE")add(errors,utc(v.validToUtc)&&!SENTINELS.has(v.validToUtc)&&Date.parse(v.validToUtc)>Date.parse(v.validFromUtc),"INVALID_VALIDITY_INTERVAL");
 else if(v.validityEndMode==="UNBOUNDED")add(errors,v.validToUtc===null,"INVALID_VALIDITY_INTERVAL");
 else errors.push("INVALID_VALIDITY_INTERVAL");
}
export function intervalContains(v,t){if(!obj(v)||!utc(t)||!utc(v.validFromUtc)||Date.parse(t)<Date.parse(v.validFromUtc))return false;return v.validityEndMode==="UNBOUNDED"||utc(v.validToUtc)&&Date.parse(t)<Date.parse(v.validToUtc);}
export function intervalsOverlap(a,b){const ae=a.validityEndMode==="UNBOUNDED"?Infinity:Date.parse(a.validToUtc),be=b.validityEndMode==="UNBOUNDED"?Infinity:Date.parse(b.validToUtc);return Date.parse(a.validFromUtc)<be&&Date.parse(b.validFromUtc)<ae;}
function lifecycleErrors(l,errors){
 add(errors,exact(l,LIFE_KEYS),"INVALID_SCHEMA_SHAPE");
 if(!obj(l))return;
 if(l.state==="DRAFT")add(errors,l.eligibleForResolution===false&&l.approvalEvidenceRef===null&&l.approvedAtUtc===null&&l.retiredAtUtc===null&&l.retirementEvidenceRef===null,"INVALID_LIFECYCLE");
 else if(l.state==="APPROVED")add(errors,l.eligibleForResolution===true&&resolvable(l.approvalEvidenceRef)&&utc(l.approvedAtUtc)&&l.retiredAtUtc===null&&l.retirementEvidenceRef===null,"INVALID_APPROVAL_EVIDENCE");
 else if(l.state==="RETIRED")add(errors,l.eligibleForResolution===false&&utc(l.retiredAtUtc)&&resolvable(l.retirementEvidenceRef),"INVALID_RETIREMENT_EVIDENCE");
 else errors.push("INVALID_LIFECYCLE");
}
export function validateAssignment(r){
 const errors=[];add(errors,exact(r,ROOT_KEYS),"INVALID_SCHEMA_SHAPE");if(!obj(r))return{valid:false,errors};
 add(errors,r.schemaVersion==="1.0.0-draft"&&r.recordType==="DSG_CURRENT_SETUP_ASSIGNMENT","INVALID_RECORD_TYPE");
 lifecycleErrors(r.lifecycle,errors);
 const p=r.assignmentPayload;add(errors,exact(p,PAYLOAD_KEYS),"INVALID_SCHEMA_SHAPE");if(!obj(p))return{valid:false,errors:unique(errors)};
 add(errors,resolvable(p.assignmentId)&&Number.isInteger(p.revision)&&p.revision>0&&resolvable(p.observatoryId),"INVALID_IDENTITY");
 const sr=p.siteAuthorityReference,br=p.setupBaselineReference,a=p.authority;
 add(errors,exact(sr,SITE_REF_KEYS),"INVALID_SCHEMA_SHAPE");add(errors,obj(sr)&&Number.isInteger(sr.revision)&&sr.revision>0&&DIGEST_RE.test(sr.payloadDigest||"")&&sr.lifecycleState==="APPROVED","INVALID_SITE_REFERENCE");
 add(errors,exact(br,BASE_REF_KEYS),"INVALID_SCHEMA_SHAPE");add(errors,obj(br)&&resolvable(br.baselineVersion)&&DIGEST_RE.test(br.payloadDigest||"")&&br.lifecycleState==="APPROVED","INVALID_BASELINE_REFERENCE");
 add(errors,obj(sr)&&sr.observatoryId===p.observatoryId,"SITE_ASSIGNMENT_MISMATCH");
 add(errors,exact(a,AUTH_KEYS),"INVALID_SCHEMA_SHAPE");
 add(errors,obj(a)&&a.authoritySystem==="GITHUB_PROTECTED_REGISTRY"&&a.repository==="maininimassimo-bit/digital-stargate-manual"&&a.registryRoot==="governance/setup-authority/"&&a.authorityScope==="SINGLE_OBSERVATORY_CURRENT_SETUP"&&a.authorityRole==="SETUP_ASSIGNMENT_AUTHORITY"&&a.assignmentOwnerRef==="github:user:maininimassimo-bit"&&a.assignmentCustodianRef==="role:digital-stargate-architecture-office"&&a.assignmentApprovalAuthorityRef==="github:user:maininimassimo-bit"&&a.custodianMayApprove===false&&a.separationPolicy==="OWNER_MAY_APPROVE_CUSTODIAN_MUST_NOT_APPROVE"&&resolvable(a.sourceLocator),"ASSIGNMENT_AUTHORITY_INCOMPLETE");
 validInterval(p.validity,errors);
 add(errors,p.scope==="OBSERVATION_PLANNER_READ_ONLY_SETUP_AUTHORITY"&&p.classification==="PROTECTED_SETUP_ASSIGNMENT"&&p.retention==="APPEND_ONLY_GIT_HISTORY"&&p.intendedUse==="CURRENT_SETUP_RESOLUTION_AFTER_SEPARATE_EXACT_DIGEST_APPROVAL","INVALID_ASSIGNMENT_SEMANTICS");
 add(errors,exact(p.publicationPolicy,PUBLICATION_KEYS)&&Object.values(p.publicationPolicy||{}).every(v=>v==="DENY_BY_DEFAULT"||v==="PROHIBITED"),"PUBLIC_PROJECTION_POLICY");
 add(errors,exact(p.rollback,ROLLBACK_KEYS)&&Object.values(p.rollback||{}).every(resolvable),"INVALID_ROLLBACK");
 add(errors,Array.isArray(p.prohibitedUses)&&REQUIRED_PROHIBITIONS.every(x=>p.prohibitedUses.includes(x)),"SAFETY_OR_SCOPE_BOUNDARY");
 add(errors,exact(r.payloadDigest,DIGEST_KEYS)&&r.payloadDigest.method===METHOD&&r.payloadDigest.algorithm==="SHA-256"&&r.payloadDigest.canonicalization==="recursive object-key sort; array order preserved; compact JSON; UTF-8","INVALID_DIGEST_PROFILE");
 if(obj(p)&&obj(r.payloadDigest))add(errors,DIGEST_RE.test(r.payloadDigest.value||"")&&digestPayload(p)===r.payloadDigest.value,"ASSIGNMENT_INTEGRITY_FAILURE");
 add(errors,exact(r.validationEvidence,EVIDENCE_KEYS),"INVALID_SCHEMA_SHAPE");
 return{valid:errors.length===0,errors:unique(errors)};
}
export function validateDecisionEvidence(d){
 const errors=[];add(errors,exact(d,DECISION_ROOT_KEYS),"DECISION_SCHEMA_INVALID");if(!obj(d))return{valid:false,errors};
 add(errors,d.schemaVersion==="1.0.0-draft"&&d.recordType==="DSG_CURRENT_SETUP_ASSIGNMENT_OWNER_DECISION"&&d.decision==="OWNER_DECISIONS_COMPLETE"&&utc(d.decisionRecordedAtUtc)&&d.decidingAuthority==="github:user:maininimassimo-bit"&&d.futureCandidateRef==="governance/setup-authority/setup-assignments/DSG-CURRENT-SETUP-ASSIGNMENT-001.draft.json"&&d.lifecycleBoundary==="OWNER_DECISIONS_COMPLETE_NOT_ASSIGNMENT_APPROVAL","DECISION_SEMANTICS_INVALID");
 const x=d.decisions;add(errors,exact(x,DECISION_KEYS),"DECISION_SCHEMA_INVALID");
 add(errors,obj(x)&&x.authoritySystem==="GITHUB_PROTECTED_REGISTRY"&&x.authorityRoot==="governance/setup-authority/"&&x.publicationRootExcluded==="docs/"&&x.assignmentOwnerRef==="github:user:maininimassimo-bit"&&x.assignmentCustodianRef==="role:digital-stargate-architecture-office"&&x.assignmentApprovalAuthorityRef==="github:user:maininimassimo-bit"&&x.custodianMayApprove===false&&x.separationPolicy==="OWNER_MAY_APPROVE_CUSTODIAN_MUST_NOT_APPROVE"&&x.retention==="APPEND_ONLY_GIT_HISTORY","DECISION_AUTHORITY_INVALID");
 add(errors,obj(x)&&exact(x.siteAuthorityReference,DECISION_SITE_KEYS)&&exact(x.setupBaselineReference,DECISION_BASE_KEYS)&&exact(x.validity,DECISION_VALIDITY_KEYS),"DECISION_SCHEMA_INVALID");
 add(errors,obj(x)&&x.validity.validFromPolicy==="APPROVED_SETUP_BASELINE_EFFECTIVE_START"&&utc(x.validity.validFromUtc)&&x.validity.validityEndMode==="UNBOUNDED"&&x.validity.validToUtc===null&&x.validity.intervalSemantics==="HALF_OPEN","DECISION_VALIDITY_INVALID");
 add(errors,exact(d.sourceAuthorization,SOURCE_AUTH_KEYS)&&d.sourceAuthorization.sourceChannel==="OWNER_CONTROLLED_INTERACTION_CHANNEL"&&Array.isArray(d.sourceAuthorization.ownerSelections)&&d.sourceAuthorization.ownerSelections.length===3&&d.sourceAuthorization.exactReferencesStoredOnlyInProtectedEvidence===true,"DECISION_SOURCE_INVALID");
 const scopes=d.scopeBoundaries||[];for(const k of ["NO_ASSIGNMENT_DIGEST_APPROVAL","NO_ASSIGNMENT_LIFECYCLE_PROMOTION","NO_RUNTIME_OR_EAGLE_OPERATION","NO_PUBLIC_PROTECTED_REFERENCES","NO_READINESS_OR_GO_NO_GO_AUTHORITY","NO_SAFETY_AUTHORITY_CHANGE"])add(errors,scopes.includes(k),"DECISION_BOUNDARY_INVALID");
 return{valid:errors.length===0,errors:unique(errors)};
}
function schemaNode(node,required){return obj(node)&&node.additionalProperties===false&&same([...(node.required||[])].sort(),[...required].sort())&&same(Object.keys(node.properties||{}).sort(),[...required].sort());}
export function assertSchemaValidatorParity(as,ds){
 const checks=[
  schemaNode(as,ROOT_KEYS),schemaNode(as.properties.lifecycle,LIFE_KEYS),schemaNode(as.$defs.assignmentPayload,PAYLOAD_KEYS),schemaNode(as.$defs.siteAuthorityReference,SITE_REF_KEYS),schemaNode(as.$defs.setupBaselineReference,BASE_REF_KEYS),schemaNode(as.$defs.authority,AUTH_KEYS),schemaNode(as.$defs.validity,VALIDITY_KEYS),schemaNode(as.$defs.publicationPolicy,PUBLICATION_KEYS),schemaNode(as.$defs.rollback,ROLLBACK_KEYS),schemaNode(as.$defs.payloadDigest,DIGEST_KEYS),schemaNode(as.properties.validationEvidence,EVIDENCE_KEYS),
  schemaNode(ds,DECISION_ROOT_KEYS),schemaNode(ds.$defs.decisions,DECISION_KEYS),schemaNode(ds.$defs.siteAuthorityReference,DECISION_SITE_KEYS),schemaNode(ds.$defs.setupBaselineReference,DECISION_BASE_KEYS),schemaNode(ds.$defs.validity,DECISION_VALIDITY_KEYS),schemaNode(ds.$defs.sourceAuthorization,SOURCE_AUTH_KEYS)
 ];
 if(checks.some(x=>!x))throw new Error("SETUP_ASSIGNMENT_SCHEMA_VALIDATOR_PARITY_FAILED");
 return{valid:true};
}
function sourceDigestValid(envelope,payloadKey){return obj(envelope)&&obj(envelope[payloadKey])&&obj(envelope.payloadDigest)&&digestPayload(envelope[payloadKey])===envelope.payloadDigest.value;}
export function validateBinding(r,d,site,baseline){
 const errors=[...validateAssignment(r).errors,...validateDecisionEvidence(d).errors];const p=r.assignmentPayload,x=d.decisions;
 if(!obj(p)||!obj(x))return{valid:false,errors:unique(errors)};
 add(errors,r.lifecycle.decisionEvidenceRef===p.authority.sourceLocator&&d.futureCandidateRef.endsWith(".draft.json"),"DECISION_BINDING_FAILED");
 const ds=x.siteAuthorityReference,db=x.setupBaselineReference;
 add(errors,same(Object.fromEntries(DECISION_SITE_KEYS.map(k=>[k,p.siteAuthorityReference?.[k]])),ds),"DECISION_SITE_BINDING_FAILED");
 add(errors,same(Object.fromEntries(DECISION_BASE_KEYS.map(k=>[k,p.setupBaselineReference?.[k]])),db),"DECISION_BASELINE_BINDING_FAILED");
 add(errors,p.authority.assignmentOwnerRef===x.assignmentOwnerRef&&p.authority.assignmentCustodianRef===x.assignmentCustodianRef&&p.authority.assignmentApprovalAuthorityRef===x.assignmentApprovalAuthorityRef&&p.authority.custodianMayApprove===x.custodianMayApprove&&p.authority.separationPolicy===x.separationPolicy,"DECISION_AUTHORITY_BINDING_FAILED");
 add(errors,same(p.validity,{validFromUtc:x.validity.validFromUtc,validityEndMode:x.validity.validityEndMode,validToUtc:x.validity.validToUtc,intervalSemantics:x.validity.intervalSemantics}),"DECISION_VALIDITY_BINDING_FAILED");
 add(errors,obj(site)&&site.lifecycle?.state==="APPROVED"&&site.lifecycle?.eligibleForResolution===true&&sourceDigestValid(site,"sitePayload"),"SITE_AUTHORITY_NOT_APPROVED_OR_INTEGRAL");
 add(errors,obj(baseline)&&baseline.lifecycle?.state==="APPROVED"&&baseline.lifecycle?.eligibleForResolution===true&&sourceDigestValid(baseline,"baselinePayload"),"BASELINE_NOT_APPROVED_OR_INTEGRAL");
 if(obj(site)){const s=site.sitePayload,ref=p.siteAuthorityReference;add(errors,s?.siteRecordId===ref.siteRecordId&&s?.revision===ref.revision&&s?.observatoryId===ref.observatoryId&&site.payloadDigest?.value===ref.payloadDigest&&site.lifecycle?.approvalEvidenceRef===ref.approvalEvidenceRef,"SITE_ASSIGNMENT_MISMATCH");}
 if(obj(baseline)){const b=baseline.baselinePayload,ref=p.setupBaselineReference;add(errors,b?.baselineId===ref.baselineId&&b?.baselineVersion===ref.baselineVersion&&b?.configurationId===ref.configurationId&&baseline.payloadDigest?.value===ref.payloadDigest&&baseline.lifecycle?.approvalEvidenceRef===ref.approvalEvidenceRef,"BASELINE_INTEGRITY_FAILURE");add(errors,p.validity.validFromUtc===b?.validity?.validFromUtc,"BASELINE_VALIDITY_BINDING_FAILED");}
 return{valid:errors.length===0,errors:unique(errors)};
}
function fail(state,reasonCode){return{state,reasonCode};}
export function resolveCurrentSetup(records,{observatoryId,asOfUtc,authorized=true,sources={}}){
 if(!authorized)return{state:"UNAVAILABLE_CURRENT",reasonCode:"ACCESS_DENIED",audit:true};
 if(!utc(asOfUtc))return fail("INVALID","INVALID_VALIDITY_INTERVAL");
 const sameObs=(records||[]).filter(r=>r.assignmentPayload?.observatoryId===observatoryId);
 const approved=sameObs.filter(r=>r.lifecycle?.state==="APPROVED");
 const invalidInterval=approved.find(r=>{const e=[];validInterval(r.assignmentPayload?.validity,e);return e.length;});
 if(invalidInterval)return fail("INVALID","INVALID_VALIDITY_INTERVAL");
 const current=approved.filter(r=>intervalContains(r.assignmentPayload.validity,asOfUtc));
 if(current.length===0)return fail("UNAVAILABLE_CURRENT",approved.length?"VALIDITY_GAP":"NO_APPROVED_ASSIGNMENT");
 if(current.length>1)return fail("CONFLICTED","OVERLAPPING_APPROVED_ASSIGNMENTS");
 const r=current[0],v=validateAssignment(r);if(!v.valid){
  if(v.errors.includes("INVALID_APPROVAL_EVIDENCE"))return fail("INVALID","ASSIGNMENT_APPROVAL_EVIDENCE_MISSING");
  if(v.errors.includes("ASSIGNMENT_AUTHORITY_INCOMPLETE"))return fail("INVALID","ASSIGNMENT_AUTHORITY_INCOMPLETE");
  if(v.errors.includes("SITE_ASSIGNMENT_MISMATCH"))return fail("INVALID","SITE_ASSIGNMENT_MISMATCH");
  if(v.errors.includes("INVALID_BASELINE_REFERENCE"))return fail("UNAVAILABLE_CURRENT","BASELINE_REFERENCE_MISSING");
  return fail("INVALID","ASSIGNMENT_INTEGRITY_FAILURE");
 }
 if(sources.error)return fail("UNAVAILABLE_CURRENT","AUTHORITY_ADAPTER_FAILURE");
 const ref=r.assignmentPayload.siteAuthorityReference,sites=sources.siteRecords||[];
 if(sites.length===0)return fail("UNAVAILABLE_CURRENT","SITE_AUTHORITY_UNAVAILABLE");
 const site=sites.find(s=>s.sitePayload?.siteRecordId===ref.siteRecordId&&s.sitePayload?.revision===ref.revision);
 if(!site||site.sitePayload?.observatoryId!==ref.observatoryId||site.payloadDigest?.value!==ref.payloadDigest)return fail("INVALID","SITE_ASSIGNMENT_MISMATCH");
 const br=r.assignmentPayload.setupBaselineReference,bases=sources.baselines||[];
 if(bases.length===0)return fail("UNAVAILABLE_CURRENT","BASELINE_NOT_RESOLVABLE");
 const idMatches=bases.filter(b=>b.baselinePayload?.baselineId===br.baselineId&&b.baselinePayload?.baselineVersion===br.baselineVersion);
 if(idMatches.length>1&&idMatches.filter(b=>b.payloadDigest?.value===br.payloadDigest).length>1)return fail("CONFLICTED","AMBIGUOUS_BASELINE_REFERENCE");
 if(idMatches.length===0)return fail("UNAVAILABLE_CURRENT","BASELINE_NOT_RESOLVABLE");
 const baseline=idMatches[0];
 if(baseline.payloadDigest?.value!==br.payloadDigest)return fail("INVALID","BASELINE_INTEGRITY_FAILURE");
 if(baseline.baselinePayload?.configurationId!==br.configurationId)return fail("INVALID","CONFIGURATION_BASELINE_MISMATCH");
 if(baseline.lifecycle?.state!=="APPROVED"||baseline.lifecycle?.eligibleForResolution!==true||!intervalContains({...baseline.baselinePayload.validity,validityEndMode:baseline.baselinePayload.validity.validToUtc===null?"UNBOUNDED":"EXCLUSIVE",intervalSemantics:"HALF_OPEN"},asOfUtc))return fail("INVALID","BASELINE_NOT_APPROVED_EFFECTIVE");
 const ba=baseline.baselinePayload?.authority;
 if(!resolvable(ba?.configurationBaselineOwnerRef)||!resolvable(ba?.configurationBaselineCustodianRef)||!resolvable(ba?.baselineApprovalAuthorityRef))return fail("INVALID","BASELINE_AUTHORITY_INCOMPLETE");
 return{state:"AVAILABLE",reasonCode:"CURRENT_SETUP_RESOLVED",assignment:{revision:r.assignmentPayload.revision},provenance:"PROTECTED_AUTHORITY"};
}
export function assertPublicPayload(value,protectedRecords=[]){
 if(!obj(value))return{valid:false,reasonCode:"PUBLIC_PROJECTION_POLICY"};
 const badKeys=[];const walk=v=>{if(Array.isArray(v))return v.forEach(walk);if(obj(v))for(const[k,x]of Object.entries(v)){if(!PUBLIC_ALLOWLIST.includes(k)&&v===value)badKeys.push(k);walk(x);}};walk(value);
 const text=JSON.stringify(value);const tokens=[];
 for(const r of protectedRecords){for(const t of [r.assignmentPayload?.assignmentId,r.assignmentPayload?.observatoryId,r.payloadDigest?.value,r.assignmentPayload?.siteAuthorityReference?.payloadDigest,r.assignmentPayload?.setupBaselineReference?.payloadDigest,r.assignmentPayload?.authority?.sourceLocator])if(resolvable(t))tokens.push(t);}
 const leaked=tokens.some(t=>text.includes(t));
 const reasonInvalid="publicReasonCode" in value&&!PUBLIC_REASON_CODES.has(value.publicReasonCode);
 return{valid:badKeys.length===0&&!leaked&&!reasonInvalid,reasonCode:badKeys.length||leaked||reasonInvalid?"PUBLIC_PROJECTION_POLICY":null};
}
export function buildPublicReference(r,{publicSetupRef,asOfUtc,availabilityState="AVAILABLE",publicReasonCode="AVAILABLE"}){
 if(r.assignmentPayload?.publicationPolicy?.publicProjection!=="DENY_BY_DEFAULT")throw new Error("PUBLIC_PROJECTION_POLICY");
 const internals=[r.assignmentPayload.assignmentId,r.assignmentPayload.observatoryId,r.payloadDigest.value];
 if(!resolvable(publicSetupRef)||internals.some(x=>publicSetupRef.includes(x)))throw new Error("PUBLIC_PROJECTION_POLICY");
 const base={publicSetupRef,availabilityState,publicReasonCode,asOfUtc,provenance:"SANITIZED_GOVERNED_AUTHORITY"};
 const out={...base,publicEvidenceDigest:digestPayload(base)};if(!assertPublicPayload(out,[r]).valid)throw new Error("PUBLIC_PROJECTION_POLICY");return out;
}
export function redactAuditEvent(e){const allowed=["event","state","reasonCode","correlationId"];return Object.fromEntries(Object.entries(e||{}).filter(([k])=>allowed.includes(k)));}
export function assertBoundarySource(source){const violations=[];if(/node:fs|readFile|readdir/.test(source))violations.push("DOMAIN_INFRASTRUCTURE_DEPENDENCY");if(/EAGLE|N\.I\.N\.A\.|latest session|configuration-summary/i.test(source))violations.push("FORBIDDEN_AUTHORITY_FALLBACK");if(/deviceCommand|readiness|go.no.go|Safety Authority/i.test(source))violations.push("SAFETY_OR_COMMAND_SCOPE");return{valid:violations.length===0,violations};}
export function scanPublicText(text,r,site){
 const forbidden=[r.assignmentPayload.assignmentId,r.payloadDigest.value,r.assignmentPayload.authority.sourceLocator,String(site.sitePayload.geodesy.latitudeDeg),String(site.sitePayload.geodesy.longitudeDeg),site.payloadDigest.value];
 const hits=forbidden.filter(x=>text.includes(x));const elevationLeak=/elevationM\s*[:=]\s*100\b|quota\s+(?:esatta\s+)?(?:di\s+)?100\s*m\b/i.test(text);
 return{valid:hits.length===0&&!elevationLeak,hitCount:hits.length+(elevationLeak?1:0)};
}
async function readJson(path){return JSON.parse(await readFile(path,"utf8"));}
async function docsText(root){let out="";for(const entry of await readdir(root,{withFileTypes:true})){const p=join(root,entry.name);if(entry.isDirectory())out+=await docsText(p);else if(extname(entry.name)===".md"||extname(entry.name)===".json"||extname(entry.name)===".html")out+=await readFile(p,"utf8");}return out;}
async function main(){
 const root=resolve(fileURLToPath(new URL("../../..",import.meta.url)));
 const p=x=>join(root,x);
 const [r,d,site,baseline,as,ds]=await Promise.all([
  readJson(p("governance/setup-authority/setup-assignments/DSG-CURRENT-SETUP-ASSIGNMENT-001.draft.json")),
  readJson(p("governance/setup-authority/decision-evidence/DSG-CURRENT-SETUP-ASSIGNMENT-001.owner-decision.json")),
  readJson(p("governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.approved.json")),
  readJson(p("governance/setup-authority/configuration-baselines/DSG-SETUP-BASELINE-001.approved.json")),
  readJson(p("governance/setup-authority/schemas/current-setup-assignment.schema.json")),
  readJson(p("governance/setup-authority/schemas/setup-assignment-owner-decision.schema.json"))
 ]);
 assertSchemaValidatorParity(as,ds);
 const b=validateBinding(r,d,site,baseline);if(!b.valid)throw new Error("PROTECTED_BINDING_GATE_FAILED:"+b.errors.join(","));
 const resolution=resolveCurrentSetup([r],{observatoryId:r.assignmentPayload.observatoryId,asOfUtc:r.assignmentPayload.validity.validFromUtc,authorized:true,sources:{siteRecords:[site],baselines:[baseline]}});
 if(resolution.state!=="UNAVAILABLE_CURRENT"||resolution.reasonCode!=="NO_APPROVED_ASSIGNMENT")throw new Error("DRAFT_RESOLVER_INELIGIBILITY_FAILED");
 const publicScan=scanPublicText(await docsText(p("docs")),r,site);if(!publicScan.valid)throw new Error("PROTECTED_PUBLICATION_BOUNDARY_FAILED");
 process.stdout.write(JSON.stringify({gate:"PASS",assignmentLifecycle:"DRAFT",resolution:"UNAVAILABLE_CURRENT",detailsRedacted:true})+"\n");
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(()=>{process.stderr.write("Setup assignment governance gate failed; protected details redacted.\n");process.exitCode=1;});
