function addRowHandlers() {
    var table = document.getElementById("v1Endpoints");
    var rows = table.getElementsByTagName("tr");
    for (i = 0; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler = function(row) {
            return function() { 
                var cell = row.getElementsByTagName("td")[1];
                // retrieving the endpoint only
                var id = cell.innerHTML;
                var v1_pos = id.lastIndexOf("v1/");
                var endpoint = id.substring(v1_pos + 'v1/'.length, id.length);

                // now adding the endpoint to the url
                var url = window.location.href;
                var new_url = url + endpoint;
                //alert("id:" + id + " " + " endpoint:" + endpoint + " " + " url:" + url + " " + " new_url:" + new_url);
                window.open(new_url, "_self")
            };
        };
        currentRow.onclick = createClickHandler(currentRow);
    }
}
window.onload = addRowHandlers();
