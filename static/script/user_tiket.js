document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/booking/get-my-bookings")
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById("booking-list");
            list.innerHTML = "";
  
            if (!data.bookings || data.bookings.length === 0) {
                list.innerHTML = "<p class='text-gray-500'>Tidak ada tiket yang ditemukan.</p>";
                return;
            }
  
            data.bookings.forEach((booking, index) => {
                const card = document.createElement("div");
                card.className = "border border-gray-200 rounded-lg p-4 mb-4 shadow-sm";
  
                // Tampilkan data booking dalam card
                card.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div>
                            <p class="font-semibold text-gray-700">#${index + 1} - ${booking.user_id}</p>
                            <p class="text-sm text-gray-500">Event ID: ${booking.event_id}</p>
                            <p class="text-sm text-gray-500">Status Pembayaran: 
                                <span class="font-medium ${booking.payment_status.value == 'success' ? 'text-green-600' : 'text-red-600'}">
                                    ${booking.payment_status.value}
                                </span>
                            </p>
                        </div>
                        <div class="text-sm text-gray-400 text-right">
                            ${new Date(booking.createdAt).toLocaleString()}
                        </div>
                    </div>
                `;
  
                list.appendChild(card);
            });
        })
        .catch(error => {
            document.getElementById("booking-list").innerHTML = `<p class="text-red-500">Gagal memuat tiket: ${error.message}</p>`;
        });
  });
  