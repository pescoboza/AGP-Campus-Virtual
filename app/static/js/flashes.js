const alertsTagId = "alerts";
const alertsLocalStorageKey = "alerts";

const alerts = document.getElementById(alertsTagId);

function updateAlertsLocalStorage(tagId = alertsTagId, localStorageKey = alertsLocalStorageKey) {
    const alerts = document.getElementById(tagId);
    if (alerts === undefined) {
        console.log(`[ERROR] Could not find alert widget with id '${tagId}'`);
        return;
    }
    localStorage.setItem(localStorageKey, alerts.innerHTML);
}

// Remove the alert html tag and updated local storage
function closeAlert(e) {
    e.target.parentElement.remove();
    updateAlertsLocalStorage();
}

// Updates html for flashes
function dispStoredFlashes(tagId = alertsTagId, localStorageKey = alertsLocalStorageKey) {
    document.getElementById(tagId).innerHTML = localStorage.getItem(localStorageKey);
}

// Fetches the alerts from the backend endpoint
function getAlerts(url, tagId = alertsTagId, localStorageKey = alertsLocalStorageKey) {
    // Get alerts from api
    $.ajax(url, {
        type: "post",
        success: (flashes) => {
            // Get the alerts widget from tag id
            const alertsWidget = document.getElementById(tagId);

            // Validate it exists
            if (alertsWidget === undefined) {
                console.log(`[ERROR] Could not find alert widget with id '${tagId}'`);
                return;
            }

            // Get the data from the local storage
            let flashesHTMLStr = localStorage.getItem(alertsLocalStorageKey);
            
            // If null, throw away
            if (flashesHTMLStr === null){
                flashesHTMLStr = "";
            }

            // Add any new flashes
            flashesHTMLStr += flashes;

            // Save the new flashes in the local storage
            localStorage.setItem(localStorageKey, flashesHTMLStr);

            // Change the html
            if (!!flashesHTMLStr) {
                alertsWidget.innerHTML = flashesHTMLStr;
            }

            // Add event listeners to close the alert tabs
            let closeButtons = document.getElementsByClassName("close");
            for (i = 0; i < closeButtons.length; i++) {
                closeButtons[i].addEventListener("click", closeAlert);
            }
        },
        error: (xhr, status, error) =>
            console.log(`[ERROR] Could not get flashsed messages, xhr: ${xhr}, status: ${status}, error: ${error} `),
    });
}
