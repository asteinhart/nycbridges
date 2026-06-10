<script>
	import Map from '$lib/components/Map.svelte';
	import Chart from '$lib/components/Chart.svelte';
	import BridgeTable from '$lib/components/BridgeTable.svelte';

	// Which view fills the right (or, for `table`, the full) panel.
	let view = $state('map');

	const views = [
		{ id: 'map', label: 'Map' },
		{ id: 'chart', label: 'Chart' },
		{ id: 'table', label: 'Table' }
	];
</script>

<div class="combo">
	<div class="toolbar">
		{#each views as v (v.id)}
			<button class:active={view === v.id} onclick={() => (view = v.id)}>
				{v.label}
			</button>
		{/each}
	</div>

	{#if view === 'table'}
		<!-- Full-width table -->
		<div class="full-panel">
			<BridgeTable />
		</div>
	{:else}
		<!-- Split: 1/3 bridge list + 2/3 swappable map/chart -->
		<div class="split">
			<div class="left">
				<BridgeTable compact />
			</div>
			<div class="right">
				{#if view === 'map'}
					<Map />
				{:else if view === 'chart'}
					<Chart />
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.combo {
		width: 100%;
		text-align: left;
	}

	.toolbar {
		display: flex;
		gap: 0.5rem;
		justify-content: center;
		margin-bottom: 0.75rem;
	}

	.toolbar button {
		font-family: 'Urbanist', sans-serif;
		font-size: 0.9rem;
		padding: 0.35rem 0.9rem;
		border: 1px solid #999;
		border-radius: 999px;
		background: transparent;
		color: #555;
		cursor: pointer;
	}

	.toolbar button.active {
		background: #555;
		color: #fff;
		border-color: #555;
	}

	.split {
		display: flex;
		gap: 1.5rem;
		align-items: stretch;
		height: 80dvh;
	}

	.left {
		flex: 1 1 0;
		min-width: 0;
		overflow-y: auto;
	}

	.right {
		flex: 2 1 0;
		min-width: 0;
		background: rgba(255, 255, 255, 0.34);
		overflow: hidden;
		box-shadow: 0 24px 60px rgba(6, 6, 6, 0.08);
	}

	.full-panel {
		width: 100%;
		overflow-x: auto;
	}

	@media (max-width: 760px) {
		.split {
			flex-direction: column;
			height: auto;
		}

		.right {
			height: 70dvh;
		}
	}
</style>
