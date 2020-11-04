(function () {
    var h, a, f;
    a = document.getElementsByTagName('link');
    for (h = 0; h < a.length; h++) {
        f = a[h];
        if (f.rel.toLowerCase().match(/stylesheet/) && f.href) {
            var g = f.href.replace(/(&|\?)rnd=\d+/, '');
            f.href = g + (g.match(/\?/) ? '&' : '?');
            f.href += 'rnd=' + (new Date().valueOf());
        }
    } // for
    //alert("[DEVELOPMENT] Reloading CSS cached files.")
})()