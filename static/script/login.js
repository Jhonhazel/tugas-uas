const username = document.getElementById("username")
const password = document.getElementById("password")
const loginBtn = document.getElementById("login")

loginBtn.addEventListener("click", async () => {
    if (!username.value || !password.value) {
        return alert("Data tidak lengkap!")
    }

    const body = JSON.stringify({
        username: username.value,
        password: password.value
    })

    try {
        const res = await fetch("http://127.0.0.1:5555/api/user/login", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body
        })

        if (!res.ok) {
            console.log(await res.json())
            return alert("Terjadi kesalahan saat login!")
        }
        const {data} = await res.json()

        if (data.role === "user") {
            window.location.replace("/")
        } else {
            window.location.replace('/admin/dashboard')
        }

    } catch (error) {
        console.log(error)
    }
})