/*
 * Digital StarGate — BKL-045 F3-B PixInsight provenance OAT probe
 *
 * Safety / authority boundary:
 * - console-only output;
 * - no image mutation;
 * - no process execution;
 * - no network access;
 * - no catalog write;
 * - actionAuthority is always NONE.
 *
 * Edit only the CONFIG block before running the pilot in PixInsight.
 */

var CONFIG = {
   sessionId: "REPLACE_SESSION_ID",
   target: "REPLACE_TARGET",
   projectId: null,
   campaignId: null,
   hostId: "REPLACE_HOST_ID",
   workspaceId: "REPLACE_WORKSPACE_ID",
   workflowId: "REPLACE_WORKFLOW_ID",
   runId: "REPLACE_RUN_ID",
   declaredBy: "Massimo Mainini",
   declaredSteps: [
      /* Example only — remove or replace with operations you explicitly declare.
      {
         processId: "ManualOperation",
         displayName: "Manual operation",
         parameters: {},
         notes: "Operator-declared step not observable through this pilot"
      }
      */
   ]
};

function requiredText( value, name )
{
   if ( value === null || value === undefined || String( value ).trim().length === 0 || String( value ).indexOf( "REPLACE_" ) === 0 )
      throw new Error( "Configure " + name + " before running the BKL-045 F3-B probe." );
   return String( value );
}

function utcNow()
{
   return new Date().toISOString();
}

function idTimestamp( iso )
{
   return iso.replace( /[-:.]/g, "" );
}

function pixInsightVersion()
{
   var parts = [];
   if ( typeof CoreApplication.versionMajor !== "undefined" ) parts.push( CoreApplication.versionMajor );
   if ( typeof CoreApplication.versionMinor !== "undefined" ) parts.push( CoreApplication.versionMinor );
   if ( typeof CoreApplication.versionRelease !== "undefined" ) parts.push( CoreApplication.versionRelease );
   var value = parts.length > 0 ? parts.join( "." ) : "UNKNOWN";
   if ( typeof CoreApplication.versionBuild !== "undefined" ) value += " build " + CoreApplication.versionBuild;
   return value;
}

function activeViewEvidence()
{
   var w = ImageWindow.activeWindow;
   if ( w.isNull )
      return { activeViewId: null, sourceLocators: ["pjsr:ImageWindow.activeWindow=null"] };
   return {
      activeViewId: w.mainView.id,
      sourceLocators: ["pjsr:ImageWindow.activeWindow.mainView.id=" + w.mainView.id]
   };
}

function declaredSteps( exportedAt )
{
   var result = [];
   for ( var i = 0; i < CONFIG.declaredSteps.length; ++i )
   {
      var x = CONFIG.declaredSteps[i];
      result.push( {
         stepId: "DECLARED-" + (i + 1),
         ordinal: i + 1,
         processId: requiredText( x.processId, "declaredSteps[" + i + "].processId" ),
         displayName: x.displayName || null,
         processVersion: null,
         evidenceClass: "DECLARED",
         capturedAt: null,
         parameters: x.parameters || {},
         sourceLocators: [],
         notes: x.notes || null,
         declaredBy: requiredText( CONFIG.declaredBy, "declaredBy" ),
         declaredAt: exportedAt,
         inputRefs: [],
         outputRefs: [],
         maskRefs: []
      } );
   }
   return result;
}

function buildSidecar()
{
   var exportedAt = utcNow();
   var active = activeViewEvidence();
   var steps = declaredSteps( exportedAt );
   var limitations = [
      "PJSR_PILOT_DOES_NOT_CLAIM_ACCESS_TO_COMPLETE_PIXINSIGHT_PROCESS_HISTORY",
      "NO_OBSERVED_PROCESSING_STEP_IS_EMITTED_BY_THIS_PROBE",
      active.activeViewId === null ? "NO_ACTIVE_IMAGE_WINDOW_AT_CAPTURE_TIME" : "ACTIVE_WINDOW_ID_ONLY_IS_AUTOMATICALLY_OBSERVED"
   ];

   return {
      schemaVersion: "1.0",
      sidecarId: "PXP-" + idTimestamp( exportedAt ) + "-OAT",
      exportedAt: exportedAt,
      authority: "processing_evidence",
      actionAuthority: "NONE",
      source: {
         product: "PixInsight",
         productVersion: pixInsightVersion(),
         hostId: requiredText( CONFIG.hostId, "hostId" ),
         workspaceId: requiredText( CONFIG.workspaceId, "workspaceId" ),
         captureMethod: "GOVERNED_PJSR_EXPORT",
         sourceLocators: ["pjsr:CoreApplication.version"].concat( active.sourceLocators )
      },
      observationContext: {
         sessionId: requiredText( CONFIG.sessionId, "sessionId" ),
         target: requiredText( CONFIG.target, "target" ),
         projectId: CONFIG.projectId,
         campaignId: CONFIG.campaignId
      },
      workflow: {
         workflowId: requiredText( CONFIG.workflowId, "workflowId" ),
         runId: requiredText( CONFIG.runId, "runId" ),
         startedAt: null,
         completedAt: null,
         environment: {
            pixInsightVersion: pixInsightVersion(),
            platform: "PJSR",
            modules: []
         },
         steps: steps,
         inputs: [],
         outputs: []
      },
      capture: {
         completeness: steps.length > 0 ? "PARTIAL" : "UNAVAILABLE",
         limitations: limitations,
         observedStepCount: 0,
         declaredStepCount: steps.length
      }
   };
}

function main()
{
   Console.show();
   var sidecar = buildSidecar();
   Console.writeln( "DSG_PXP_BEGIN" );
   Console.writeln( JSON.stringify( sidecar, null, 2 ) );
   Console.writeln( "DSG_PXP_END" );
   Console.writeln( "BKL-045 F3-B probe completed. No image or catalog mutation was performed." );
}

main();
