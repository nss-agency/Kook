function setModalRoomDescription(room_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("form-modal-room-type").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "/ajax_description/" + room_id, true);
    xhttp.send();
}

function getRoomTypeMap() {
    let room_select = document.querySelector('#id_room_type');
    let choices = room_select.options;
    let result = {}
    for (let i = 0; i < choices.length; ++i) {
        result[choices[i].value] = choices[i].index
    }

    return result
}

function submitForm() {
    document.querySelector('#form-body').submit()
}

function modalShowNextStep() {
    document.querySelector('#form-modal').classList.add('form-modal-inactive')
    document.querySelector('#form-confirmation').classList.remove('confirmation-inactive')
    let date_start = document.querySelector('#id_date_entry').value
    let date_end = document.querySelector('#id_date_leave').value
    let select = document.querySelector('#id_room_type')
    let id = parseInt(select[select.selectedIndex].value)
    let email = document.querySelector('#id_email').value
    let promo = document.querySelector('#id_discount').value


    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("form-confirmation").innerHTML = this.responseText;
            document.getElementById('payment_button').addEventListener('click', submitForm)
        }
    };
    xhttp.open("GET", `/ajax_second_step?date_start=${date_start}&date_end=${date_end}&id=${id}&email=${email}&promo=${promo}`, true);
    xhttp.send();
}

function showModal(room_id) {
    document.querySelector('#form-modal').classList.remove('form-modal-inactive')
    document.querySelector('#form-confirmation').classList.add('confirmation-inactive')
    let modal = document.querySelector('#form-modal-wrapper');
    modal.classList.remove('modal-inactive');
    let room_type_select = document.querySelector('#id_room_type');
    room_type_select.selectedIndex = getRoomTypeMap()[room_id];
    setModalRoomDescription(room_id)
    let ids_require_bed_type = [1,2]
    if (ids_require_bed_type.indexOf(room_id) >= 0)
        document.querySelector('#id_bed_type').hidden = false
    else {
        document.querySelector('#id_bed_type').hidden = true
    }
}

function hideModal() {
    let modal = document.querySelector('#form-modal-wrapper');
    modal.classList.add('modal-inactive')
}

function backgroundModalClick(e) {
    if (e.target === this) {
        hideModal()
    }
}

function formNextStep(e) {
    e.preventDefault()
    let form = document.querySelector('#form-body')
    if (form.checkValidity()) {
        modalShowNextStep()
    } else {
        form.reportValidity()
    }
}

function checkRoomAvailability() {
    let date_start = document.querySelector('#id_date_entry').value
    let date_end = document.querySelector('#id_date_leave').value
    let id = document.querySelector('#id_room_type').value

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText === 'True') {
                document.querySelector('#room_availability').innerHTML = ''
            } else {
                document.querySelector('#room_availability').innerHTML = 'this room is not available at this date'
            }
        }
    };
    xhttp.open("GET", `/room_availability_check/${id}/${date_start}/${date_end}/`, true);
    xhttp.send();
}

document.getElementById('form-modal-wrapper').addEventListener('click', backgroundModalClick)
document.getElementById('submitContactForm').addEventListener('click', formNextStep)


document.querySelector('#id_date_entry').min = new Date().toISOString().split("T")[0];
document.querySelector('#id_date_leave').min = new Date().toISOString().split("T")[0];

document.querySelector('#id_date_entry').addEventListener('change', () => {
        document.querySelector('#id_date_leave').min = new Date(document.querySelector('#id_date_entry').value).toISOString().split("T")[0];
        checkRoomAvailability()
    }
)
document.querySelector('#id_date_leave').addEventListener('change', () => {
        checkRoomAvailability()
    }
)
