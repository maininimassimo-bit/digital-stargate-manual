import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import {
  METHOD, canonicalize, digestPayload, validateAssignment, validateDecisionEvidence,
  validateBinding, assertSchemaValidatorParity, intervalContains, intervalsOverlap,
  resolveCurrentSetup, buildPublicReference, assertPublicPayload, redactAuditEvent,
  assertBoundarySource, scanPublicText
} from "./setup-assignment-validator.mjs";

const START="2026-01-01T00:00:00.000Z",END="2026-02-01T00:00:00.000Z";
const clone=v=>structuredClone(v);
function sourceFixture(){
 const sitePayload={siteRecordId:"SITE-SYNTHETIC-001",revision:1,observatoryId:"OBS-SYNTHETIC-001",validity:{validFromUtc:START,validToUtc:null}};
 const site={lifecycle:{state:"APPROVED",eligibleForResolution:true,approvalEvidenceRef:"protected/site-receipt.json"},sitePayload,payloadDigest:{value:digestPayload(sitePayload)}};
 const baselinePayload={baselineId:"BASE-SYNTHETIC-001",baselineVersion:"1.0.0",configurationId:"CONFIG-SYNTHETIC-001",validity:{validFromUtc:START,validToUtc:null},authority:{configurationBaselineOwnerRef:"owner",configurationBaselineCustodianRef:"custodian",baselineApprovalAuthorityRef:"approver"}};
 const baseline={lifecycle:{state:"APPROVED",eligibleForResolution:true,approvalEvidenceRef:"protected/baseline-receipt.json"},baselinePayload,payloadDigest:{value:digestPayload(baselinePayload)}};
 return{site,baseline};
}
function payload(opts={}){
 const {site,baseline}=sourceFixture();
 return{
  assignmentId:opts.assignmentId||"ASSIGNMENT-SYNTHETIC-001",revision:opts.revision||1,observatoryId:"OBS-SYNTHETIC-001",
  siteAuthorityReference:{recordPath:"protected/site.json",siteRecordId:site.sitePayload.siteRecordId,revision:1,observatoryId:site.sitePayload.observatoryId,payloadDigest:site.payloadDigest.value,lifecycleState:"APPROVED",approvalEvidenceRef:site.lifecycle.approvalEvidenceRef},
  setupBaselineReference:{recordPath:"protected/baseline.json",baselineId:baseline.baselinePayload.baselineId,baselineVersion:baseline.baselinePayload.baselineVersion,configurationId:baseline.baselinePayload.configurationId,payloadDigest:baseline.payloadDigest.value,lifecycleState:"APPROVED",approvalEvidenceRef:baseline.lifecycle.approvalEvidenceRef},
  authority:{authoritySystem:"GITHUB_PROTECTED_REGISTRY",repository:"maininimassimo-bit/digital-stargate-manual",registryRoot:"governance/setup-authority/",authorityScope:"SINGLE_OBSERVATORY_CURRENT_SETUP",authorityRole:"SETUP_ASSIGNMENT_AUTHORITY",assignmentOwnerRef:"github:user:maininimassimo-bit",assignmentCustodianRef:"role:digital-stargate-architecture-office",assignmentApprovalAuthorityRef:"github:user:maininimassimo-bit",custodianMayApprove:false,separationPolicy:"OWNER_MAY_APPROVE_CUSTODIAN_MUST_NOT_APPROVE",sourceLocator:"protected/decision.json"},
  validity:{validFromUtc:opts.validFromUtc||START,validityEndMode:opts.validityEndMode||"UNBOUNDED",validToUtc:opts.validToUtc===undefined?null:opts.validToUtc,intervalSemantics:"HALF_OPEN"},
  scope:"OBSERVATION_PLANNER_READ_ONLY_SETUP_AUTHORITY",classification:"PROTECTED_SETUP_ASSIGNMENT",retention:"APPEND_ONLY_GIT_HISTORY",
  publicationPolicy:{publicProjection:"DENY_BY_DEFAULT",internalIdentifiers:"PROHIBITED",protectedDigests:"PROHIBITED",authorityLocators:"PROHIBITED",exactSiteFacts:"PROHIBITED"},
  intendedUse:"CURRENT_SETUP_RESOLUTION_AFTER_SEPARATE_EXACT_DIGEST_APPROVAL",
  prohibitedUses:["CURRENT_SETUP_RESOLUTION_BEFORE_APPROVAL","DEVICE_COMMAND","SAFETY_AUTHORITY","READINESS_OR_GO_NO_GO","PUBLIC_PROTECTED_ASSIGNMENT_PROJECTION","EAGLE_WORKLOAD","LATEST_WINS_FALLBACK","HOST_OR_SESSION_STATE_AS_AUTHORITY"],
  rollback:{draft:"reviewed revert",futureApproval:"retire and unavailable",retirement:"preserve evidence"}
 };
}
function envelope(opts={}){
 const p=opts.payload||payload(opts);const state=opts.state||"APPROVED";
 return{schemaVersion:"1.0.0-draft",recordType:"DSG_CURRENT_SETUP_ASSIGNMENT",
  lifecycle:{state,eligibleForResolution:state==="APPROVED",approvalEvidenceRef:state==="APPROVED"?"protected/assignment-receipt.json":null,approvedAtUtc:state==="APPROVED"?"2026-01-01T00:00:01.000Z":null,retiredAtUtc:state==="RETIRED"?"2026-03-01T00:00:00.000Z":null,retirementEvidenceRef:state==="RETIRED"?"protected/retirement.json":null,decisionEvidenceRef:"protected/decision.json",statement:"Synthetic fixture."},
  assignmentPayload:p,payloadDigest:{method:METHOD,canonicalization:"recursive object-key sort; array order preserved; compact JSON; UTF-8",algorithm:"SHA-256",value:digestPayload(p)},
  validationEvidence:{jsonParse:{state:"VERIFIED"},schemaValidatorParity:{state:"VERIFIED"},decisionEvidenceBinding:{state:"VERIFIED"},sourceAuthorityBinding:{state:"VERIFIED"},payloadDigestRecomputation:{state:"VERIFIED"},lifecycleIneligibility:{state:"VERIFIED"},executableContractCases:{state:"VERIFIED"},protectedValueLeakScan:{state:"VERIFIED"},runtimeOat:{state:"NOT_APPLICABLE"}}
 };
}
function sync(r){r.payloadDigest.value=digestPayload(r.assignmentPayload);return r;}
function sources(){const {site,baseline}=sourceFixture();return{siteRecords:[site],baselines:[baseline]};}
function resolveOne(r=envelope(),extra={}){return resolveCurrentSetup([r],{observatoryId:"OBS-SYNTHETIC-001",asOfUtc:"2026-01-15T00:00:00.000Z",authorized:true,sources:sources(),...extra});}
function expectError(r,code){const out=validateAssignment(r);assert.equal(out.valid,false);assert.ok(out.errors.includes(code),out.errors.join(","));}

