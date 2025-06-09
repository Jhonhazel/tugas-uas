const first_name = document.getElementById('first_name')
const last_name = document.getElementById('last_name')
const phone = document.getElementById('phone')
const email = document.getElementById('email')
const address = document.getElementById('address')
const gov_id = document.getElementById('gov_id')
const book = document.getElementById('book')

const path = window.location.pathname; // "/event/book/CFqYpURV0aeK"
const parts = path.split("/");          // ["", "event", "book", "CFqYpURV0aeK"]
const event_id = parts[2];

const createBooking = async () => {
    const body = JSON.stringify({
        event_id,
        first_name: first_name.value,
        last_name: last_name.value,
        phone: phone.value,
        email: email.value,
        address: address.value,
        gov_id: gov_id.value
    })

    try {
        const res = await (await fetch('http://127.0.0.1:5555/api/booking/create', {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body
        })).json()

        if (!res.booking_id) {
            return alert(res.msg)
        }

        window.location.replace(`/event/pay/${res.event_id}/${res.booking_id}`)
    } catch (error) {
        return alert(error)
    }
}

book.addEventListener('click', createBooking)