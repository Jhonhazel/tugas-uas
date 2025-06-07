const delete_card = document.getElementById('delete-card')

const id = new URLSearchParams(window.location.search).get('detail')

async function deleteCard() {
    const yes = confirm("Yakin mau di hapus?")

    if (yes) {
        try {
            const res = await fetch(`http://127.0.0.1:5555/api/payment/method/remove?id=${id}`, {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json'
                }
            });


            if (!res.ok) {
                console.log(await res.json())
                return alert('Kartu gagal di hapus')
            }

            alert('Kartu berhasil di hapus')
            window.location.replace('/profile')
            return
        } catch (error) {
            return alert(error)
        }
    } else {
        return
    }
}

delete_card.addEventListener('click', deleteCard)