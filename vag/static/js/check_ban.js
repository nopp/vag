function verifyHttp() {
    x = document.getElementById('ban_domain');
    if (x.value.slice(0,7) == "http://") {
        x.value = x.value.substring(7)
    }
}
function verifyUri() {
    x = document.getElementById('ban_uri');
    if (x.value[0] == "/") {
        x.value = x.value.substring(1)
    }
}
