using NINA.Core.Enum;
using NINA.Equipment.Equipment.MyDome;
using NINA.Equipment.Interfaces.Mediator;
using NINA.Plugin;
using NINA.Plugin.Interfaces;
using System;
using System.Collections.Generic;
using System.ComponentModel.Composition;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Web.Script.Serialization;

namespace DigitalStarGate.Nina.DomeTelemetryExporter {
    [Export(typeof(IPluginManifest))]
    public sealed class DomeTelemetryExporterPlugin : PluginBase, IDomeConsumer {
        private readonly IDomeMediator domeMediator;
        private readonly string projectionPath;
        private bool disposed;

        [ImportingConstructor]
        public DomeTelemetryExporterPlugin(IDomeMediator domeMediator) {
            this.domeMediator = domeMediator ?? throw new ArgumentNullException(nameof(domeMediator));

            var localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            projectionPath = Path.Combine(localAppData, "DigitalStarGate", "telemetry", "nina-dome.json");

            domeMediator.RegisterConsumer(this);

            try {
                WriteProjection(domeMediator.GetInfo(), null);
            } catch (Exception ex) {
                WriteProjection(null, "MEDIATOR_INFO_UNAVAILABLE:" + ex.GetType().Name);
            }
        }

        public void UpdateDeviceInfo(DomeInfo deviceInfo) {
            if (disposed) {
                return;
            }

            try {
                WriteProjection(deviceInfo, null);
            } catch {
                // Observatory Status telemetry is non-authoritative and must never break N.I.N.A.
                // A failed write simply means the external projection will age to stale/UNKNOWN.
            }
        }

        public override Task Teardown() {
            Dispose();
            return base.Teardown();
        }

        public void Dispose() {
            if (disposed) {
                return;
            }

            disposed = true;
            try {
                domeMediator.RemoveConsumer(this);
            } catch {
                // Teardown must remain best-effort and must not affect N.I.N.A. shutdown.
            }
        }

        private void WriteProjection(DomeInfo info, string explicitReason) {
            var connected = info != null && info.Connected;
            var state = connected ? MapState(info.ShutterStatus) : "UNKNOWN";
            var reason = explicitReason;

            if (string.IsNullOrWhiteSpace(reason)) {
                if (info == null) {
                    reason = "NO_DOME_INFO";
                } else if (!info.Connected) {
                    reason = "DOME_DISCONNECTED";
                } else if (state == "UNKNOWN") {
                    reason = "UNMAPPED_SHUTTER_STATE";
                } else {
                    reason = null;
                }
            }

            var payload = new Dictionary<string, object> {
                { "schemaVersion", 1 },
                { "source", "nina-dome-exporter" },
                { "connected", connected },
                { "state", state },
                { "rawShutterStatus", info == null ? null : info.ShutterStatus.ToString() },
                { "observedAtUtc", DateTime.UtcNow.ToString("o") },
                { "reason", reason }
            };

            var serializer = new JavaScriptSerializer();
            var json = serializer.Serialize(payload);

            var directory = Path.GetDirectoryName(projectionPath);
            Directory.CreateDirectory(directory);

            var tempPath = projectionPath + ".tmp";
            File.WriteAllText(tempPath, json, new UTF8Encoding(false));

            if (File.Exists(projectionPath)) {
                var backupPath = projectionPath + ".bak";
                try {
                    File.Replace(tempPath, projectionPath, backupPath, true);
                    TryDelete(backupPath);
                } catch (PlatformNotSupportedException) {
                    ReplaceByMove(tempPath);
                }
            } else {
                File.Move(tempPath, projectionPath);
            }
        }

        private void ReplaceByMove(string tempPath) {
            TryDelete(projectionPath);
            File.Move(tempPath, projectionPath);
        }

        private static void TryDelete(string path) {
            try {
                if (File.Exists(path)) {
                    File.Delete(path);
                }
            } catch {
            }
        }

        private static string MapState(ShutterState shutterStatus) {
            switch (shutterStatus) {
                case ShutterState.ShutterOpen:
                    return "OPEN";
                case ShutterState.ShutterClosed:
                    return "CLOSED";
                case ShutterState.ShutterOpening:
                case ShutterState.ShutterClosing:
                    return "MOVING";
                case ShutterState.ShutterError:
                    return "FAULT";
                default:
                    return "UNKNOWN";
            }
        }
    }
}
