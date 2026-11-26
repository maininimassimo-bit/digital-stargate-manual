'use strict';
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const fs=require('node:fs');
const path=require('node:path');
const {verify,digest}=require('./verifica.cjs');
const [planFile,report]=process.argv.slice(2);
const raw=fs.readFileSync(planFile),p=JSON.parse(raw);
const enc=x=>Buffer.from(JSON.stringify(x));
const generate=()=>crypto.generateKeyPairSync('ed25519');
const pairs={ARB:generate(),RQ:generate(),authority:generate()};
const pub=x=>x.publicKey.export({type:'spki',format:'der'}).toString('base64');
const trust={schema:'BKL046_STREAM34_ROLE_TRUST_V1',arbPublic:pub(pairs.ARB),
             rqPublic:pub(pairs.RQ),enrollmentPublic:pub(pairs.authority)};
const trustRaw=enc(trust),trustSha256=digest(trustRaw);
const context={scope:'BKL046_STREAM34_COMPLETE_VM_LAUNCHER',subjectSha256:p.subjectSha256};

function signed(role, extra={}, overrides={}, signer=role){
  const review=enc({...context,role,decision:'APPROVED',blockers:[],reviewer:role+' fixture',...extra});
  const body={...context,protocol:'BKL046_STREAM34_REVIEW_ORIGIN_V1',role,
              receiptSha256:digest(review),reviewOrigin:'offline-fixture',...overrides};
  const signature=crypto.sign(null,enc(body),pairs[signer].privateKey).toString('base64');
  return {receipt:review,origin:enc({body,signature})};
}
const ARB=signed('ARB');
const rqExtras={arbSha256:digest(ARB.receipt)};
const RQ=signed('RQ',rqExtras);
const reviews={ARB,RQ};
const base={subjectSha256:p.subjectSha256,trustRaw,trustSha256,reviews};
const outcomes={};
outcomes.arbOnly=verify({...base,reviews:{ARB}}).status;
outcomes.complete=verify(base).status;
assert.deepEqual(outcomes,{arbOnly:'ARB_VERIFIED_RQ_PENDING',complete:'BOTH_RECEIPTS_VERIFIED'});
const refusals={};
function failure(label,expected,input) {
  assert.throws(()=>verify(input),{message:expected});
  refusals[label]=expected;
}
failure('rqBeforeArb','ARB_REQUIRED_FIRST',{...base,reviews:{RQ}});
failure('wrongTrustPin','TRUST_DIGEST_CHANGED',{...base,trustSha256:'f'.repeat(64)});
const repeated=enc({...trust,rqPublic:trust.arbPublic});
failure('sameTrustKey','TRUST_ROLES_NOT_INDEPENDENT',{...base,trustRaw:repeated,trustSha256:digest(repeated)});
failure('foreignSubject','APPROVAL_SUBJECT_CHANGED',{...base,subjectSha256:'e'.repeat(64)});
failure('historicalSubjectInOrigin','ORIGIN_BINDING_MISMATCH',
        {...base,reviews:{ARB:signed('ARB',{}, {subjectSha256:'e'.repeat(64)}),RQ}});
failure('signatureFromDifferentRole','ORIGIN_SIGNATURE_INVALID',
        {...base,reviews:{ARB,RQ:signed('RQ',rqExtras,{},'ARB')}});
failure('arbRequestedChanges','REVIEW_NOT_APPROVED',
        {...base,reviews:{ARB:signed('ARB',{decision:'CHANGES_REQUIRED'}),RQ}});
failure('arbApparentApprovalWithBlockers','REVIEW_NOT_APPROVED',
        {...base,reviews:{ARB:signed('ARB',{blockers:['fixture blocker']}),RQ}});
failure('sameReviewer','RQ_ARB_LINK',
        {...base,reviews:{ARB,RQ:signed('RQ',{...rqExtras,reviewer:'ARB fixture'})}});
failure('rqOtherArb','RQ_ARB_LINK',
        {...base,reviews:{ARB,RQ:signed('RQ',{arbSha256:'f'.repeat(64)})}});
failure('modifiedReceipt','ORIGIN_BINDING_MISMATCH',
        {...base,reviews:{ARB,RQ:{...RQ,receipt:Buffer.concat([RQ.receipt,Buffer.from('\n')])}}});
failure('rqUnlinkedOrigin','ORIGIN_BINDING_MISMATCH',
        {...base,reviews:{ARB,RQ:signed('RQ',rqExtras,{receiptSha256:'f'.repeat(64)})}});
failure('unsignedTimeOrderCannotAuthorize','ORIGIN_BINDING_MISMATCH',
        {...base,reviews:{ARB,RQ:signed('RQ',rqExtras,{reviewOrigin:''})}});
const summary={schema:'BKL046_STREAM34_REVIEW_INTAKE_OFFLINE_RESULT_V1',protocolSha256:digest(raw),
   programSha256:digest(fs.readFileSync(path.join(__dirname,'verifica.cjs'))),
   subjectSha256:p.subjectSha256,outcomes,refusals,actualApprovalsVerified:false,
   enrollmentAttempted:false,admissionRequested:false,nativeExecutions:0,scientificClosures:0};
fs.writeFileSync(report,JSON.stringify(summary,null,2)+'\n',{flag:'wx'});
