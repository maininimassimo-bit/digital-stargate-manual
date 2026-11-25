/* PJSR definitions only. No call is made when this file is included.
 * The source-pinned parent must hold private directories and input handles,
 * obtain common R4 admission, and publish the bound acknowledgement.
 */
function DSGRunImageAnalysisControls(directory, operationRef, configSha256) {
   function need(ok, code) { if (!ok) throw Error('DSG_IA_ADAPTER_'+code); }
   function exact(value, keys) {
      return value && typeof value==='object' && !Array.isArray(value) &&
         Object.keys(value).sort().join(',')===keys.slice().sort().join(',');
   }
   function hex(value,length) {
      return typeof value==='string' && value.length===length && /^[a-f0-9]+$/.test(value);
   }
   function asciiPath(value) {
      return typeof value==='string' && /^[A-Za-z]:\/[\x20-\x7e]+$/.test(value) &&
         !/[\\":*?<>|]/.test(value.slice(2)) &&
         value.slice(3).split('/').every(part=>part && part!=='.' && part!=='..' && !/[. ]$/.test(part));
   }
   need(asciiPath(directory) && hex(operationRef,32) && directory.endsWith('/'+operationRef) &&
      hex(configSha256,64),'CONTEXT');
   console.abortEnabled=true;
   need(console.abortEnabled===true,'ABORT_CONTROL');
   const timer=new ElapsedTime;
   const began=Date.now();
   let lastWall=began, lastElapsed=0, deadline=began+10000, timeLimit=10;
   function guard() {
      const wall=Date.now(), elapsed=timer.value;
      need(Number.isFinite(wall) && Number.isFinite(elapsed) && wall>=lastWall &&
         elapsed>=lastElapsed && wall<deadline && elapsed<timeLimit,'BUDGET');
      lastWall=wall;
      lastElapsed=elapsed;
      need(typeof console.abortRequested==='boolean' && console.abortRequested===false,'ABORT');
   }
   function hash(bytes) { return new CryptographicHash(256).hash(bytes).toHex(); }
   function read(path,maxBytes) {
      guard();
      const file=new File;
      try {
         file.openForReading(path);
         const count=file.size;
         need(Number.isInteger(count) && count>0 && count<=maxBytes,'READ_SIZE');
         const raw=file.read(15,count);
         need(raw.length===count && file.size===count,'SHORT_READ');
         return raw;
      } finally {
         if (file.isOpen) file.close();
      }
   }
   function parse(raw) {
      return parseStrictPassiveAsciiJson(raw.toUint8Array(),
         {maxBytes:1048576,checkBudget:guard},'CALIBRATION_PATH_VALUES_512_V1');
   }
   function writeNew(path,value) {
      guard();
      need(!File.exists(path),'OUTPUT_EXISTS');
      const bytes=ByteArray.stringToUTF8(JSON.stringify(value));
      need(bytes.length>0 && bytes.length<=65536,'OUTPUT_SIZE');
      const sha=hash(bytes);
      File.writeFile(path,bytes);
      need(hash(read(path,65536))===sha,'OUTPUT_READBACK');
      guard();
      return sha;
   }
   const configRaw=read(directory+'/runtime-config.json',65536);
   need(hash(configRaw)===configSha256,'CONFIG_HASH');
   const config=parse(configRaw);
   need(exact(config,['protocol','operationRef','requestNonce','deadlineUTC','plan']) &&
      config.protocol==='BKL046_IMAGEANALYSIS_PJSR_CONFIG_V1' && config.operationRef===operationRef &&
      hex(config.requestNonce,32) && config.plan && config.plan.operationRef===operationRef &&
      config.plan.inputRoot===directory+'/inputs','CONFIG');
   const configuredDeadline=typeof config.deadlineUTC==='string' ? Date.parse(config.deadlineUTC) : NaN;
   need(Number.isFinite(configuredDeadline) && new Date(configuredDeadline).toISOString()===config.deadlineUTC &&
      configuredDeadline>began && configuredDeadline-began<=300000,'CONFIG_DEADLINE');
   deadline=configuredDeadline;
   timeLimit=(deadline-began)/1000;
   guard();
   const entrySha=hash(read(directory+'/entry.js',65536));
   const request=directory+'/start-request.json', ack=directory+'/start-ack.json';
   const resultPath=directory+'/measurements.json', receiptPath=directory+'/return.json';
   need([request,ack,resultPath,receiptPath].every(path=>!File.exists(path)),'DIR_NOT_FRESH');
   const requestSha=writeNew(request,{protocol:'BKL046_IMAGEANALYSIS_START_REQUEST_V1',
      operationRef,requestNonce:config.requestNonce,configSha256,entrySha256:entrySha});
   need(typeof processEvents==='function' && typeof msleep==='function','PJSR_WAIT_API');
   while (!File.exists(ack)) { guard(); processEvents(false,1); msleep(20); }
   const ackRaw=read(ack,65536), grant=parse(ackRaw);
   need(exact(grant,['protocol','operationRef','requestNonce','requestSha256','reservation','decision']) &&
      grant.protocol==='BKL046_IMAGEANALYSIS_START_ACK_V1' && grant.operationRef===operationRef &&
      grant.requestNonce===config.requestNonce && grant.requestSha256===requestSha &&
      typeof grant.reservation==='string' && /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(grant.reservation) &&
      grant.decision==='ADMITTED','ACK_BINDING');
   const currentVersion=()=>[CoreApplication.versionMajor,CoreApplication.versionMinor,CoreApplication.versionRelease].join('.')+
      ' build '+CoreApplication.versionBuild;
   const result=DSGImageAnalysisControls(config.plan,{ImageAnalysis,currentVersion,guard,
      fingerprint(path) {
         const raw=read(path,77760);
         return {sha256:hash(raw),byteLength:raw.length};
      }});
   need(Array.isArray(ImageWindow.windows) && ImageWindow.windows.length===0,'NONEMPTY_WORKSPACE');
   const ackSha=hash(ackRaw);
   need(hash(read(ack,65536))===ackSha,'ACK_CHANGED');
   const resultSha=writeNew(resultPath,result);
   const receipt={protocol:'BKL046_IMAGEANALYSIS_RETURN_V1',operationRef,
      requestNonce:config.requestNonce,reservation:grant.reservation,entrySha256:entrySha,
      configSha256,startAckSha256:ackSha,resultSha256:resultSha,
      producerReturned:true,scientificAcceptance:false};
   const receiptSha=writeNew(receiptPath,receipt);
   console.writeln('DSG_BKL046_IMAGEANALYSIS_RETURNED_V1 '+operationRef+' '+receiptSha);
   return receipt;
}
