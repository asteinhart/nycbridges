<script>
	import Map from '$lib/components/Map.svelte';
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
		margin-top: 1.9rem;
	}

	p {
		text-align: left;
		font-size: 1.5rem;
		padding-bottom: 1.5rem;
	}

	.map-section {
		width: min(100%, 980px);
		height: 540px;
		margin: 0 auto;
		background: rgba(255, 255, 255, 0.34);
		overflow: hidden;
		box-shadow: 0 24px 60px rgba(6, 6, 6, 0.08);
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
