// Date Range Picker

$(function () {
    // Initialize Date Range Picker
    $('input[name="daterange"]').daterangepicker({
        autoUpdateInput: false,
        locale: {
            format: "YYYY-MM-DD",
            separator: " - ",
            applyLabel: "Apply",
            cancelLabel: "Clear",
        },
    });

    // Update input field when dates are selected
    $('input[name="daterange"]').on("apply.daterangepicker", function (ev, picker) {
        $(this).val(picker.startDate.format("YYYY-MM-DD") + " - " + picker.endDate.format("YYYY-MM-DD"));
    });

    // Clear input field when canceled
    $('input[name="daterange"]').on("cancel.daterangepicker", function (ev, picker) {
        $(this).val("");
    });
});

