/* Offline candidate for the separate CFA origin experiment. */
var CFA_CONTROL_CASES = {
  "zero-origin0": {
    "files": [
      "shear-a-center0-origin0.0.xdrz",
      "shear-b-center0-origin0.0.xdrz",
      "shear-c-center0-origin0.0.xdrz"
    ],
    "rejection": false
  },
  "zero-origin05": {
    "files": [
      "shear-a-center0-origin0.5.xdrz",
      "shear-b-center0-origin0.5.xdrz",
      "shear-c-center0-origin0.5.xdrz"
    ],
    "rejection": false
  },
  "half-origin0": {
    "files": [
      "shear-a-edge05-origin0.0.xdrz",
      "shear-b-edge05-origin0.0.xdrz",
      "shear-c-edge05-origin0.0.xdrz"
    ],
    "rejection": false
  },
  "half-origin05": {
    "files": [
      "shear-a-edge05-origin0.5.xdrz",
      "shear-b-edge05-origin0.5.xdrz",
      "shear-c-edge05-origin0.5.xdrz"
    ],
    "rejection": false
  }
};
var CFA_FIXTURE = "O:/BKL046-CFA-origine-fattoriale-v1/prodotti/xdrz/";

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
   cfaRequire(/^O:\/BKL046-CFA-origine-nativa-v1\/[0-9a-f-]{36}\/outputs$/.test(outputRoot),
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
   var exportEvent = "DSG_CFA_EXPORT " + JSON.stringify({caseId: caseId, intensity: intensity, weights: weights});
   console.writeln(exportEvent);
   return [parameterEvent, exportEvent];
}


var ORIGIN_PLAN_SHA256 = "ab70f00fae2063a3693280036b6bfe166afabdc0a24abec43f761192a31d167a";
var ORIGIN_OPERATION = "BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001";

function runOriginBatch(binding) {
   cfaRequire(binding && binding.operation === ORIGIN_OPERATION &&
              binding.planSha256 === ORIGIN_PLAN_SHA256, "Unexpected origin experiment binding");
   cfaRequire(typeof binding.reservation === "string" &&
              /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(binding.reservation),
              "Invalid experiment reservation");
   var root = "O:/BKL046-CFA-origine-nativa-v1/" + binding.reservation;
   var outputs = root + "/outputs";
   cfaRequire(File.directoryExists(root) && File.directoryExists(outputs), "Missing experiment directories");
   var eventsFile = root + "/events.txt";
   var doneFile = root + "/batch.done.json";
   cfaRequire(!File.exists(eventsFile) && !File.exists(doneFile), "Existing experiment transcript or marker");
   var labels = Object.keys(CFA_CONTROL_CASES);
   cfaRequire(labels.length === 4, "Unexpected case count");
   labels.forEach(function (label) {
      cfaRequire(!File.exists(outputs + '/' + label + '-rgb.fits') &&
                 !File.exists(outputs + '/' + label + '-weight.fits'), "Output namespace already used");
   });
   var events = [];
   labels.forEach(function (label) {
      var lines = runCfaXdrzCase(label, outputs);
      cfaRequire(lines.length === 2, "Missing experiment evidence");
      events = events.concat(lines);
   });
   cfaRequire(events.length === 8, "Incomplete origin experiment transcript");
   var text = events.join("\n") + "\n";
   File.writeTextFile(eventsFile,text);
   cfaRequire(File.readTextFile(eventsFile) === text, "Origin transcript readback differs");
   cfaRequire(!File.exists(doneFile), "Unexpected existing marker");
   var done = JSON.stringify({schema:"BKL046_CFA_ORIGIN_BATCH_MARKER_V1",scope:"OUTPUT_MARKER_NOT_ADMISSION",
      operation:ORIGIN_OPERATION,planSha256:ORIGIN_PLAN_SHA256,reservation:binding.reservation,cases:labels}) + "\n";
   File.writeTextFile(doneFile,done);
   cfaRequire(File.readTextFile(doneFile) === done, "Origin marker readback differs");
}