test("A2-P01 one approved exact assignment resolves AVAILABLE",()=>assert.equal(resolveOne().state,"AVAILABLE"));
test("A2-P02 half-open start is inclusive",()=>assert.equal(resolveOne(envelope(),{asOfUtc:START}).state,"AVAILABLE"));
test("A2-P03 instant before exclusive end is available",()=>assert.equal(resolveOne(envelope({validityEndMode:"EXCLUSIVE",validToUtc:END}),{asOfUtc:"2026-01-31T23:59:59.999Z"}).state,"AVAILABLE"));
test("A2-P04 adjacent intervals select only the second at boundary",()=>{const a=envelope({validityEndMode:"EXCLUSIVE",validToUtc:END}),b=envelope({assignmentId:"ASSIGNMENT-SYNTHETIC-002",revision:2,validFromUtc:END});const x=resolveCurrentSetup([a,b],{observatoryId:"OBS-SYNTHETIC-001",asOfUtc:END,authorized:true,sources:sources()});assert.equal(x.state,"AVAILABLE");assert.equal(x.assignment.revision,2);});
test("A2-P05 unbounded interval contains future instants",()=>assert.equal(resolveOne(envelope(),{asOfUtc:"2030-01-01T00:00:00.000Z"}).state,"AVAILABLE"));
test("A2-P06 exact baseline identity version configuration and digest resolve",()=>assert.equal(resolveOne().reasonCode,"CURRENT_SETUP_RESOLVED"));
test("A2-P07 assignment roles are resolvable and separated",()=>assert.equal(validateAssignment(envelope()).valid,true));
test("A2-P08 site baseline and assignment approval evidence are separate",()=>{const r=envelope(),s=sources();assert.equal(new Set([r.lifecycle.approvalEvidenceRef,s.siteRecords[0].lifecycle.approvalEvidenceRef,s.baselines[0].lifecycle.approvalEvidenceRef]).size,3);});
test("A2-P09 retired prior revision and approved successor resolve successor",()=>{const old=envelope({state:"RETIRED"}),next=envelope({revision:2});assert.equal(resolveCurrentSetup([old,next],{observatoryId:"OBS-SYNTHETIC-001",asOfUtc:"2026-01-15T00:00:00.000Z",sources:sources()}).assignment.revision,2);});
test("A2-P10 public reference is minimal and allowlisted",()=>{const r=envelope(),o=buildPublicReference(r,{publicSetupRef:"PUBLIC-SYNTHETIC-001",asOfUtc:START});assert.equal(assertPublicPayload(o,[r]).valid,true);});
test("A2-P11 observed drift is descriptive and does not replace desired",()=>assert.equal(resolveOne(envelope(),{sources:{...sources(),observed:{configurationId:"OTHER"}}}).state,"AVAILABLE"));
test("A2-P12 source order does not alter deterministic resolution",()=>{const r=envelope(),a=resolveCurrentSetup([r],{observatoryId:"OBS-SYNTHETIC-001",asOfUtc:START,sources:sources()}),b=resolveCurrentSetup([r].reverse(),{observatoryId:"OBS-SYNTHETIC-001",asOfUtc:START,sources:sources()});assert.deepEqual(a,b);});

