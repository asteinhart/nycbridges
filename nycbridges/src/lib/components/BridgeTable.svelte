<script>
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import { selection } from '$lib/stores/selection.svelte.js';

	// `compact` = sidebar mode (fewer columns). Full mode shows everything.
	let { compact = false } = $props();

	let rows = $state([]);

	function bridgeName(slug) {
		return (
			slug
				.split('-')
				.map((w) => w[0].toUpperCase() + w.slice(1))
				.join(' ') + ' Bridge'
		);
	}

	onMount(async () => {
		const data = await d3.csv('/data/chart_data.csv', (d) => ({
			bridge: d.bridge,
			distance: +d.distance,
			ele: +d.ele,
			ele_change: +d.ele_change
		}));

		// One summary row per bridge.
		rows = d3
			.groups(data, (d) => d.bridge)
			.map(([bridge, values]) => {
				const length = d3.max(values, (d) => d.distance);
				const maxEle = d3.max(values, (d) => d.ele);
				const minEle = d3.min(values, (d) => d.ele);
				const gain = d3.max(values, (d) => d.ele_change);
				return {
					bridge,
					name: bridgeName(bridge),
					length,
					rise: maxEle - minEle,
					gain
				};
			})
			.sort((a, b) => b.length - a.length);
	});

	const fmt = (n) => Math.round(n).toLocaleString();
</script>

<table class:compact>
	<thead>
		<tr>
			<th>Bridge</th>
			<th class="num">Length (m)</th>
			{#if !compact}
				<th class="num">Rise (m)</th>
				<th class="num">Elevation gain (m)</th>
			{/if}
		</tr>
	</thead>
	<tbody>
		{#each rows as row (row.bridge)}
			<tr
				class:highlight={selection.hovered === row.bridge}
				onmouseenter={() => (selection.hovered = row.bridge)}
				onmouseleave={() => (selection.hovered = null)}
			>
				<td>{row.name}</td>
				<td class="num">{fmt(row.length)}</td>
				{#if !compact}
					<td class="num">{fmt(row.rise)}</td>
					<td class="num">{fmt(row.gain)}</td>
				{/if}
			</tr>
		{/each}
	</tbody>
</table>

<style>
	table {
		width: 100%;
		border-collapse: collapse;
		font-family: 'Urbanist', sans-serif;
		font-size: 1rem;
		text-align: left;
	}

	table.compact {
		font-size: 0.9rem;
	}

	th,
	td {
		padding: 0.55rem 0.75rem;
		border-bottom: 1px solid #e2e2e2;
	}

	th {
		font-weight: 600;
		color: #555;
		border-bottom: 2px solid #ccc;
		white-space: nowrap;
	}

	td {
		color: #333;
	}

	.num {
		text-align: right;
		font-variant-numeric: tabular-nums;
	}

	tbody tr {
		cursor: pointer;
	}

	tbody tr.highlight {
		background: rgba(74, 163, 255, 0.18);
	}
</style>
