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
            {"icon": "layout-dashboard", "label": "Dashboard", "route": "admin_dashboard"},
            {"icon": "shopping-cart", "label": "Pesanan", "route": "pesanan"},
            {"icon": "users", "label": "Pengguna", "route": "dashboard_users"},
            {"icon": "settings", "label": "Pengaturan", "route": "pengaturan"},
        ]

    def get_main_message(self):
        return "Selamat datang di dashboard admin."

    def get_page_title(self):
        return "Dashboard Admin"


class OrganizerDashboard(Dashboard):
    def get_sidebar_items(self):
        return [
            {"icon": "layout-dashboard", "label": "Dashboard", "route": "dashboard_view"},
            {"icon": "shopping-cart", "label": "Event Saya", "route": "dashboard_view"},
            {"icon": "bar-chart-3", "label": "Laporan", "route": "dashboard_view"},
        ]

    def get_main_message(self):
        return "Halo penyelenggara! Kelola event Anda di sini."

    def get_page_title(self):
        return "Dashboard Penyelenggara"


class UserDashboard(Dashboard):
    def get_sidebar_items(self):
        return [
            {"icon": "user-circle", "label": "Profile", "route": "profile"},
            {"icon": "ticket", "label": "Tiket Saya", "route": "user_tiket"},
            {"icon": "history", "label": "Riwayat", "route": "riwayat_tiket"},
        ]

    def get_main_message(self):
        return "Selamat datang! Silakan pilih event favoritmu."

    def get_page_title(self):
        return "Dashboard Pengguna"
