// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

const L = require('../libs/leaflet.js');
const tileLayer = require('./TileLayer.js');

export class LeafletTDTLayerModel extends tileLayer.LeafletTileLayerModel {
  defaults() {
    return {
      ...super.defaults(),
      _view_name: 'LeafletTDTLayerView',
      _model_name: 'LeafletTDTLayerModel',
      subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
      key: '2d585d36d89ab86049e29f6f10364dc3',
    };
  }
}

export class LeafletTDTLayerView extends tileLayer.LeafletTileLayerView {
  create_obj() {
    this.obj = L.tileLayer(this.model.get('url'), {
      ...this.get_options(),
      zoomOffset: this.model.get('zoom_offset'),
    });

    // 天地图 as basemap, set z-index as 0
    this.obj.setZIndex(0);
  }
}
