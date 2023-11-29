
window.onload = function() {
    var parameters = {
        "container": "ggb-element",
        "width": 600,
        "height": 400,
        "showToolBar": true,
        "showAlgebraInput": true,
        "showMenuBar": true
    };

    var app = new GGBApplet(parameters, '5.0');
    app.inject('ggb-element');
};
