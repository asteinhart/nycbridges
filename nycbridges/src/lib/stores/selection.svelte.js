// Shared hover/selection state across the table, map, and chart.
// The bridge slug (e.g. "george-washington") of the currently hovered bridge,
// or null when nothing is hovered. Using a $state field on an exported object
// so every importer reads/writes the same reactive value.
export const selection = $state({ hovered: null });
