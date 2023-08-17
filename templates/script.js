function addDropdown() {
    var dropdowns = document.getElementById("dropdowns");

    var numDropdowns = dropdowns.childElementCount / 2;
    var label = document.createElement("label");
    label.setAttribute("for", "property" + (numDropdowns + 1));
    label.textContent = "Select property " + (numDropdowns + 1) + ":";
    var select = document.createElement("select");
    select.setAttribute("name", "property" + (numDropdowns + 1));
    select.setAttribute("id", "property" + (numDropdowns + 1));

    // Generate options dynamically using JavaScript
    var all_properties_list = {{ all_properties_list|tojson }};
    for (var i = 0; i < all_properties_list.length; i++) {
        var option = document.createElement("option");
        option.setAttribute("value", all_properties_list[i]);
        option.textContent = all_properties_list[i];
        select.appendChild(option);
    }

    var br = document.createElement("br");
    dropdowns.appendChild(label);
    dropdowns.appendChild(select);
    dropdowns.appendChild(br);
}