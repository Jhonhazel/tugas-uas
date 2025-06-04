class Dashboard:
    def __init__(self, user):
        self._user = user

    def get_sidebar_items(self):
        return []

    def get_main_message(self):
        return "Konten dashboard default."

    def get_page_title(self):
        return "Dashboard"


class AdminDashboard(Dashboard):
    def get_sidebar_items(self):
        return [
            {"icon": "layout-dashboard", "label": "Dashboard"},
            {"icon": "shopping-cart", "label": "Pesanan"},
            {"icon": "users", "label": "Pengguna"},
            {"icon": "settings", "label": "Pengaturan"},
        ]

    def get_main_message(self):
        return "Selamat datang di dashboard admin."

    def get_page_title(self):
        return "Dashboard Admin"


class OrganizerDashboard(Dashboard):
    def get_sidebar_items(self):
        return [
            {"icon": "layout-dashboard", "label": "Dashboard"},
            {"icon": "shopping-cart", "label": "Event Saya"},
            {"icon": "bar-chart-3", "label": "Laporan"},
        ]

    def get_main_message(self):
        return "Halo penyelenggara! Kelola event Anda di sini."

    def get_page_title(self):
        return "Dashboard Penyelenggara"


class UserDashboard(Dashboard):
    def get_sidebar_items(self):
        return [
            {"icon": "user-circle", "label": "Profile", "route": "profile"},
            {"icon": "shopping-cart", "label": "Tiket Saya", "route": "user_tiket"},
            {"icon": "bar-chart-3", "label": "Riwayat", "route": "dashboard_view"},
        ]

    def get_main_message(self):
        return "Selamat datang! Silakan pilih event favoritmu."

    def get_page_title(self):
        return "Dashboard Pengguna"
