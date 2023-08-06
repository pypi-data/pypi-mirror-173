const widgets = require('@jupyter-widgets/base');

function camel_case(input) {
  // Convert from foo_bar to fooBar
  return input.toLowerCase().replace(/_(.)/g, function (match, group1) {
    return group1.toUpperCase();
  });
}

export class LeafletWidgetView extends widgets.WidgetView {}
export class LeafletDOMWidgetView extends widgets.DOMWidgetView {}

class leafletViewCommon {
  get_options() {
    var o = this.model.get('options');
    var use_camel_case = this.model.get('camel_case');
    var options = {};
    var key;
    for (var i = 0; i < o.length; i++) {
      key = o[i];
      if (key === 'camel_case') {
        continue;
      }
      // Convert from foo_bar to fooBar that Leaflet.js uses
      if (!!use_camel_case) {
        options[camel_case(key)] = this.model.get(key);
      } else {
        options[key] = this.model.get(key);
      }
    }
    return options;
  }
}

function applyMixins(derivedCtor, baseCtors) {
  baseCtors.forEach((baseCtor) => {
    Object.getOwnPropertyNames(baseCtor.prototype).forEach((name) => {
      Object.defineProperty(
        derivedCtor.prototype,
        name,
        Object.getOwnPropertyDescriptor(baseCtor.prototype, name),
      );
    });
  });
}

applyMixins(LeafletWidgetView, [leafletViewCommon]);
applyMixins(LeafletDOMWidgetView, [leafletViewCommon]);
