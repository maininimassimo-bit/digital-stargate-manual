/* Candidate PJSR implementation. A reviewed supervisor must call runCfaXdrzCase
 * inside its admitted process after verifying every frozen input hash. */
var CFA_CONTROL_CASES = {
  "unmasked": {
    "files": [
      "integer-a.xdrz",
      "integer-b-unmasked.xdrz",
      "integer-c.xdrz"
    ],
    "rejection": false
  },
  "mask-green": {
    "files": [
      "integer-a.xdrz",
      "integer-b-mask-green.xdrz",
      "integer-c.xdrz"
    ],
    "rejection": true
  },
  "mask-wrong-channel": {
    "files": [
      "integer-a.xdrz",
      "integer-b-mask-wrong-channel.xdrz",
      "integer-c.xdrz"
    ],
    "rejection": true
  },
  "zero-detector": {
    "files": [
      "integer-a.xdrz",
      "integer-b-zero-detector.xdrz",
      "integer-c.xdrz"
    ],
    "rejection": false
  },
  "zero-reference": {
    "files": [
      "integer-a.xdrz",
      "integer-b-zero-reference.xdrz",
      "integer-c.xdrz"
    ],
    "rejection": false
  }
};
var CFA_FIXTURE = "O:/BKL046-CFA-XDRZ-valor-zero-tre-ingressi-v1/fixture/";

function cfaRequire(value, message) {
   if (!value)
      throw new Error(message);
}

function cfaSet(process, key, value) {
   cfaRequire(typeof process[key] !== "undefined" && typeof value !== "undefined",
              "Unavailable parameter or enumeration: " + key);
   process[key] = value;
   cfaRequire(JSON.stringify(process[key]) === JSON.stringify(value), "Parameter readback differs: " + key);
}

function cfaWriteFits(window, destination) {
   cfaRequire(!File.exists(destination), "FITS destination already exists");
   var format = new FileFormat(".fits", false, true);
   cfaRequire(format && !format.isNull, "FITS writer unavailable");
   var writer = new FileFormatInstance(format);
   cfaRequire(writer && !writer.isNull, "FITS writer creation failed");
   try {
      cfaRequire(writer.create(destination, "non-interactive"), "FITS create failed");
      var options = new ImageDescription;
      options.bitsPerSample = 64;
      options.ieeefpSampleFormat = true;
      cfaRequire(writer.setOptions(options), "FITS options rejected");
      cfaRequire(writer.writeImage(window.mainView.image), "FITS write failed");
      cfaRequire(writer.close(), "FITS close failed");
   } finally {
      if (writer.isOpen)
         writer.close();
   }
   cfaRequire(File.exists(destination), "FITS destination missing");
}

function runCfaXdrzCase(caseId, outputRoot) {
   cfaRequire(Object.prototype.hasOwnProperty.call(CFA_CONTROL_CASES, caseId), "Unknown candidate case");
   cfaRequire(/^O:\/BKL046-CFA-XDRZ-weight-window-runs-v1\/[A-Za-z0-9_-]{12,64}\/products$/.test(outputRoot),
              "Output directory is outside the designated scratch root");
   cfaRequire(File.directoryExists(outputRoot), "Unique output directory is missing");
   var intensity = outputRoot + "/" + caseId + "-rgb.fits";
   var weights = outputRoot + "/" + caseId + "-weight.fits";
   cfaRequire(!File.exists(intensity) && !File.exists(weights), "Output exists");
   var scene = CFA_CONTROL_CASES[caseId];
   cfaRequire(scene.files.length === 3 && scene.files[0] !== scene.files[1] &&
              scene.files[1] !== scene.files[2] && scene.files[0] !== scene.files[2],
              "Need three distinct inputs");
   var inputs = scene.files.map(function (name) {
      var source = CFA_FIXTURE + name;
      cfaRequire(File.exists(source), "Input XDRZ missing: " + name);
      return [true, source, ""];
   });
   var p = new DrizzleIntegration;
   var settings = {
      inputData: inputs,
      onError: DrizzleIntegration.Abort,
      enableCFA: true,
      cfaPattern: DrizzleIntegration.Auto,
      scale: 1,
      dropShrink: 0.70,
      kernelFunction: DrizzleIntegration.Kernel_Square,
      useLUT: false,
      enableRejection: scene.rejection,
      enableImageWeighting: false,
      enableSurfaceSplines: false,
      enableLocalNormalization: false,
      enableAdaptiveNormalization: false,
      truncateOnOutOfRange: false,
      closePreviousImages: false,
      showImages: false
   };
   Object.keys(settings).forEach(function (key) { cfaSet(p, key, settings[key]); });
   cfaRequire(typeof p.toSource === "function", "Effective parameter export unavailable");
   var effective = p.toSource("JavaScript", "control", 0);
   cfaRequire(typeof effective === "string" && effective.length > 0, "Effective parameter export failed");
   var parameterEvent = "DSG_CFA_PARAMETERS " + JSON.stringify({caseId: caseId, settings: settings, source: effective});
   console.writeln(parameterEvent);

   var before = ImageWindow.windows.map(function (w) { return w.mainView.id; });
   cfaRequire(p.executeGlobal() === true, "DrizzleIntegration returned failure");
   var ids = [p.integrationImageId, p.weightImageId];
   cfaRequire(typeof ids[0] === "string" && typeof ids[1] === "string" &&
              ids[0] && ids[1] && ids[0] !== ids[1], "Integration or weight ID missing");
   var outputs = ids.map(function (id) {
      cfaRequire(before.indexOf(id) < 0, "Output ID was already open");
      var win = ImageWindow.windowById(id);
      cfaRequire(win && !win.isNull && win.mainView && win.mainView.image, "Output view not found");
      var image = win.mainView.image;
      cfaRequire(image.width === 32 && image.height === 28 && image.numberOfChannels === 3,
                 "Unexpected output geometry");
      return win;
   });
   cfaWriteFits(outputs[0], intensity);
   cfaWriteFits(outputs[1], weights);
   outputs.forEach(function (win) { win.forceClose(); });
   cfaRequire(ImageWindow.windows.every(function (w) {
      return ids.indexOf(w.mainView.id) < 0;
   }), "Owned result window stayed open");
   var exportEvent = "DSG_CFA_EXPORT " + JSON.stringify({caseId: caseId, intensity: intensity, weights: weights,
      weightWindowId: ids[1], weightMeaning: "NATIVE_WEIGHT_WINDOW_UNCLASSIFIED"});
   console.writeln(exportEvent);
   return [parameterEvent, exportEvent];
}

