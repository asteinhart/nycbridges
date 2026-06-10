<script>
import { onMount } from 'svelte';
import maplibregl from 'maplibre-gl';
import mapStyle from '$lib/assets/map-style.json';

onMount(() => {
  const map = new maplibregl.Map({
    container: 'map',
    style: mapStyle, // Map style URL
    center: [-74.006, 40.7128], // Initial map center [lng, lat]
    zoom: 10 // Initial zoom level
  });

  //disable all movement
  map.dragPan.disable();
  map.scrollZoom.disable();
  map.doubleClickZoom.disable();
  map.touchZoomRotate.disable();


 
});

</script>

<div id="map" class="map-container"></div>
<style> 
.map-container {

  width: 100%;
  height: 100%;
}
</style>