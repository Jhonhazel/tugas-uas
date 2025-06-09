const eventForm = document.getElementById('eventForm')

function toSQLDatetime(datetimeLocalValue) {
  if (!datetimeLocalValue) return null
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

eventForm.addEventListener('submit', async function(e) {
  e.preventDefault()

  const data = {
    name: document.getElementById('name').value,
    description: document.getElementById('description').value,
    venue_address: document.getElementById('venue_address').value,
    started_at: toSQLDatetime(document.getElementById('started_at').value),
    ended_at: toSQLDatetime(document.getElementById('ended_at').value),
    price: parseFloat(document.getElementById('price').value),
    capacity: parseInt(document.getElementById('capacity').value)
  }

  try {
    const response = await fetch('/add-event', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'X-CSRFToken': getCookie('csrf_token'),  // aktifkan kalau pakai CSRF protection
      },
      body: JSON.stringify(data)
    })

    if (!response.ok) throw new Error('Gagal mengirim data')

    const result = await response.json()
    alert(result.message || 'Event berhasil ditambahkan!')

    window.location.href = '/my-events'
  } catch (error) {
    alert('Error: ' + error.message)
  }
})



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