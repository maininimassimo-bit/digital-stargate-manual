import {readFile, realpath, stat} from 'node:fs/promises';
import {createReadStream} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve, sep} from 'node:path';

export async function projectSessionPackage(repoRoot, sessionId) {
  if (!/^\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}$/.test(sessionId)) throw new Error('Invalid session ID');
  const relative=`data/sessions/${sessionId.slice(0,4)}/${sessionId.slice(5,7)}/${sessionId}/manifest.json`;
  const record={sessionId,scope:'SESSION_DOCUMENT_PACKAGE',state:'UNAVAILABLE',manifestRef:relative,fileCount:0,verifiedFileCount:0};
  let manifest;
  const repository=await realpath(repoRoot);
  try {
    const path=await realpath(resolve(repository,relative));
    if(!path.startsWith(repository+sep))return {...record,state:'INVALID'};
    manifest=JSON.parse((await readFile(path,'utf8')).replace(/^\uFEFF/,''));
  }
  catch { return record; }
  if (manifest.schema_version!=='1.0' || manifest.session_id!==sessionId || manifest.report_status!=='COMPLETE' || !Array.isArray(manifest.files) || !manifest.files.length || manifest.files.length>1000) return {...record,state:'INVALID'};
  record.fileCount=manifest.files.length;
  const names=new Set();
  for (const file of manifest.files) {
    if (typeof file.path!=='string' || !/^raw\/[A-Za-z0-9_./ -]+$/.test(file.path) || file.path.split('/').some(p=>!p || p==='.' || p==='..') || names.has(file.path) || !Number.isSafeInteger(file.size_bytes) || file.size_bytes<0 || !/^[a-f0-9]{64}$/i.test(file.sha256 || '')) return {...record,state:'INVALID'};
    names.add(file.path);
  }
  const directory=await realpath(resolve(repoRoot,relative,'..'));
  if(!directory.startsWith(repository+sep))return {...record,state:'INVALID'};
  for (const file of manifest.files) {
    try {
      const path=await realpath(resolve(directory,file.path));
      if (!path.startsWith(directory+sep)) return {...record,state:'INVALID'};
      const metadata=await stat(path);
      if (!metadata.isFile() || metadata.size!==file.size_bytes) continue;
      const hash=createHash('sha256');
      for await (const chunk of createReadStream(path)) hash.update(chunk);
      if (hash.digest('hex')===file.sha256.toLowerCase()) record.verifiedFileCount++;
    } catch { /* Missing/unreadable evidence never becomes verified. */ }
  }
  record.state=record.verifiedFileCount===record.fileCount?'VERIFIED':'INCOMPLETE';
  return record;
}