var CFA_PLAN_SHA256 = "677460604bd564285b0571a7149f22f7ae6ea7aed27e5badc1d71b42b0474a0f";
var CFA_COMPONENT_CONTRACT_SHA256 = "d71f3a4dfc2ae411f4a7da212ef3fb37e4f04149c6b70f426e32f9ed3a20a9a2";

function runCfaXdrzBatch(binding) {
   cfaRequire(binding && binding.operation === "BKL046_CFA_XDRZ_WEIGHT_WINDOW_DSG_SHARED_001" &&
              binding.planSha256 === CFA_PLAN_SHA256 && binding.componentContractSha256 === CFA_COMPONENT_CONTRACT_SHA256,
              "Unexpected CFA batch binding");
   cfaRequire(typeof binding.reservation === "string" &&
              /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(binding.reservation),
              "Unexpected reservation identity");
   var root = "O:/BKL046-CFA-XDRZ-weight-window-runs-v1/" + binding.reservation + "/products";
   cfaRequire(File.directoryExists(root), "Missing unique run directory");
   var eventsFile = root + "/events.txt";
   var doneFile = root + "/batch.done.json";
   cfaRequire(!File.exists(eventsFile) && !File.exists(doneFile), "Event transcript or completion already exists");
   var ids = Object.keys(CFA_CONTROL_CASES);
   cfaRequire(ids.length === 5, "Candidate case count differs");
   ids.forEach(function (label) {
      cfaRequire(!File.exists(root+"/"+label+"-rgb.fits") &&
                 !File.exists(root+"/"+label+"-weight.fits"),"Batch output already present");
   });
   var lines = [];
   ids.forEach(function (label) {
      var result = runCfaXdrzCase(label,root);
      cfaRequire(result.length===2, "Missing case evidence");
      lines = lines.concat(result);
   });
   cfaRequire(lines.length === 2*ids.length, "Incomplete batch transcript");
   var events = lines.join("\n")+"\n";
   cfaRequire(!File.exists(eventsFile), "Event transcript unexpectedly exists");
   File.writeTextFile(eventsFile,events);
   cfaRequire(File.readTextFile(eventsFile) === events, "Transcript readback differs");
   cfaRequire(!File.exists(doneFile), "Completion marker unexpectedly exists");
   var done = JSON.stringify({schema:"BKL046_CFA_XDRZ_BATCH_OUTPUT_MARKER_V1",
      scope:"OUTPUT_MARKER_NOT_ADMISSION",operation:binding.operation,
      planSha256:CFA_PLAN_SHA256,componentContractSha256:CFA_COMPONENT_CONTRACT_SHA256,reservation:binding.reservation,cases:ids})+"\n";
   File.writeTextFile(doneFile,done);
   cfaRequire(File.readTextFile(doneFile) === done, "Completion marker readback differs");
   console.writeln("DSG_CFA_BATCH_COMPLETE "+JSON.stringify({reservation:binding.reservation,cases:ids}));
}
