using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Threading.Tasks;

namespace DigitalStarGate.Nina.DomeTelemetryExporter;

internal sealed class NetworkTelemetryAdapter {
    private const string InternetAddress = "1.1.1.1";
    private const int InternetPort = 443;
    private const string DnsName = "github.com";
    private static readonly TimeSpan ProbeTimeout = TimeSpan.FromSeconds(3);

    public Dictionary<string, object> Observe() {
        try {
            var route = GetLocalRouteEvidence();
            var gatewayReachable = !string.IsNullOrWhiteSpace(route.Gateway) && TestTcp(route.Gateway, 443, out var gatewayLatencyMs);
            if (!gatewayReachable && !string.IsNullOrWhiteSpace(route.Gateway)) {
                gatewayReachable = TestTcp(route.Gateway, 80, out gatewayLatencyMs);
            }

            var internetReachable = TestTcp(InternetAddress, InternetPort, out var internetLatencyMs);
            var dnsResolved = TestDns(DnsName, out var dnsLatencyMs, out var dnsAddressCount);

            var state = MapState(route.HasUsableInterface, gatewayReachable, internetReachable, dnsResolved);
            var connected = state == "ONLINE" ? true : state == "OFFLINE" ? false : (bool?)null;
            var reason = state switch {
                "ONLINE" => null,
                "DEGRADED" => "PARTIAL_NETWORK_REACHABILITY",
                "OFFLINE" => "NETWORK_UNREACHABLE",
                _ => "NETWORK_STATE_UNDETERMINED"
            };

            return BuildService(connected, state, reason, new Dictionary<string, object> {
                { "interface", route.InterfaceName },
                { "gateway", route.Gateway },
                { "gatewayReachable", gatewayReachable },
                { "gatewayLatencyMs", gatewayLatencyMs },
                { "internetTarget", $"{InternetAddress}:{InternetPort}" },
                { "internetReachable", internetReachable },
                { "internetLatencyMs", internetLatencyMs },
                { "dnsName", DnsName },
                { "dnsResolved", dnsResolved },
                { "dnsLatencyMs", dnsLatencyMs },
                { "dnsAddressCount", dnsAddressCount },
                { "activeLink", null },
                { "vpn", null },
                { "lteFailover", null }
            });
        } catch {
            return BuildService(null, "UNKNOWN", "NETWORK_PROBE_FAILED", new Dictionary<string, object> {
                { "activeLink", null },
                { "vpn", null },
                { "lteFailover", null }
            });
        }
    }

    private static (bool HasUsableInterface, string InterfaceName, string Gateway) GetLocalRouteEvidence() {
        var candidates = NetworkInterface.GetAllNetworkInterfaces()
            .Where(nic => nic.OperationalStatus == OperationalStatus.Up)
            .Where(nic => nic.NetworkInterfaceType != NetworkInterfaceType.Loopback)
            .Select(nic => new {
                Nic = nic,
                Properties = SafeGetIpProperties(nic)
            })
            .Where(x => x.Properties != null)
            .SelectMany(x => x.Properties.GatewayAddresses
                .Where(g => g?.Address != null && g.Address.AddressFamily == AddressFamily.InterNetwork)
                .Where(g => !IPAddress.Any.Equals(g.Address) && !IPAddress.None.Equals(g.Address))
                .Select(g => new { x.Nic, Gateway = g.Address.ToString() }))
            .ToList();

        var selected = candidates.FirstOrDefault();
        return selected == null
            ? (false, null, null)
            : (true, selected.Nic.Name, selected.Gateway);
    }

    private static IPInterfaceProperties SafeGetIpProperties(NetworkInterface nic) {
        try {
            return nic.GetIPProperties();
        } catch {
            return null;
        }
    }

    private static bool TestTcp(string address, int port, out int? latencyMs) {
        latencyMs = null;
        var stopwatch = Stopwatch.StartNew();
        using var client = new TcpClient();
        try {
            var task = client.ConnectAsync(address, port);
            if (!task.Wait(ProbeTimeout)) {
                return false;
            }
            stopwatch.Stop();
            latencyMs = (int)stopwatch.ElapsedMilliseconds;
            return client.Connected;
        } catch {
            return false;
        }
    }

    private static bool TestDns(string name, out int? latencyMs, out int addressCount) {
        latencyMs = null;
        addressCount = 0;
        var stopwatch = Stopwatch.StartNew();
        try {
            Task<IPAddress[]> task = Dns.GetHostAddressesAsync(name);
            if (!task.Wait(ProbeTimeout)) {
                return false;
            }
            stopwatch.Stop();
            var addresses = task.Result ?? Array.Empty<IPAddress>();
            addressCount = addresses.Length;
            latencyMs = (int)stopwatch.ElapsedMilliseconds;
            return addressCount > 0;
        } catch {
            return false;
        }
    }

    private static string MapState(bool routePresent, bool gatewayReachable, bool internetReachable, bool dnsResolved) {
        if (routePresent && gatewayReachable && internetReachable && dnsResolved) {
            return "ONLINE";
        }

        if (!routePresent || (!gatewayReachable && !internetReachable && !dnsResolved)) {
            return "OFFLINE";
        }

        if (gatewayReachable || internetReachable || dnsResolved) {
            return "DEGRADED";
        }

        return "UNKNOWN";
    }

    private static Dictionary<string, object> BuildService(bool? connected, string state, string reason, Dictionary<string, object> details) {
        return new Dictionary<string, object> {
            { "connected", connected },
            { "state", state },
            { "reason", reason },
            { "details", details }
        };
    }
}
