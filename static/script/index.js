document.addEventListener('DOMContentLoaded', async function () {
    const dropdownButton = document.getElementById('profileDropdownButton');
    const dropdownMenu = document.getElementById('profileDropdownMenu');

    if (dropdownButton && dropdownMenu) {
        dropdownButton.addEventListener('click', function (e) {
            e.stopPropagation(); // Mencegah event click bubbling ke body
            dropdownMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function (e) {
            if (!dropdownMenu.contains(e.target) && !dropdownButton.contains(e.target)) {
                dropdownMenu.classList.add('hidden');
            }
        });
    }

    const event_container = document.getElementById('event-container')
    const event_data = await getAllEvent()
    event_data.forEach((data, index) => {
        const imageIndex = 4802 + index;
        const imageSrc = `/static/img/events/IMG_${imageIndex}.jpg`;
        const html = `<div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl hover:-translate-y-2 transition duration-300">
                  <div class="relative">
                      <img
                          src="${imageSrc}"
                          alt="Event Image"
                          class="w-full h-48 object-cover"
                      >
                      <div class="absolute top-4 left-4">
                          <span class="bg-primary text-white px-3 py-1 rounded-full text-sm font-medium">${dateConverstion(data.started_at)}</span>
                      </div>
                  </div>
                  <div class="p-6">
                      <h3 class="text-lg font-semibold text-gray-900 mb-2">${data.name}</h3>
                      <p class="text-gray-600 mb-4 flex items-center">
                          <i class="bi bi-geo-alt mr-2"></i>
                          ${data.venue_address}
                      </p>
                      <div class="flex justify-between items-center">
                          <span class="text-xl font-bold text-primary">${formatToRupiah(data.price)}</span>
                          <a
                              href="/event/detail/${data.id}?img=${imageIndex}""
                              class="bg-primary text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition duration-300"
                          >
                              Lihat Detail
                          </a>
                      </div>
                  </div>
              </div>`

        event_container.insertAdjacentHTML('beforeend', html)
    })


});

const getAllEvent = async () => {
    try {
        const {data} = await (await fetch('http://127.0.0.1:5555/api/event/get-all')).json()
        return data
    } catch (e) {
        console.log(e)
        return e
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
