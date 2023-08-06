// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

const L = require('../libs/leaflet.js');
const rasterlayer = require('./RasterLayer.js');
const Spinner = require('spin.js').Spinner;

class PostTileLayer extends L.TileLayer.WMS {}

export class LeafletTileLayerModel extends rasterlayer.LeafletRasterLayerModel {
  defaults() {
    return {
      ...super.defaults(),
      _view_name: 'LeafletTileLayerView',
      _model_name: 'LeafletTileLayerModel',
      bottom: true,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      min_zoom: 0,
      max_zoom: 18,
      bounds: null,
      tile_size: 256,
      attribution:
        'Map data (c) <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
      detect_retina: false,
      no_wrap: false,
      tms: false,
      show_loading: false,
      loading: false,
      show_load_timing: true,
    };
  }
}

export class LeafletTileLayerView extends rasterlayer.LeafletRasterLayerView {
  initialize(parameters) {
    super.initialize(parameters);
    this.loadStartTime = null;
  }

  create_obj() {
    this.obj = L.tileLayer(this.model.get('url'), this.get_options());
    this.model.on('msg:custom', this.handle_message.bind(this));
  }

  leaflet_events() {
    super.leaflet_events();
    this.obj.on('loading', () => {
      this.model.set('loading', true);
      this.model.save_changes();
      if (this.model.get('show_loading')) {
        this.spinner = new Spinner().spin(this.map_view.el);
      }
    });
    this.obj.on('loading-queue', () => {
      if (this.model.get('show_load_timing') && this.model.get('layers')) {
        this.loadStartTime = new Date().getTime();
        console.log(
          `==BEGIN==${this.model.get('layers')}:${this.model.get('name')}: ${this.loadStartTime}`,
        );
      }
    });
    this.obj.on('remove', () => {
      if (this.model.get('show_load_timing') && this.model.get('layers') && this.loadStartTime) {
        this.loadStartTime = null;
        console.log(`==CANCELLED==${this.model.get('layers')}:${this.model.get('name')}`);
      }
    });
    this.obj.on('load', () => {
      this.model.set('loading', false);
      this.model.save_changes();
      this.send({
        event: 'load',
      });
      if (this.model.get('show_loading')) {
        this.spinner.stop();
      }
      if (this.model.get('show_load_timing') && this.model.get('layers') && this.loadStartTime) {
        const endTime = new Date().getTime();
        console.log(
          `===END===${this.model.get('layers')}:${this.model.get('name')}: ${endTime}, duration: ${
            (endTime - this.loadStartTime) / 1000
          }s`,
        );
        this.loadStartTime = null;
      }
    });
    this.obj.on('remove', () => {
      if (this.model.get('show_loading')) {
        this.spinner.stop();
      }
    });
  }

  model_events() {
    super.model_events();
    this.listenTo(
      this.model,
      'change:url',
      function () {
        this.obj.setUrl(this.model.get('url'), true);
        this.obj.refresh();
      },
      this,
    );
  }

  handle_message(content) {
    if (content.msg == 'redraw') {
      this.obj.redraw();
    }
  }
}
