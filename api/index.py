from http.server import BaseHTTPRequestHandler
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- Бронированная склейка через ASCII-коды ---
        S = chr(47)  # /
        C = chr(58)  # :
        P = "https" + C + S + S
        
        # Токен v9.2-GLOBAL
        p1 = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ODY4NWUxMzYzZTc3NjUxMDNjODA5OThmNDg0MTYwMyIsInN1YiI6IjY2MTAwYmUyZGEyOTFhMDE2MzhhYjYwNiIsInNjcCI6WyJhcGlfcmVhZCJdLCJ2ZXIiOjF9"
        p2 = "."
        p3 = "yX7-U_vNf_r9C8mI5_v2R7mN9eR0W4h8I3Y2W9L1U_8"
        token = (p1 + p2 + p3).strip().replace("\n", "").replace("\r", "")
        
        # Сборка базового URL: https://themoviedb.org
        # Используем S (/) для безопасности
        base_parts = ["api.themoviedb.org", "3"]
        tmdb_base = P + S.join(base_parts)
        
        # Очистка входящего пути (убираем /api)
        clean_path = self.path.replace(S + 'api', '')
        if not clean_path.startswith(S):
            clean_path = S + clean_path
            
        # Финальный URL для запроса
        tmdb_url = tmdb_base + clean_path

        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json;charset=utf-8",
            "User-Agent": "TMDB-Proxy-v9.2"
        }

        try:
            response = requests.get(tmdb_url, headers=headers, timeout=10)
            
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json;charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Proxy Error: {str(e)}".encode())
