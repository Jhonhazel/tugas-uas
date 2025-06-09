const event_t_body = document.getElementById('event_view_tbody')

document.addEventListener('DOMContentLoaded', async () => {
    const data = await getEventData()

    if (data == []) {
        const html = `<tr>
                                <td colspan="6" class="text-center py-6 text-gray-500">Belum ada event yang ditambahkan.</td>
                            </tr>`
        event_t_body.insertAdjacentHTML('beforeend', html)
    }

    data.forEach(e => {
        const html = `<tr class="border-b hover:bg-gray-50 transition">
                    <td class="py-3 px-4">${e.name}</td>
                    <td class="py-3 px-4">${dateConverstion(e.started_at)} - ${dateConverstion(e.ended_at)}</td>
                    <td class="py-3 px-4">${formatToRupiah(e.price)}</td>
                    <td class="py-3 px-4">${e.tikets_count}</td>
                    <td class="py-3 px-4">${e.is_fullybooked ? "TIDAK TERSEDIA" : "TERSEDIA"}</td>
                    <td class="py-3 px-4">${e.venue_address}</td>
                </tr>`
        event_t_body.insertAdjacentHTML('beforeend', html)
    })
})

const getEventData = async () => {
    try {
        const {data} = await (await fetch('http://127.0.0.1:5555/api/event/get-all')).json()
        return data
    } catch (error) {
        return alert(error)
    }
}

const dateConverstion = (date) => {
    const date_time = new Date(date)
    const month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    return `${date_time.getDay()} ${month[date_time.getUTCMonth()]} ${date_time.getFullYear()}`
}

function formatToRupiah(number) {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(number)
}