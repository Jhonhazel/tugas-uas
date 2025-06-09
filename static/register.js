const username = document.getElementById("username")
const email = document.getElementById("email")
const password = document.getElementById("password")
const confirm_password = document.getElementById("confirm_password")

const daftar = document.getElementById("register")
daftar.addEventListener("click", async (e) => {
    e.preventDefault()
    if (!username.value || !email.value || !password.value || !confirm_password.value) {
        return alert("Data tidak lengkap!")
    }

    if (password.value !== confirm_password.value) {
       return alert("Password tidak sama!")
    }

    const body = JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value
    })

    try {
        const res = await fetch("http://127.0.0.1:5555/api/user/create", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body
        })

        console.log(body)

        if (!res.ok) {
            console.log(res)
            return alert("Terjadi kesalahan! harap coba lagi")
        }

        alert("User berhasil terdaftar, silakan login")

    } catch (error) {
        alert(`error: ${error}`)
    }
})