test("A2-N01 absence of assignments is unavailable",()=>assert.equal(resolveCurrentSetup([],{observatoryId:"OBS-SYNTHETIC-001",asOfUtc:START,sources:sources()}).reasonCode,"NO_APPROVED_ASSIGNMENT"));
test("A2-N02 temporal gap is unavailable",()=>assert.equal(resolveOne(envelope({validFromUtc:"2026-02-01T00:00:00.000Z"})).reasonCode,"VALIDITY_GAP"));
test("A2-N03 overlapping approved assignments conflict",()=>{const a=envelope(),b=envelope({assignmentId:"ASSIGNMENT-SYNTHETIC-002",revision:2});assert.equal(resolveCurrentSetup([a,b],{observatoryId:"OBS-SYNTHETIC-001",asOfUtc:START,sources:sources()}).state,"CONFLICTED");});
test("A2-N04 DRAFT never resolves current",()=>assert.equal(resolveOne(envelope({state:"DRAFT"})).reasonCode,"NO_APPROVED_ASSIGNMENT"));
test("A2-N05 RETIRED never resolves current",()=>assert.equal(resolveOne(envelope({state:"RETIRED"})).reasonCode,"NO_APPROVED_ASSIGNMENT"));
test("A2-N06 equal or reversed validity end is invalid",()=>{for(const end of [START,"2025-12-01T00:00:00.000Z"]){const r=envelope({validityEndMode:"EXCLUSIVE",validToUtc:end});assert.equal(resolveOne(r).reasonCode,"INVALID_VALIDITY_INTERVAL");}});
test("A2-N07 non-Z timestamp is invalid",()=>{const r=envelope();r.assignmentPayload.validity.validFromUtc="2026-01-01T00:00:00+00:00";sync(r);expectError(r,"INVALID_VALIDITY_INTERVAL");});
test("A2-N08 null EXCLUSIVE end and sentinel end are invalid",()=>{for(const end of [null,"9999-12-31T23:59:59.999Z"]){const r=envelope({validityEndMode:"EXCLUSIVE",validToUtc:end});expectError(r,"INVALID_VALIDITY_INTERVAL");}});
test("A2-N09 assignment digest mismatch fails integrity",()=>{const r=envelope();r.payloadDigest.value="sha256:"+"0".repeat(64);expectError(r,"ASSIGNMENT_INTEGRITY_FAILURE");});
test("A2-N10 missing assignment authority fails closed",()=>{const r=envelope();r.assignmentPayload.authority.assignmentOwnerRef="";sync(r);expectError(r,"ASSIGNMENT_AUTHORITY_INCOMPLETE");});
test("A2-N11 approved assignment requires approval evidence",()=>{const r=envelope();r.lifecycle.approvalEvidenceRef=null;r.lifecycle.approvedAtUtc=null;expectError(r,"INVALID_APPROVAL_EVIDENCE");});
test("A2-N12 absent Site Authority is unavailable",()=>assert.equal(resolveOne(envelope(),{sources:{siteRecords:[],baselines:sources().baselines}}).reasonCode,"SITE_AUTHORITY_UNAVAILABLE"));
test("A2-N13 site identity or digest mismatch is invalid",()=>{const s=sources();s.siteRecords[0].sitePayload.observatoryId="OTHER";assert.equal(resolveOne(envelope(),{sources:s}).reasonCode,"SITE_ASSIGNMENT_MISMATCH");});
test("A2-N14 missing baseline reference is unavailable",()=>{const r=envelope();r.assignmentPayload.setupBaselineReference=null;sync(r);assert.equal(resolveOne(r).reasonCode,"BASELINE_REFERENCE_MISSING");});
test("A2-N15 absent concrete baseline is unavailable",()=>assert.equal(resolveOne(envelope(),{sources:{siteRecords:sources().siteRecords,baselines:[]}}).reasonCode,"BASELINE_NOT_RESOLVABLE"));
test("A2-N16 duplicate exact baseline references conflict",()=>{const s=sources();s.baselines.push(clone(s.baselines[0]));assert.equal(resolveOne(envelope(),{sources:s}).reasonCode,"AMBIGUOUS_BASELINE_REFERENCE");});
test("A2-N17 DRAFT baseline is not approved effective",()=>{const s=sources();s.baselines[0].lifecycle.state="DRAFT";s.baselines[0].lifecycle.eligibleForResolution=false;assert.equal(resolveOne(envelope(),{sources:s}).reasonCode,"BASELINE_NOT_APPROVED_EFFECTIVE");});
test("A2-N18 incomplete baseline authority is invalid",()=>{const s=sources();s.baselines[0].baselinePayload.authority.configurationBaselineOwnerRef="";assert.equal(resolveOne(envelope(),{sources:s}).reasonCode,"BASELINE_AUTHORITY_INCOMPLETE");});
test("A2-N19 baseline digest mismatch fails integrity",()=>{const r=envelope();r.assignmentPayload.setupBaselineReference.payloadDigest="sha256:"+"f".repeat(64);sync(r);assert.equal(resolveOne(r).reasonCode,"BASELINE_INTEGRITY_FAILURE");});
test("A2-N20 configuration mismatch fails binding",()=>{const r=envelope();r.assignmentPayload.setupBaselineReference.configurationId="OTHER";sync(r);assert.equal(resolveOne(r).reasonCode,"CONFIGURATION_BASELINE_MISMATCH");});
test("A2-N21 AP-006 concept without concrete instance stays unavailable",()=>assert.equal(resolveOne(envelope(),{sources:{siteRecords:sources().siteRecords,baselines:[],architectureConcept:true}}).reasonCode,"BASELINE_NOT_RESOLVABLE"));
test("A2-N22 latest-session input cannot become authority",()=>assert.equal(resolveOne(envelope(),{sources:{...sources(),latestSession:{configurationId:"OTHER"}}}).state,"AVAILABLE"));
test("A2-N23 configuration-summary input cannot become authority",()=>assert.equal(resolveOne(envelope(),{sources:{...sources(),configurationSummary:{configurationId:"OTHER"}}}).state,"AVAILABLE"));
test("A2-N24 overlap never uses revision file order or mtime",()=>{const a=envelope(),b=envelope({assignmentId:"ASSIGNMENT-SYNTHETIC-002",revision:99});for(const list of [[a,b],[b,a]])assert.equal(resolveCurrentSetup(list,{observatoryId:"OBS-SYNTHETIC-001",asOfUtc:START,sources:sources()}).state,"CONFLICTED");});
test("A2-N25 host or EAGLE fallback violates authority boundary",()=>assert.ok(assertBoundarySource("read N.I.N.A. from EAGLE").violations.includes("FORBIDDEN_AUTHORITY_FALLBACK")));
test("A2-N26 observed state cannot mutate desired assignment",()=>{const r=envelope(),before=canonicalize(r.assignmentPayload);resolveOne(r,{sources:{...sources(),observed:{configurationId:"OTHER"}}});assert.equal(canonicalize(r.assignmentPayload),before);});
test("A2-N27 unauthorized caller receives no protected payload",()=>assert.deepEqual(resolveOne(envelope(),{authorized:false}),{state:"UNAVAILABLE_CURRENT",reasonCode:"ACCESS_DENIED",audit:true}));
test("A2-N28 public protected field fails allowlist",()=>assert.equal(assertPublicPayload({assignmentId:"x"},[envelope()]).valid,false));
test("A2-N29 deterministically derived public ref is rejected",()=>{const r=envelope();assert.throws(()=>buildPublicReference(r,{publicSetupRef:"PUBLIC-"+r.assignmentPayload.assignmentId,asOfUtc:START}),/PUBLIC_PROJECTION_POLICY/);});
test("A2-N30 unclassified public projection is unavailable",()=>{const r=envelope();r.assignmentPayload.publicationPolicy.publicProjection="UNCLASSIFIED";sync(r);assert.throws(()=>buildPublicReference(r,{publicSetupRef:"PUBLIC-X",asOfUtc:START}),/PUBLIC_PROJECTION_POLICY/);});
test("A2-N31 conflict evidence cannot enter public output",()=>assert.equal(assertPublicPayload({conflictEvidenceRef:"protected"},[envelope()]).valid,false));
test("A2-N32 authority adapter failure has no fallback",()=>assert.equal(resolveOne(envelope(),{sources:{error:true}}).reasonCode,"AUTHORITY_ADAPTER_FAILURE"));
test("A2-N33 internal reason code cannot enter public projection",()=>assert.equal(assertPublicPayload({publicSetupRef:"PUBLIC-X",publicReasonCode:"BASELINE_INTEGRITY_FAILURE"},[envelope()]).valid,false));

