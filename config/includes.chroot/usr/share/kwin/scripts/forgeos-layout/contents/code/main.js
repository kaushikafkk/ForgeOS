function normalized(value) {
    return (value || "").toString().toLowerCase();
}

function placeForgeWindow(window) {
    var klass = normalized(window.resourceClass);
    var caption = normalized(window.caption);
    var area = workspace.clientArea(KWin.MaximizeArea, window);
    var gap = Math.max(24, Math.round(area.width * 0.025));
    var top = area.y + Math.max(70, Math.round(area.height * 0.095));

    if (klass.indexOf("org.forgeos.hub") !== -1 || klass.indexOf("forge-hub") !== -1 || caption === "forge hub") {
        var hubWidth = Math.min(468, Math.round(area.width * 0.32));
        var hubHeight = Math.min(650, area.height - (top - area.y) - 34);
        window.frameGeometry = {
            x: area.x + area.width - hubWidth - gap,
            y: top,
            width: hubWidth,
            height: hubHeight
        };
        window.keepAbove = false;
        return;
    }

    if (klass.indexOf("konsole") !== -1) {
        var reserved = Math.min(535, Math.round(area.width * 0.37));
        var shellWidth = Math.max(620, area.width - reserved - gap * 2);
        var shellHeight = Math.min(650, area.height - (top - area.y) - 34);
        window.frameGeometry = {
            x: area.x + Math.max(92, gap * 2),
            y: top,
            width: shellWidth,
            height: shellHeight
        };
    }
}

workspace.windowAdded.connect(function (window) {
    setTimeout(function () { placeForgeWindow(window); }, 350);
});
