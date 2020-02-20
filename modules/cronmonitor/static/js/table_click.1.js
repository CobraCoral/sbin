//<![CDATA[
<script src="static/js/lib/jquery-3.4.1.js"></script>
<script src="static/js/lib/jquery.cycle.all.js"></script>
<script type="text/javascript"> 
//]]>
    function addRowHandlers() {
        var table = document.getElementById("tableId");
        var rows = table.getElementsByTagName("tr");
        for (i = 0; i < rows.length; i++) {
            var currentRow = table.rows[i];
            var createClickHandler = function(row) {
                return function() { 
                    var cell = row.getElementsByTagName("td")[0];
                    var id = cell.innerHTML;
                    alert("id:" + id);
                };
            };
            currentRow.onclick = createClickHandler(currentRow);
        }
    }
    window.onload = addRowHandlers();
//<![CDATA[
</script>

//]]>