const here=dirname(fileURLToPath(import.meta.url)),root=resolve(here,"../../..");
async function real(name){return JSON.parse(await readFile(join(root,name),"utf8"));}
test("D4-P01 repository DRAFT validates as a closed envelope",async()=>assert.equal(validateAssignment(await real("governance/setup-authority/setup-assignments/DSG-CURRENT-SETUP-ASSIGNMENT-001.draft.json")).valid,true));
test("D4-P02 protected owner decision evidence validates closed",async()=>assert.equal(validateDecisionEvidence(await real("governance/setup-authority/decision-evidence/DSG-CURRENT-SETUP-ASSIGNMENT-001.owner-decision.json")).valid,true));
test("D4-P03 DRAFT binds exact approved authorities without disclosure",async()=>{const [r,d,site,baseline]=await Promise.all([real("governance/setup-authority/setup-assignments/DSG-CURRENT-SETUP-ASSIGNMENT-001.draft.json"),real("governance/setup-authority/decision-evidence/DSG-CURRENT-SETUP-ASSIGNMENT-001.owner-decision.json"),real("governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.approved.json"),real("governance/setup-authority/configuration-baselines/DSG-SETUP-BASELINE-001.approved.json")]);assert.deepEqual(validateBinding(r,d,site,baseline).errors,[]);});
test("D4-P04 repository DRAFT resolves unavailable current",async()=>{const r=await real("governance/setup-authority/setup-assignments/DSG-CURRENT-SETUP-ASSIGNMENT-001.draft.json");assert.equal(resolveCurrentSetup([r],{observatoryId:r.assignmentPayload.observatoryId,asOfUtc:r.assignmentPayload.validity.validFromUtc,sources:{}}).state,"UNAVAILABLE_CURRENT");});
test("D4-P05 schemas match validator closed-key coverage",async()=>{const [a,d]=await Promise.all([real("governance/setup-authority/schemas/current-setup-assignment.schema.json"),real("governance/setup-authority/schemas/setup-assignment-owner-decision.schema.json")]);assert.equal(assertSchemaValidatorParity(a,d).valid,true);});
test("D4-P06 privacy scanner rejects protected literals",async()=>{const [r,site]=await Promise.all([real("governance/setup-authority/setup-assignments/DSG-CURRENT-SETUP-ASSIGNMENT-001.draft.json"),real("governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.approved.json")]);assert.equal(scanPublicText("Generic public statement only.",r,site).valid,true);assert.equal(scanPublicText(r.payloadDigest.value,r,site).valid,false);});

