function crowdseclookup(result) {
    var url = result.base_url + '/smoke?context=' + result.ip;
    window.open(url, "ModalPopUp",
        "toolbar=no," +
        "scrollbars=no," +
        "location=no," +
        "statusbar=no," +
        "menubar=no," +
        "resizable=0," +
        "width=785," +
        "height=625," +
        "left = 300," +
        "right = 300," +
        "top = 90," +
        "bottom=90");
}
