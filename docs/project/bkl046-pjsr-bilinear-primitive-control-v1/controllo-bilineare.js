/* Callable control body. The reviewed parent owns Image objects and all I/O. */
function bkl046BilinearSampleControl(source, target, phaseX16, phaseY16, interpolationMode) {
   var validPhase = (phaseX16 === 0 && phaseY16 === 0) ||
                    (phaseX16 === 8 && phaseY16 === 0) ||
                    (phaseX16 === 0 && phaseY16 === 8) ||
                    (phaseX16 === 8 && phaseY16 === 8) ||
                    (phaseX16 === 4 && phaseY16 === 12);
   if (!source || !target || source === target || !validPhase || interpolationMode !== 1 ||
       source.width !== 64 || source.height !== 64 || source.numberOfChannels !== 1 ||
       target.width !== 64 || target.height !== 64 || target.numberOfChannels !== 1)
      throw Error("BKL046_CONTROL_INVALID_BINDING");
   var oldMode = source.interpolation;
   var count = 0;
   var primaryFailed = false, primaryFailure;
   try {
      source.interpolation = interpolationMode;
      if (source.interpolation !== interpolationMode)
         throw Error("BKL046_CONTROL_INTERPOLATION_READBACK");
      for (var y = 1; y < 63; ++y)
         for (var x = 1; x < 63; ++x) {
            var v = source.interpolate(x + phaseX16/16, y + phaseY16/16, 0);
            if (typeof v !== "number" || !isFinite(v) || v < 0 || v > 1)
               throw Error("BKL046_CONTROL_INVALID_SAMPLE");
            target.setSample(v, x, y, 0);
            ++count;
         }
   } catch (e) {
      primaryFailed = true;
      primaryFailure = e;
   }
   try {
      source.interpolation = oldMode;
      if (source.interpolation !== oldMode)
         throw Error("BKL046_CONTROL_RESTORE_READBACK");
   } catch (restoreFailure) {
      var failure = Error("BKL046_CONTROL_RESTORE_FAILED");
      failure.primaryFailed = primaryFailed;
      failure.primaryFailure = primaryFailure;
      failure.restoreFailure = restoreFailure;
      throw failure;
   }
   if (primaryFailed)
      throw primaryFailure;
   return count;
}
