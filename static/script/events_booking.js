const countdownElement = document.getElementById('countdown-timer');
let remainingSeconds = 60 * 60; // 60 menit × 60 detik

function updateCountdown() {
    const minutes = Math.floor(remainingSeconds / 60);
    const seconds = remainingSeconds % 60;

    // Format dua digit
    const formatted = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    countdownElement.textContent = `Harap melakukan pembayaran dalam: ${formatted}`;

    if (remainingSeconds > 0) {
        remainingSeconds--;
    } else {
        clearInterval(timer);
        countdownElement.textContent = "⏳ Waktu habis!";
    }
}

// Jalankan countdown tiap detik
updateCountdown(); // tampilkan pertama kali langsung
const timer = setInterval(updateCountdown, 1000);


// url params
const path = window.location.pathname;
const parts = path.split("/");


const payBooking = async () => {
    const payment_method_selector = document.querySelector('input[name="payment_method"]:checked');
    const booking_id = parts[4]
    let payment_method_id = ''

    if (payment_method_selector) {
        payment_method_id = payment_method_selector.value
    }

    const body = JSON.stringify({
        booking_id,
        payment_method_id
    })

    try {
        const payment_res = await fetch('http://127.0.0.1:5555/api/payment/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body
        })

        if (!payment_res.ok) {
            console.log(await payment_res.json())
            return alert('Tejadi kesalahan')
        }

        if (payment_res.ok) {
            const pay_res = await payment_res.json()
            const pay_booking_res = await fetch('http://127.0.0.1:5555/api/booking/payment/pay', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    payment_id: pay_res.payment_id,
                    booking_id
                })
            })

            if (!pay_booking_res.ok) {
                window.location.replace(`/payment-failed`)
            }

            window.location.replace(`/payment-success/${pay_res.payment_id}`)
        }


    } catch (error) {
        return alert(error)
    }
}

pay.addEventListener('click', payBooking)