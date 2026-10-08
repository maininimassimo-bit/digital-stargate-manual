// Rectilinear barycentric model only. No matching policy or apparent-place solution.
const finite = v => typeof v === 'number' && Number.isFinite(v);
const fields = ['raDeg','decDeg','parallaxMas','pmRaCosDecMasYr','pmDecMasYr','radialVelocityKmS','fromJulianYear','toJulianYear','timeScale'];
const rad = Math.PI / 180, masRad = rad / 3600000;
export function inspectEpochPosition(v) {
  if (!v || typeof v !== 'object' || Array.isArray(v) || Object.keys(v).length !== fields.length
      || !fields.every(k => Object.hasOwn(v,k)) || v.timeScale !== 'TCB'
      || !fields.slice(0,-1).every(k => v[k] === null || finite(v[k]))) throw new Error('INVALID_EPOCH_POSITION');
  if (v.raDeg !== null && (v.raDeg < 0 || v.raDeg >= 360)
      || v.decDeg !== null && Math.abs(v.decDeg) > 90) throw new Error('INVALID_EPOCH_POSITION');
  const base = {model:'BARYCENTRIC_RECTILINEAR_6D',scientificComparison:'NOT_VALIDATED',
    matchClassification:'NOT_EVALUATED',covariance:null,apparentPlaceComputed:false,
    annualParallaxApplied:false,lightTimeApplied:false,externalRequests:0};
  if (fields.slice(0,-1).some(k => v[k] === null) || v.parallaxMas <= 0)
    return Object.freeze({...base,status:'INCOMPLETE',raDeg:null,decDeg:null,reason:'REQUIRED_MOTION_DISTANCE_OR_EPOCH_UNKNOWN'});
  const a = v.raDeg*rad, d = v.decDeg*rad, t = v.toJulianYear-v.fromJulianYear;
  const r=[Math.cos(d)*Math.cos(a),Math.cos(d)*Math.sin(a),Math.sin(d)];
  const p=[-Math.sin(a),Math.cos(a),0], q=[-Math.sin(d)*Math.cos(a),-Math.sin(d)*Math.sin(a),Math.cos(d)];
  const radial = v.radialVelocityKmS*v.parallaxMas*masRad*31557600/149597870.7;
  const xyz=r.map((x,i)=>x*(1+radial*t)+t*masRad*(v.pmRaCosDecMasYr*p[i]+v.pmDecMasYr*q[i]));
  const n=Math.hypot(...xyz);
  if (!xyz.every(finite) || !finite(n) || n === 0) throw new Error('INVALID_EPOCH_POSITION');
  const ra=(Math.atan2(xyz[1],xyz[0])/rad+360)%360;
  const dec=Math.atan2(xyz[2],Math.hypot(xyz[0],xyz[1]))/rad;
  return Object.freeze({...base,status:'MODEL_COMPUTED',raDeg:ra,decDeg:dec,
    reason:'COVARIANCE_SYSTEMATICS_AND_OBSERVER_TRANSFORM_NOT_VALIDATED'});
}
