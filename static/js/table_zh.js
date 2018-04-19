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
            url: "/search/data/zh/?region_lst=" + id_array.join(","),
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
                title: "区域",
                className: "data-table"
            },
            {
                data: "Address",
                title: "小区",
                className: "data-table"
            },
            {
                data: "Style",
                title: "户型",
                className: "data-table"
            },
            {
                data: "TotalPriceCNY",
                title: "总价（万元）",
                className: "data-table"
            },
            {
                data: "TotalAreaSqM",
                title: "面积（平米）",
                className: "data-table"
            },
            {
                data: "UnitPriceCNY",
                title: "单价（元/平米）",
                className: "data-table"
            },
        ],
        scrollY: 400,
        pageLength: 50,
        lengthMenu: [[25, 50, 100, -1], [25, 50, 100, "ALL"]]
    });
};