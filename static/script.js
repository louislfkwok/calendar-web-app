const WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

document.querySelectorAll('.task-button-primary').forEach(function(button) {
    var timeoutId;

    button.addEventListener('mouseenter', function(event) {
        const id = event.target.id.split('-')[1];
        const overlayId = 'task-' + id + '-primary-overlay';
        const overlay = document.getElementById(overlayId);

        timeoutId = setTimeout(function() {
            overlay.style.display = 'flex';
        }, 500);
    });

    button.addEventListener('mouseleave', function() {
        clearTimeout(timeoutId);
    });
});

document.querySelectorAll('.task-primary-overlay').forEach(function(overlay) {
    overlay.addEventListener('mouseleave', function(event) {
        event.target.style.display = 'none';
    });
});

document.querySelectorAll('.task-button-edit').forEach(function(button) {
    button.addEventListener('click', function(event) {
        const id = event.target.id.split('-')[1];
        const overlayId = 'task-' + id + '-secondary-overlay';
        const overlay = document.getElementById(overlayId);
        overlay.style.display = 'flex';

        const input = overlay.querySelector('.task-input-edit');
        input.focus();
    });
});

var modal = document.getElementById("modal");

document.querySelector('.slots-grid').addEventListener('click', function(event) {
    const modalForm = document.querySelector('.event-form');
    var addEvent = false;

    if (event.target.classList.contains('events')) {
        const eventId = event.target.id.split('-')[1];
        const eventName = event.target.innerText;
        const eventData = event.target.querySelector('.event-data').textContent;
        const [eventWeekday, eventStartTime, eventEndTime] = eventData.split('-');

        document.querySelector('.modal-title').textContent = 'Edit Event';

        modalForm.querySelector('.event-id').value = parseInt(eventId);
        modalForm.querySelector('.event-name').value = eventName;
        modalForm.querySelector('.event-weekday-select').value = eventWeekday;
        modalForm.querySelector('.event-start-time-select').value = eventStartTime;
        modalForm.querySelector('.event-end-time-select').value = eventEndTime;
        modalForm.querySelector('.event-add').style.display = 'none';
        modalForm.querySelector('.event-edit').style.display = 'block';
        modalForm.querySelector('.event-delete').style.display = 'block';
    }

    if (event.target.classList.contains('slots-gridbox')) {
        addEvent = true;

        const slotId = event.target.id.split('-')[1];
        const slotIndex = parseInt(slotId);
        const slotName = '';
        const slotWeekday = WEEKDAYS[Math.floor((slotIndex - 1) / 24)];
        var slotStartHour = ((slotIndex - 1) % 24).toString();
        if (slotStartHour.length < 2) {
            slotStartHour = "0" + slotStartHour;
        }
        var slotEndHour = ((slotIndex - 1) % 24 + 1).toString();
        if (slotEndHour.length < 2) {
            slotEndHour = "0" + slotEndHour;
        }

        const slotStartTime = slotStartHour + ":00";
        const slotEndTime = slotEndHour + ":00";

        document.querySelector('.modal-title').textContent = 'Add Event';

        modalForm.querySelector('.event-id').value = 0;
        modalForm.querySelector('.event-name').value = slotName;
        modalForm.querySelector('.event-weekday-select').value = slotWeekday;
        modalForm.querySelector('.event-start-time-select').value = slotStartTime;
        modalForm.querySelector('.event-end-time-select').value = slotEndTime;
        modalForm.querySelector('.event-add').style.display = 'block';
        modalForm.querySelector('.event-edit').style.display = 'none';
        modalForm.querySelector('.event-delete').style.display = 'none';
    }

    modal.style.display = 'block';
    if (addEvent) {
        modalForm.querySelector('.event-name').focus();
    }
});

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}