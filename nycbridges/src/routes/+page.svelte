<script>
	import TableChartCombo from '$lib/components/TableChartCombo.svelte';
	import Map from '$lib/components/Map.svelte';
	import Chart from '$lib/components/Chart.svelte';
	import titleSvg from '$lib/assets/title.svg';
	import bikeSvg from '$lib/assets/bike.svg';

	const subtitle = 'I biked every* bridge in NYC.<br>Here&apos;s what the data shows.';
</script>

<div class="article">
	<header>
		<div class="title-container">
			<img class="title-svg" src={titleSvg} alt="Which NYC Bridge Is the Worst to Bike?" />
			<div class="subtitle">{@html subtitle}</div>
			<div class="byline">
				By <a href="https://austinsteinhart.com" target="_blank" rel="noopener noreferrer"
					>Austin Steinhart</a
				>
			</div>
		</div>
	</header>

	<img class="page-break" src={bikeSvg} alt="bike" />

	<div class="body">
		<p>
			There are a lot of bridges in New York City. The most recent bridge inventory by the NYC
			Department of Transportation put the number somewhere around XXX.
		</p>
		<p>
			I biked over every single one of them. I wanted to see if there were any patterns in the data,
			and if so, what they might reveal about the city.
		</p>
		<div class="scrolly">
			<div class="background">
				<div class="chart-sticky">
					<Chart />
				</div>
			</div>
			<div class="foreground">
				<div class="steps">
					<div class="step">Step 1</div>
					<div class="step">Step 2</div>
					<div class="step">Step 3</div>
				</div>
			</div>
			<p>
				There are a lot of bridges in New York City. The most recent bridge inventory by the NYC
				Department of Transportation put the number somewhere around XXX.
			</p>
			<p>
				I biked over every single one of them. I wanted to see if there were any patterns in the
				data, and if so, what they might reveal about the city.
			</p>
		</div>
		<div class="map-section">
			<Map />
		</div>
		<p>
			There are a lot of bridges in New York City. The most recent bridge inventory by the NYC
			Department of Transportation put the number somewhere around XXX.
		</p>
		<p>
			I biked over every single one of them. I wanted to see if there were any patterns in the data,
			and if so, what they might reveal about the city.
		</p>
		<div class="chart-section">
			<Chart />
		</div>
		<p>
			There are a lot of bridges in New York City. The most recent bridge inventory by the NYC
			Department of Transportation put the number somewhere around XXX.
		</p>
		<p>
			I biked over every single one of them. I wanted to see if there were any patterns in the data,
			and if so, what they might reveal about the city.
		</p>
		<div class="combo-section">
			<TableChartCombo />
		</div>
		<p>
			There are a lot of bridges in New York City. The most recent bridge inventory by the NYC
			Department of Transportation put the number somewhere around XXX.
		</p>
		<p>
			I biked over every single one of them. I wanted to see if there were any patterns in the data,
			and if so, what they might reveal about the city.
		</p>
	</div>
</div>

<style>
	.article {
		width: 60%;
		min-width: 400px;
		max-width: 800px;
		margin: 0 auto;
		text-align: center;
	}

	.background {
		position: sticky;
		height: 100dvh;
		top: 0;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.foreground {
		position: relative;
	}

	.steps {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.step {
		font-size: 1.5rem;
		padding: 1rem;
		border: 1px solid #999;
		margin-bottom: 50vh;
		border-radius: 8px;
		background: #f0f0f0;
	}

	.chart-sticky {
		width: 100%;
	}

	.map-section {
		margin: 0 auto;
		height: 80dvh;
		width: 50%;
	}
	.chart-section {
		margin: 0 auto;
		width: 100%;
	}

	.title-svg {
		display: block;
		width: 100%;
		height: auto;
	}
	.page-break {
		margin: 1rem auto;
		width: 100%;
		max-width: 50px;
		height: auto;
	}

	.subtitle {
		margin: 0 auto;
		margin-top: -6rem;
		font-size: 1.4rem;
		width: 90%;
		font-weight: 400;
	}

	.byline {
		margin: 1.2rem 0 0;
		font-size: clamp(1.05rem, 2vw, 1.65rem);
	}

	.byline a {
		color: inherit;
		text-decoration: none;
	}

	.byline a:hover {
		text-decoration: underline;
	}

	.body {
		margin: 0 auto;
		margin-top: 1.9rem;
	}

	p {
		text-align: left;
		font-size: 1.5rem;
		padding-bottom: 1.5rem;
	}

	.combo-section {
		/* break out of the narrow article column so the 1/3 + 2/3 split has room */
		width: min(96vw, 1200px);
		margin: 3rem calc(50% - min(48vw, 600px)) 0;
	}

	@media (max-width: 760px) {
		.article {
			width: min(100vw - 1rem, 1200px);
		}

		.subtitle {
			margin-top: 0.7rem;
		}

		p {
			font-size: 1.2rem;
		}
	}
</style>
