// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

const L = require('../libs/leaflet.js');
const tileLayer = require('./TileLayer.js');
const proj = require('../projections.js');

export class LeafletPostWMSLayerModel extends tileLayer.LeafletTileLayerModel {
  defaults() {
    return {
      ...super.defaults(),
      _view_name: 'LeafletPostWMSLayerView',
      _model_name: 'LeafletPostWMSLayerModel',
      layers: '',
      styles: '',
      format: 'image/png',
      transparent: true,
      crs: null,
      uppercase: true,
    };
  }
}

export class LeafletPostWMSLayerView extends tileLayer.LeafletTileLayerView {
  create_obj() {
    this.obj = L.tileLayer.postwms(this.model.get('url'), {
      ...this.get_options(),
      crs: proj.getProjection(this.model.get('crs')),
    });
  }

  model_events() {
    super.model_events();

    for (var option in this.get_options()) {
      this.model.on('change:' + option, () => {
        this.obj.setParams(this.get_options(), true);
        this.obj.refresh();
      });
    }
  }
}
