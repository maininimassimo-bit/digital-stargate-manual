namespace DigitalStarGate.Contracts.Common;

public sealed record ConfigurationKey(string Section, string Name);
public sealed record OptionValue(ConfigurationKey Key, string Value, string Provider, int Priority);
public sealed record SecretReference(ConfigurationKey Key, string Provider, string Reference);
public sealed record ConfigurationHierarchy(IReadOnlyList<string> OrderedProviders);
public sealed record SettingsSnapshot(IReadOnlyDictionary<string, string> Values, DateTimeOffset LoadedAt, string Provider);
