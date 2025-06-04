
# Tiket Event

Sebuah aplikasi tugas UAS kelompok 8 PBO




## Run Locally

Clone the project

```bash
  git clone https://github.com/AlbertRT/tugas-uas.git
```

Go to the project directory

```bash
  cd tugas-uas
```

Install dependencies

```bash
  pip install
```

Start the server

```bash
  python app.py
```


## Environment Variables

To run this project, you will need to add the following environment variables to your env/env_local.py file

`DB_USER`

`DB_PASS` -> pass if don't have db password

`DB_HOST` 


## API Reference User

#### Register User

```http
  POST /api/user/create
```

| Parameter | Type     | Required                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **True** |
| `email` | `string` | **True** |
| `password` | `string` | **True** |

#### Login

```http
  POST /api/user/login
```

| Parameter | Type     | Required                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **True**|
| `password`      | `string` | **True**|

#### Logout

```http
  GET /api/user/logout
```


## API Reference Event

#### Create

```http
  POST /api/event/create
```

| Parameter | Type     | Required                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **True**|
| `description`      | `string` | **False**|
| `capacity`      | `Int` | **True**|
| `price`      | `Float` | **True**|
| `venue_address`      | `string` | **True**|
| `vendor_id`      | `string` | **True**|


#### Get all event

```http
  GET /api/event/get
```

