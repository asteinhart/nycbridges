<script>
	import { onMount } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import mapStyle from '$lib/assets/map-style.json';
	import { selection } from '$lib/stores/selection.svelte.js';

	const CENTER = [-73.990463, 40.738632];
	const ZOOM = 10;

	// Debug tools (e.g. click-to-log coordinates). Flip to true while authoring.
	const debug = true;

	// Pretty labels from the bridge slug.
	function bridgeName(slug) {
		return (
			slug
				.split('-')
				.map((w) => w[0].toUpperCase() + w.slice(1))
				.join(' ') + ' Bridge'
		);
	}

	// Meters of ground covered by one screen pixel at a given latitude / zoom.
	// maplibre tiles are 512px, so the 256 base constant is scaled accordingly.
	function metersPerPixel(lat, zoom) {
		return (156543.03392 * Math.cos((lat * Math.PI) / 180)) / 2 ** zoom / 2;
	}

	// slug -> generated feature id, so the store (driven by the table) can map a
	// bridge slug back to the map feature it should highlight. Set on load.
	let idBySlug = {};
	// Imperatively toggle a feature's hover state; guarded until the map is ready.
	let applyHover = () => {};

	// React to selection changes that originate elsewhere (e.g. the table).
	$effect(() => {
		applyHover(selection.hovered);
	});

	onMount(() => {
		const map = new maplibregl.Map({
			container: 'map',
			style: mapStyle,
			center: CENTER,
			zoom: ZOOM,
			attributionControl: false
		});

		// // Create a compact attribution control
		// const attribution = new maplibregl.AttributionControl({
		// 	compact: true
		// });
		// map.addControl(attribution, 'bottom-right');

		// Lock the view — this is a static display map.
		map.dragPan.disable();
		map.scrollZoom.disable();
		map.doubleClickZoom.disable();
		map.touchZoomRotate.disable();
		map.keyboard.disable();

		map.on('load', async () => {
			const [lines, mids] = await Promise.all([
				fetch('/data/bridges_lines.geojson').then((r) => r.json()),
				fetch('/data/bridges_midpoints.geojson').then((r) => r.json())
			]);

			// Convert each bridge's enclosing radius (meters) into a pixel radius at
			// our fixed zoom, with a small margin so the circle sits just outside the
			// bridge rather than touching its ends.
			const MARGIN = 1.15;
			for (const f of mids.features) {
				const lat = f.geometry.coordinates[1];
				const r = (f.properties.radius_m * MARGIN) / metersPerPixel(lat, ZOOM);
				f.properties.radius_px = r;
				f.properties.name = bridgeName(f.properties.bridge);
				f.properties.hover = false;
			}

			// generateId assigns sequential ids in feature order, so the index is
			// the feature id maplibre will use for feature-state.
			idBySlug = Object.fromEntries(mids.features.map((f, i) => [f.properties.bridge, i]));

			map.addSource('bridge-lines', { type: 'geojson', data: lines });
			// generateId lets us drive hover via feature-state (features have no id).
			map.addSource('bridge-mids', { type: 'geojson', data: mids, generateId: true });

			// 1. The bridge paths — thick white lines.
			map.addLayer({
				id: 'bridge-lines',
				type: 'line',
				source: 'bridge-lines',
				layout: { 'line-cap': 'round', 'line-join': 'round' },
				paint: {
					'line-color': '#ffffff',
					'line-width': 4
				}
			});

			// 2. Circle around each bridge — thin white stroke, no fill. Turns blue
			//    on hover. The fill is transparent but still hit-tests, so hovering
			//    anywhere inside the circle counts.
			map.addLayer({
				id: 'bridge-circles',
				type: 'circle',
				source: 'bridge-mids',
				paint: {
					'circle-radius': ['get', 'radius_px'],
					'circle-color': 'rgba(0,0,0,0)',
					'circle-stroke-width': 1.5,
					'circle-stroke-color': [
						'case',
						['boolean', ['feature-state', 'hover'], false],
						'#4aa3ff',
						'#ffffff'
					]
				}
			});

			// 3. Bridge name label above the circle — only visible on hover.
			map.addLayer({
				id: 'bridge-labels',
				type: 'symbol',
				source: 'bridge-mids',
				layout: {
					'text-field': ['get', 'name'],
					'text-font': ['Noto Sans Regular'],
					'text-size': 13,
					'text-anchor': 'bottom',
					'text-allow-overlap': true,
					// sit the label just above the circle: radial offset (ems) points up
					// and equals the circle's pixel radius divided by the text size.
					'text-variable-anchor': ['bottom'],
					'text-radial-offset': ['+', ['/', ['get', 'radius_px'], 13], 0.4]
				},
				paint: {
					'text-color': '#4aa3ff',
					'text-halo-color': 'rgba(20,24,40,0.9)',
					'text-halo-width': 1.5,
					'text-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], 1, 0]
				}
			});

			// Hover handling. We hit-test the (transparent) circle fill so anywhere
			// inside counts, and drive the blue/label via feature-state. The shared
			// `selection` store is the source of truth, so the map and table stay in
			// sync; `applyHover` (called by the $effect) does the actual map update.
			let appliedId = null;

			function setFeatureHover(id, state) {
				if (id == null) return;
				map.setFeatureState({ source: 'bridge-mids', id }, { hover: state });
			}

			applyHover = (slug) => {
				const id = slug == null ? null : (idBySlug[slug] ?? null);
				if (id === appliedId) return;
				setFeatureHover(appliedId, false);
				appliedId = id;
				setFeatureHover(appliedId, true);
			};

			// Now that the source/layers exist, apply whatever is already selected.
			applyHover(selection.hovered);

			map.on('mousemove', 'bridge-circles', (e) => {
				selection.hovered = e.features[0].properties.bridge;
				map.getCanvas().style.cursor = 'pointer';
			});

			map.on('mouseleave', 'bridge-circles', () => {
				selection.hovered = null;
				map.getCanvas().style.cursor = '';
			});

			// Debug: log the clicked coordinates so they can be copied into data.
			if (debug) {
				map.on('click', (e) => {
					const { lng, lat } = e.lngLat;
					console.log(`[debug] clicked: [${lng.toFixed(6)}, ${lat.toFixed(6)}]`);
				});
			}
		});
	});
</script>

<div id="map" class="map-container"></div>

<style>
	.map-container {
		width: 100%;
		height: 100%;
	}
</style>
