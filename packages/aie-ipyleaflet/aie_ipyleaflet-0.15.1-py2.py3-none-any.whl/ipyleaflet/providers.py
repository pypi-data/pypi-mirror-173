from traitlets.utils.bunch import Bunch

providers = Bunch(
   TianDiTu=dict(
    Normal=dict(
      Map='//t{s}.tianditu.gov.cn/vec_{proj}/wmts?layer=vec&style=default&tilematrixset={proj}&Service=WMTS&Request=GetTile&Version=1.0.0&Format=tiles&TileMatrix={z}&TileCol={x}&TileRow={y}&tk={key}',
      Annotion='//t{s}.tianditu.gov.cn/cva_{proj}/wmts?layer=cva&style=default&tilematrixset={proj}&Service=WMTS&Request=GetTile&Version=1.0.0&Format=tiles&TileMatrix={z}&TileCol={x}&TileRow={y}&tk={key}',
    ),
    Satellite=dict(
      Map='//t{s}.tianditu.gov.cn/img_{proj}/wmts?layer=img&style=default&tilematrixset={proj}&Service=WMTS&Request=GetTile&Version=1.0.0&Format=tiles&TileMatrix={z}&TileCol={x}&TileRow={y}&tk={key}',
      Annotion='//t{s}.tianditu.gov.cn/cia_{proj}/wmts?layer=cia&style=default&tilematrixset={proj}&Service=WMTS&Request=GetTile&Version=1.0.0&Format=tiles&TileMatrix={z}&TileCol={x}&TileRow={y}&tk={key}',
    ),
    Terrain=dict(
      Map='//t{s}.tianditu.gov.cn/ter_{proj}/wmts?layer=ter&style=default&tilematrixset={proj}&Service=WMTS&Request=GetTile&Version=1.0.0&Format=tiles&TileMatrix={z}&TileCol={x}&TileRow={y}&tk={key}',
      Annotion='//t{s}.tianditu.gov.cn/cta_{proj}/wmts?layer=cta&style=default&tilematrixset={proj}&Service=WMTS&Request=GetTile&Version=1.0.0&Format=tiles&TileMatrix={z}&TileCol={x}&TileRow={y}&tk={key}',
    ),
    Subdomains=['0', '1', '2', '3', '4', '5', '6', '7'],
    key='2d585d36d89ab86049e29f6f10364dc3',
   ),
)