test("PROP-01 adjacent half-open intervals do not overlap",()=>assert.equal(intervalsOverlap({validFromUtc:START,validityEndMode:"EXCLUSIVE",validToUtc:END},{validFromUtc:END,validityEndMode:"UNBOUNDED",validToUtc:null}),false));
test("PROP-02 unbounded interval overlaps any later interval",()=>assert.equal(intervalsOverlap({validFromUtc:START,validityEndMode:"UNBOUNDED",validToUtc:null},{validFromUtc:END,validityEndMode:"UNBOUNDED",validToUtc:null}),true));
test("PROP-03 removing approval cannot increase availability",()=>{const r=envelope();assert.equal(resolveOne(r).state,"AVAILABLE");r.lifecycle.state="DRAFT";r.lifecycle.eligibleForResolution=false;r.lifecycle.approvalEvidenceRef=null;r.lifecycle.approvedAtUtc=null;assert.equal(resolveOne(r).state,"UNAVAILABLE_CURRENT");});
test("PROP-04 public digest is not the protected digest",()=>{const r=envelope(),o=buildPublicReference(r,{publicSetupRef:"PUBLIC-X",asOfUtc:START});assert.notEqual(o.publicEvidenceDigest,r.payloadDigest.value);});
test("PROP-05 audit redaction removes protected fields",()=>assert.deepEqual(redactAuditEvent({event:"DENY",assignmentId:"secret",sourceLocator:"secret"}),{event:"DENY"}));
test("PROP-06 safety and command semantics remain out of scope",()=>assert.ok(assertBoundarySource("deviceCommand readiness go-no-go Safety Authority").violations.includes("SAFETY_OR_COMMAND_SCOPE")));
