
var dt = {
    "why": "hello",
    "you": "there"
}
$.ajax({
    url: '/learnAjax',
    dataType: 'json',
    type: 'post',
    contentType: 'application/json',
    data: JSON.stringify(dt),
    success: function (data, textStatus, jQxhr) {
        console.log(data)
    },
    error: function (jqXhr, textStatus, errorThrown) {
        console.log(errorThrown);
    }
});


const date = new Date();

const renderCalendar = () => {
    date.setDate(1);

    const monthDays = document.querySelector(".days");

    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();

    const firstDayIndex = date.getDay();

    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();

    const nextDays = 7 - lastDayIndex - 1;

    const months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];


    document.querySelector(".date h1").innerHTML = months[date.getMonth()];

    document.querySelector(".date h2").innerHTML = date.getFullYear();

    let days = "";

    for (let x = firstDayIndex; x > 0; x--) {
        days += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
    }


    for (let i = 1; i <= lastDay; i++) {
        if (i === new Date().getDate() && date.getMonth() === new Date().getMonth()) {
            days += `<div class="current-month today">${i}</div>`;
        }
        else {
            days += `<div class="current-month">${i}</div>`;
        }
    }

    for (let j = 1; j <= nextDays; j++) {
        days += `<div class="next-date">${j}</div>`;
    }
    monthDays.innerHTML = days;

    console.log(document.querySelectorAll(".current-month"));
    document.querySelectorAll(".current-month").forEach(div => div.addEventListener("click", currentMonthListener));
};

document.querySelector(".prev").addEventListener("click", () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
});

document.querySelector(".next").addEventListener("click", () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
});

function addDeleteEventListener(e) {
    console.log(e);
    let dt = {
        "taskId": e.target.name
    }
    $.ajax({
        url: '/deleteEventAjax',
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(dt),
        success: function (data, textStatus, jQxhr) {
            let taskId = data["taskId"];
            $(`#task-div-${taskId}`).attr('hidden', true);
        },
        error: function (jqXhr, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}

function fixDate(year, month, date) {
    if (month.toString().length == 1) {
        month = "0" + month
    }
    if (date.length == 1) {
        date = "0" + date
    }
    return year + "-" + month + "-" + date
}

renderCalendar();


function currentMonthListener(e) {
    var dt = {

        "chosenDate": fixDate(date.getFullYear(), date.getMonth() + 1, e.target.outerText)
    }

    $.ajax({
        url: '/dateEventAjax',
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(dt),
        success: function (data, textStatus, jQxhr) {
            var ms = document.querySelector("#task-list-container");
            var s = ""
            s += `<h2>${fixDate(date.getFullYear(), date.getMonth() + 1, e.target.outerText)}</h2>`

            $.each(data, function (index, item) {
                s += `<div id=task-div-${item["id"]}><h4><div class="task-preview">${item["name"]} <button name="${item["id"]}" class="btn btn-sm btn-success not-delete-kappa"> &#x2713</button></div></h4></div>`;
            });

            if (!$("#add-task-form-container").prop('hidden')) {
                $("#add-task-container").removeAttr("hidden");
                $("#add-task-form-container").attr('hidden', true);
            }
            ms.innerHTML = s;
            $("#task-list-container").removeAttr('hidden');
            $("#add-task-button").removeAttr('hidden');
            window.scrollTo(0, 1000);

            document.querySelectorAll('.not-delete-kappa').forEach(btn => {

                btn.addEventListener('click', addDeleteEventListener);
            });
        },
        error: function (jqXhr, textStatus, errorThrown) {
            console.log(errorThrown);
        }

    });
    $("#add-task-button").click(() => {
        $("#add-task-container").attr('hidden', true);
        $("#add-task-form-container").removeAttr("hidden");
        window.scroll(0, 1000);
        $("#dueDate").val(fixDate(date.getFullYear(), date.getMonth() + 1, e.target.outerText));
        $('<input>').attr({
            type: 'hidden',
            name: 'selectedDate',
            value: fixDate(date.getFullYear(), date.getMonth() + 1, e.target.outerText)
        }).appendTo('#add-task-form');

    });
}