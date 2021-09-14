/* Set the width of the side navigation to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
    document.getElementById("mySidenav").style.boxShadow = "5px 0px 30px 50px #00000099";
}
  
/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("mySidenav").style.boxShadow = "5px 0px 30px -5px #00000099";
}

function userFilterByName() {
    // Declare and set variables
    var input, filter, i, txtValue, allAccList, userName, userCards;
    userCards = document.getElementsByClassName("user-card");
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    allAccList = document.getElementById("all-account-list");
    userName = allAccList.getElementsByClassName("user-name");

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < userName.length; i++) {
        txtValue = userName[i].textContent || userName[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            userCards[i].style.display = "";
        } else {
            userCards[i].style.display = "none";
        }
    }
}

function plantFilterByCompany() {
    // Declare and set variables
    var input, filter, i, compName, allPlantsList, plantCompany, plantCards;
    plantCards = document.getElementsByClassName("plant-card");
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    allPlantsList = document.getElementById("all-plants-list");
    plantCompany = allPlantsList.getElementsByClassName("plant-company");

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < plantCompany.length; i++) {
        compName = plantCompany[i].getElementsByTagName("img")[0].alt;
        if (compName.toUpperCase().indexOf(filter) > -1) {
            plantCards[i].style.display = "";
        } else {
            plantCards[i].style.display = "none";
        }
    }
}

function plantFilterByStatus() {
    // Declare and set variables
    var input, filter, i, allPlantsList, container;
    input = document.getElementById("mySelect");
    filter = input.value;
    allPlantsList = document.getElementById("all-plants-list");
    container = allPlantsList.getElementsByClassName("container");

    // Check if one of the options is selected
    if (filter == "plant-list-healthy" || filter == "plant-list-alert" || filter == "plant-list-danger") {
        // Loop through all list items, and hide those who don't match the search query
        for (i = 0; i < container.length; i++) {
            if (container[i].className.indexOf(filter) > -1) {
                container[i].style.display = "";
            } else {
                container[i].style.display = "none";
            }
        }
    } else {
        // If no option is selected, display all list items back again
        for (i = 0; i < container.length; i++) {
            container[i].style.display = "";
        }
    }
}

function companyFilterByName() {
    // Declare and set variables
    var input, filter, i, compName, compCard, textValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    compName = document.getElementsByClassName("company-name");
    compCard = document.getElementsByClassName("company-card");

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < compName.length; i++) {
        textValue = compName[i].textContent || compName[i].innerText;
        if (textValue.toUpperCase().indexOf(filter) > -1) {
            compCard[i].style.display = "";
        } else {
            compCard[i].style.display = "none";
        }
    }
}

function companySortByName() {
    // Declare and set variables
    var input, filter, normalList, ascendingList, descendingList;
    input = document.getElementById("mySelect");
    filter = input.value;
    normalList = document.getElementById("company-normal-list");
    ascendingList = document.getElementById("company-ascending-list");
    descendingList = document.getElementById("company-descending-list");

    // Check which option is selected and show the list accordingly
    if (filter == "a-z") {
        normalList.style.display = "none";
        ascendingList.style.display = "block";
        descendingList.style.display = "none";
    } else if (filter == "z-a") {
        normalList.style.display = "none";
        ascendingList.style.display = "none";
        descendingList.style.display = "block";
    } else {
        normalList.style.display = "block";
        ascendingList.style.display = "none";
        descendingList.style.display = "none";
    }
}

function deviceFilterByCompName() {
    // Declare and set variables
    var input, filter, i, allDevicesList, container, compName;
    input = document.getElementById("mySelect");
    filter = input.value;
    allDevicesList = document.getElementById("all-devices-list");
    container = allDevicesList.getElementsByClassName("container");

    // If default option is selected, display all list items back again
    if (filter.indexOf("default") > -1) {
        for (i = 0; i < container.length; i++) {
            container[i].style.display = "";
        }
    } else {
        // Else, loop through all list items, and hide those who don't match the search query
        for (i = 0; i < container.length; i++) {
            compName = container[i].getAttribute("data-company-name");
            if (compName.indexOf(filter) > -1) {
                container[i].style.display = "";
            } else {
                container[i].style.display = "none";
            }
        }
    }
}

// Making the file selector field on the add company page display the name of the chosen file, and makes it selected
$(".custom-file-input").on("change", function() {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});
