function search(){
    var id_array = new Array();
    $("input[name='region']:checked").each(function(){
        id_array.push($(this).attr("id"))
    })

    if (typeof(table_obj) != "undefined"){
        table_obj.destroy();
    }

    table_obj = $("#search-table").DataTable({
        ajax: {
            url: "/search/data/?region_lst=" + id_array.join(","),
            dataSrc: ""
        },
        columns: [
            {
                data: "URL",
                title: "URL",
                className: "data-table"
            },
            {
                data: "Region",
                title: "Region",
                className: "data-table"
            },
            {
                data: "NumOfBd",
                title: "NumOfBd",
                className: "data-table"
            },
            {
                data: "TotalPriceUSD",
                title: "TotalPrice(KUSD)",
                className: "data-table"
            },
            {
                data: "TotalAreaSqFt",
                title: "TotalArea(SqFt)",
                className: "data-table"
            },
            {
                data: "UnitPriceUSD",
                title: "UnitPrice(USD/SqFt)",
                className: "data-table"
            },
        ],
        scrollY: 400,
        pageLength: 50,
        lengthMenu: [[25, 50, 100, -1], [25, 50, 100, "ALL"]]
    });
};