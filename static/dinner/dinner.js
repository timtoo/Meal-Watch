function pad (str, max) {
  return str.length < max ? pad("0" + str, max) : str;
}

var today = function() {
    var d = new Date();
    var iso = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
    return iso;
}

