const numberInput = document.getElementById('card-number');
const logo = document.getElementById('card-logo');
const cvv_cvc = document.getElementById('cvv-cvc')
const expired = document.getElementById('expired-date')
const placeholder_name = document.getElementById('placeholder-name')
const bank_name = document.getElementById('bank-name')
const tambah = document.getElementById('tambah')

const cardTypes = [
    {
        name: "visa",
        prefix: /^4/,
        lengths: [13, 16, 19]
    },
    {
        name: "mastercard",
        prefix: /^5[1-5]|^2(2[2-9]|[3-6][0-9]|7[01]|720)/,
        lengths: [16]
    },
    {
        name: "amex",
        prefix: /^3[47]/,
        lengths: [15]
    },
    {
        name: "jcb",
        prefix: /^35(2[89]|[3-8][0-9])/,
        lengths: [16, 17, 18, 19]
    },
    {
        name: "union-pay",
        prefix: /^62/,
        lengths: [16, 17, 18, 19]
    }
];

numberInput.addEventListener('input', handleCardInput);

let matchedType = null;

function handleCardInput(e) {
    // Hapus semua non-digit
    let raw = e.target.value.replace(/\D/g, '');

    // Deteksi tipe kartu
    for (const type of cardTypes) {
        if (type.prefix.test(raw)) {
            matchedType = type;
            break;
        }
    }

    // Jika ketemu, potong raw ke panjang maksimal kartu tsb
    if (matchedType) {
        const maxLength = Math.max(...matchedType.lengths);
        raw = raw.slice(0, maxLength);

        // Tampilkan logo
        logo.src = `/static/img/card/${matchedType.name}.svg`;
        logo.alt = `Logo ${matchedType.name}`;
        logo.style.display = 'inline';
    } else {
        logo.src = '';
        logo.style.display = 'none';
    }

    // Format ke XXXX XXXX XXXX
    e.target.value = formatCardNumber(raw);
}

function formatCardNumber(number) {
    // Amex 4-6-5 format
    if (/^3[47]/.test(number)) {
        return number.replace(/(\d{4})(\d{6})(\d{0,5})/, '$1 $2 $3').trim();
    }
    // Default 4-4-4-4
    return number.replace(/(.{4})/g, '$1 ').trim();
}


let realCVV = ''
cvv_cvc.addEventListener('input', (e) => {
    const inputValue = e.target.value;
    const lastChar = inputValue[inputValue.length - 1];

    // Cek apakah input angka dan tidak lebih dari 3 digit
    if (/^\d$/.test(lastChar) && realCVV.length < 3) {
        realCVV += lastChar;
    }

    // Set tampilan jadi bintang
    e.target.value = '*'.repeat(realCVV.length);
});

cvv_cvc.addEventListener('input', (e) => {
    // Tangkap karakter terakhir yang dimasukkan
    const inputValue = e.target.value;

    // Hitung panjang sebelum perubahan
    const maskedLength = realCVV.length;

    // Jika user menambahkan angka
    if (inputValue.length > maskedLength) {
        const newChar = inputValue[inputValue.length - 1];

        if (/^\d$/.test(newChar) && realCVV.length < 3) {
            realCVV += newChar;
        }
    }

    // Jika user menghapus
    else if (inputValue.length < maskedLength) {
        realCVV = realCVV.slice(0, -1);
    }

    // Update tampilan
    e.target.value = '*'.repeat(realCVV.length);
});

// Untuk menangani backspace
cvv_cvc.addEventListener('keydown', (e) => {
    if (e.key === 'Backspace') {
        e.preventDefault(); // Jangan hapus dari input (karena kita custom)
        realCVV = realCVV.slice(0, -1);
        cvv_cvc.value = '*'.repeat(realCVV.length);
    }
});

expired.addEventListener('input', (e) => {
  let value = e.target.value.replace(/\D/g, '').slice(0, 4);

  if (value.length >= 3) {
    value = value.slice(0, 2) + '/' + value.slice(2);
  }

  e.target.value = value;
});

function parseExpiredDate(expiredValue) {
    const [mm, yy] = expiredValue.split('/');
    if (!mm || !yy || mm.length !== 2 || yy.length !== 2) {
        throw new Error("Format tanggal tidak valid. Gunakan MM/YY");
    }

    const month = parseInt(mm, 10);
    const year = 2000 + parseInt(yy, 10);

    if (month < 1 || month > 12) {
        throw new Error("Bulan tidak valid");
    }

    return {
        expired_month: month,
        expired_year: year
    };
}

async function tambahKartu() {
    const { expired_month, expired_year} = parseExpiredDate(expired.value)
    const body = JSON.stringify({
        "card_number": numberInput.value,
        "bank_name": bank_name.value,
        "card_type": matchedType.name,
        expired_month,
        expired_year,
        "placeholder_name": placeholder_name.value

    })

    try {
        const res = await fetch('http://127.0.0.1:5555/api/payment/method/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body
        })

        if (!res.ok) {
            console.log(await res.json())
            return alert("Kartu tidak berhasil di tambah")
        }

        alert("kartu baru berhasil di tambah")
        window.location.replace('/pengaturan')
    } catch (error) {
        return alert(error)
    }
}

tambah.addEventListener('click', tambahKartu)