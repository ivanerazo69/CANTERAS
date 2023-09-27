// botón para agrandar toda la pantalla el mapa //
// function toggleFullscreen(mapId) {
//     var map = document.getElementById(mapId);
//     if (!map.fullscreen) {
//       map.requestFullscreen();
//     } else {
//       document.exitFullscreen();
//     }
//     map.fullscreen = !map.fullscreen;
//   }
  
//   function addFullscreenControl(mapId) {
//     var fullscreenBtn = L.Control.extend({
//       options: {
//         position: 'topleft'
//       },
  
//       onAdd: function (map) {
//         var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
//         container.innerHTML = '<a class="fullscreen-map-btn" href="#" title="Full Screen" onclick="toggleFullscreen(\'' + mapId + '\'); return false;"><i class="fa fa-arrows-alt fa-lg"></i></a>';
//         return container;
//       }
//     });
//     map = $('#' + mapId).data('leafletMap');
//     map.addControl(new fullscreenBtn());
//   }
//*********************************************//