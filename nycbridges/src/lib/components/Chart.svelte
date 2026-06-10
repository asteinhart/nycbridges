<script>
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import { selection } from '$lib/stores/selection.svelte.js';

	let container; // d3 builds everything inside here; Svelte never touches the svg
	let metric = $state('ele_change');

	const height = 400;
	const margin = { top: 20, right: 20, bottom: 40, left: 40 };

	// Set by onMount so updateChart (called from the buttons) can reach them.
	let updateChart = (m) => {};
	// Set by onMount so the $effect can re-style lines when the selection changes.
	let applyHighlight = () => {};

	// React to the shared selection (from this chart, the table, or the map).
	$effect(() => {
		applyHighlight(selection.hovered);
	});

	onMount(async () => {
		const rows = await d3.csv('/data/chart_data.csv', (d) => ({
			bridge: d.bridge,
			distance: +d.distance,
			ele: +d.ele,
			ele_change: +d.ele_change
		}));

		// One line per bridge, points kept in CSV (distance) order.
		const series = d3
			.groups(rows, (d) => d.bridge)
			.map(([bridge, values]) => ({
				bridge,
				values
			}));

		let width = container.clientWidth || 800;
		const isMobile = () => width < 600;

		const svg = d3
			.select(container)
			.append('svg')
			.attr('viewBox', `0 0 ${width} ${height}`)
			.attr('preserveAspectRatio', 'none');

		const x = d3
			.scaleLinear()
			.domain([0, d3.max(series, (s) => d3.max(s.values, (d) => d.distance))])
			.range([margin.left, width - margin.right]);

		const y = d3.scaleLinear().range([height - margin.bottom, margin.top]);

		const line = d3
			.line()
			.x((d) => x(d.distance))
			.y((d) => y(d.value)); // each point carries a `value` for the active metric

		// y axis: a real d3 axis so transitioning is just `.transition().call(yAxis)`.
		// We use axisRight with the group anchored at the left edge so tick lines
		// extend rightward across the chart (gridlines) while labels sit on the
		// left. Styled to drop the tick marks and domain line.
		const innerWidth = width - margin.left - margin.right;
		const yAxisGen = d3
			.axisRight(y)
			.ticks(5)
			.tickSize(innerWidth)
			.tickPadding(-innerWidth - 25); // pull labels back to the left edge

		// layers
		const yAxis = svg
			.append('g')
			.attr('class', 'y-axis')
			.attr('transform', `translate(${margin.left},0)`);
		const linesG = svg.append('g').attr('class', 'series-layer');
		const xAxis = svg.append('g').attr('class', 'x-axis');

		// x axis: labels every 500 (1000 on mobile), no tick marks. Built once.
		const step = isMobile() ? 1000 : 500;
		const xTicks = d3.range(0, x.domain()[1] + step, step);
		xAxis
			.selectAll('text')
			.data(xTicks)
			.join('text')
			.attr('class', 'x-label')
			.attr('x', (d) => x(d))
			.attr('y', height - margin.bottom + 18)
			.text((d) => d);
		xAxis
			.append('text')
			.attr('class', 'axis-title')
			.attr('x', width / 2)
			.attr('y', height - 4)
			.text('distance (m)');

		// one grey line per bridge, created once; updateChart re-binds the values.
		// Hovering a line (or its hit area) writes to the shared selection store.
		const paths = linesG
			.selectAll('path')
			.data(series, (s) => s.bridge)
			.join('path')
			.attr('class', 'series')
			.style('cursor', 'pointer')
			.on('mouseenter', (event, s) => (selection.hovered = s.bridge))
			.on('mouseleave', () => (selection.hovered = null));

		// Highlight the line matching the current selection; dim the rest.
		applyHighlight = (slug) => {
			paths
				.classed('highlight', (s) => s.bridge === slug)
				.classed('dim', (s) => slug != null && s.bridge !== slug);
			// raise the highlighted line so it draws on top
			paths.filter((s) => s.bridge === slug).raise();
		};

		// The update function — like the axis-transition example: set the active
		// value on the data, update the y domain, then `.transition().call(yAxis)`
		// so d3's axis handles the smooth tick move, and transition the lines on the
		// same duration so everything animates together.
		updateChart = (m) => {
			for (const s of series) for (const d of s.values) d.value = d[m];

			y.domain(d3.extent(series.flatMap((s) => s.values.map((d) => d.value)))).nice();

			yAxis.transition().duration(1000).call(yAxisGen);
			paths
				.transition()
				.duration(1000)
				.attr('d', (s) => line(s.values));
		};

		// initial draw (no transition)
		for (const s of series) for (const d of s.values) d.value = d[metric];
		y.domain(d3.extent(series.flatMap((s) => s.values.map((d) => d.value)))).nice();
		yAxis.call(yAxisGen);
		paths.attr('d', (s) => line(s.values));
		applyHighlight(selection.hovered);
	});

	function setMetric(m) {
		metric = m;
		updateChart(m);
	}
</script>

<div class="controls">
	<button class:active={metric === 'ele_change'} onclick={() => setMetric('ele_change')}>
		Elevation change
	</button>
	<button class:active={metric === 'ele'} onclick={() => setMetric('ele')}> Elevation </button>
</div>

<div class="chart" bind:this={container}></div>

<style>
	.chart {
		width: 100%;
	}

	.controls {
		display: flex;
		gap: 0.5rem;
		justify-content: center;
		margin-bottom: 0.75rem;
	}

	.controls button {
		font-family: 'Urbanist', sans-serif;
		font-size: 0.9rem;
		padding: 0.35rem 0.9rem;
		border: 1px solid #999;
		border-radius: 999px;
		background: transparent;
		color: #555;
		cursor: pointer;
	}

	.controls button.active {
		background: #555;
		color: #fff;
		border-color: #555;
	}

	/* svg + the d3-created elements live inside .chart, so target with :global */
	.chart :global(svg) {
		width: 100%;
		height: auto;
		font-family: 'Urbanist', sans-serif;
	}

	.chart :global(path.series) {
		fill: none;
		stroke: #999;
		stroke-width: 1.5;
		opacity: 0.7;
		transition:
			stroke 0.15s,
			stroke-width 0.15s,
			opacity 0.15s;
	}

	.chart :global(path.series.highlight) {
		stroke: #4aa3ff;
		stroke-width: 3;
		opacity: 1;
	}

	.chart :global(path.series.dim) {
		opacity: 0.2;
	}

	/* d3 y axis: drop the domain line, render ticks as faint gridlines, and
	   style the tick labels (which sit on the left, on the line). */
	.chart :global(.y-axis .domain) {
		display: none;
	}

	.chart :global(.y-axis .tick line) {
		stroke: #ccc;
		stroke-width: 1;
	}

	.chart :global(.y-axis .tick text) {
		fill: #555;
		font-size: 12px;
		text-anchor: start;
	}

	.chart :global(text.x-label) {
		fill: #555;
		font-size: 12px;
		text-anchor: middle;
	}

	.chart :global(text.axis-title) {
		fill: #555;
		font-size: 13px;
		text-anchor: middle;
	}
</style>
