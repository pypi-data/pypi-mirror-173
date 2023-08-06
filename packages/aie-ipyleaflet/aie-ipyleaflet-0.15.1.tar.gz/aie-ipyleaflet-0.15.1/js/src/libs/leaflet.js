const L = require('leaflet');
require('proj4');
require('proj4leaflet');
require('leaflet-defaulticon-compatibility');
// require('leaflet.vectorgrid');
require('leaflet-splitmap');
require('leaflet-draw');
require('leaflet.markercluster');
require('leaflet-velocity');
require('leaflet-measure');
require('./leaflet-heat.js');
require('./leaflet-magnifyingglass.js');
require('./leaflet-no-gap');
require('leaflet-rotatedmarker');
require('leaflet-fullscreen');
require('leaflet-transform');
require('leaflet.awesome-markers');
require('leaflet-search');

const md5 = require('./md5').default;

// Monkey patch GridLayer for smoother URL updates
L.patchGridLayer = function (layer) {
  layer._refreshTileUrl = function (tile, url) {
    //use a image in background, so that only replace the actual tile, once image is loaded in cache!
    var img = new Image();
    img.onload = function () {
      L.Util.requestAnimFrame(function () {
        tile.el.src = url;
      });
    };
    img.src = url;
  };

  layer.refresh = function () {
    //prevent _tileOnLoad/_tileReady re-triggering a opacity animation
    var wasAnimated = this._map._fadeAnimated;
    this._map._fadeAnimated = false;

    for (var key in this._tiles) {
      var tile = this._tiles[key];
      if (tile.current && tile.active) {
        var oldsrc = tile.el.src;
        var newsrc = this.getTileUrl(tile.coords);
        if (oldsrc != newsrc) {
          //L.DomEvent.off(tile, 'load', this._tileOnLoad); ... this doesnt work!
          this._refreshTileUrl(tile, newsrc);
        }
      }
    }

    if (wasAnimated) {
      setTimeout(function () {
        this._map._fadeAnimated = wasAnimated;
      }, 5000);
    }
  };
};

class LayerQueue {
  constructor() {
    this._layers = {};
    this._layerLoading = null;

    this.check = this.check.bind(this);
  }

  check() {
    if (!this._layerLoading) return;

    const layer = this._layers[this._layerLoading];
    if (layer && !layer._noTilesToLoad()) {
      window.requestAnimationFrame(this.check);
      return;
    }

    layer && delete this._layers[this._layerLoading];
    this._layerLoading = null;

    this.loadLayer();
    window.requestAnimationFrame(this.check);
  }

  enqueue(layer, tile, coords) {
    const id = layer._leaflet_id;
    if (!this._layers[id]) {
      this._layers[id] = layer;
    }

    if (!this._layerLoading) {
      this._layerLoading = id;
      this.loadTile(layer, tile, coords);
      layer.fire('loading-queue');
      window.requestAnimationFrame(this.check);
    } else if (this._layerLoading === id) {
      this.loadTile(layer, tile, coords);
    }
  }

  dequeue(layer) {
    const id = layer._leaflet_id;
    // 正在加载的layer，不处理（check中处理）
    if (id === this._layerLoading) return;
    if (this._layers[id]) {
      delete this._layers[id];
    }
  }

  loadTile(layer, tile, coords) {
    tile.src = layer.getTileUrl(coords);
  }

  loadLayer() {
    let layer = null;
    Object.keys(this._layers).forEach((key) => {
      const l = this._layers[key];
      if (!layer || (l.zIndex && l.zIndex > (layer.zIndex || 1))) {
        layer = l;
      }
    });

    if (!layer) return;

    this._layerLoading = layer._leaflet_id;
    layer.fire('loading-queue');
    Object.keys(layer._tiles).forEach((key) => {
      const { el, coords } = layer._tiles[key];
      this.loadTile(layer, el, coords);
    });
  }
}

const layerQueue = new LayerQueue();

var oldTileLayer = L.tileLayer;
L.tileLayer = function (url, options) {
  var obj = oldTileLayer(url, options);
  L.patchGridLayer(obj);
  return obj;
};

var oldWmsLayer = oldTileLayer.wms;
L.tileLayer.wms = function (url, options) {
  var obj = oldWmsLayer(url, options);
  L.patchGridLayer(obj);

  const _getTileUrl = obj.getTileUrl.bind(obj);
  obj.getTileUrl = (coords) => {
    let url = _getTileUrl(coords);
    url = `${url}&req_id=${md5(url)}`;
    return url;
  };

  const _onRemove = obj.onRemove.bind(obj);
  obj.onRemove = (map) => {
    _onRemove(map);
    layerQueue.dequeue(obj);
  };

  obj.createTile = (coords, done) => {
    var tile = document.createElement('img');

    L.DomEvent.on(tile, 'load', L.Util.bind(obj._tileOnLoad, obj, done, tile));
    L.DomEvent.on(tile, 'error', L.Util.bind(obj._tileOnError, obj, done, tile));

    if (obj.options.crossOrigin || obj.options.crossOrigin === '') {
      tile.crossOrigin = obj.options.crossOrigin === true ? '' : obj.options.crossOrigin;
    }

    // for obj new option we follow the documented behavior
    // more closely by only setting the property when string
    if (typeof obj.options.referrerPolicy === 'string') {
      tile.referrerPolicy = obj.options.referrerPolicy;
    }

    // The alt attribute is set to the empty string,
    // allowing screen readers to ignore the decorative image tiles.
    // https://www.w3.org/WAI/tutorials/images/decorative/
    // https://www.w3.org/TR/html-aria/#el-img-empty-alt
    tile.alt = '';

    // tile.src = obj.getTileUrl(coords);
    layerQueue.enqueue(obj, tile, coords);

    return tile;
  };
  // obj.on('tileunload', (params) => {
  //   console.log('tileunload', params);
  // });

  // obj.on('tileabort', (params) => {
  //   console.log('tileabort', params);
  // });

  return obj;
};

L.tileLayer.postwms = function (url, options) {
  const body = options.body;
  if (!!body) {
    delete options.body;
  }
  var obj = oldWmsLayer(url, options);
  L.patchGridLayer(obj);
  // 重写 createTile 方法
  const loadTile = async (url, done, img) => {
    const response = await fetch(url, {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        'Content-type': 'application/json',
      },
    });
    const blobData = await response.blob();
    const fileReader = new FileReader();
    fileReader.onload = () => {
      img.src = fileReader.result;
      done(undefined, img);
    };
    fileReader.readAsDataURL(blobData);
  };
  obj.createTile = (coords, done) => {
    const img = document.createElement('img');
    url = obj.getTileUrl(coords);
    loadTile(url, done, img);
    return img;
  };
  return obj;
};

module.exports = L;
