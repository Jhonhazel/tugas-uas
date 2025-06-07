const event_name = document.getElementById('name')
const event_description = document.getElementById('description')
const started_at = document.getElementById('started_at')
const ended_at = document.getElementById('ended_at')
const price = document.getElementById('price')
const capacity = document.getElementById('capacity')
const venue_address = document.getElementById('venue_address')
const create_event = document.getElementById('create')

function toSQLDatetime(datetimeLocalValue) {
  const date = new Date(datetimeLocalValue)
  const pad = n => n.toString().padStart(2, '0')

  const year = date.getFullYear()
  const month = pad(date.getMonth() + 1)
  const day = pad(date.getDate())
  const hours = pad(date.getHours())
  const minutes = pad(date.getMinutes())
  const seconds = pad(date.getSeconds())

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}


const create = async () => {
    const body = JSON.stringify({
        name: event_name.value,
        description: event_description.value,
        capacity: capacity.value,
        price: price.value,
        started_at: toSQLDatetime(started_at.value),
        ended_at: toSQLDatetime(ended_at.value),
        venue_address: venue_address.value
    })

    try {
        const res = await fetch('http://127.0.0.1:5555/api/event/create', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body
        })

        if (!res.ok) {
            console.log(await res.json())
            return alert('Gagal dalam membuat event')
        } else {
            alert('Event baru berhasil dibuat')
            window.location.replace('/event_saya')
        }
    } catch (error) {
        console.log(error)
        return alert(error)
    }
}

create_event.addEventListener('click', create)