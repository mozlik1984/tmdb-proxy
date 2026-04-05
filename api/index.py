from http.server import BaseHTTPRequestHandler
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- Бронированная склейка токена (v9.2-GLOBAL) ---
        p1 = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ODY4NWUxMzYzZTc3NjUxMDNjODA5OThmNDg0MTYwMyIsInN1YiI6IjY2MTAwYmUyZGEyOTFhMDE2MzhhYjYwNiIsInNjcCI6WyJhcGlfcmVhZCJdLCJ2ZXIiOjF9"
        p2 = "."
        p3 = "yX7-U_vNf_r9C8mI5_v2R7mN9eR0W4h8I3Y2W9L1U_8"
        
        # Склеиваем и жестко вычищаем пробелы и переносы строк
        token = (p1 + p2 + p3).strip().replace("\n", "").replace("\r", "")
        
        # Формируем путь (убираем /api, оставляем остальное как есть)
        clean_path = self.path.replace('/api', '')
        # Оставляем язык по умолчанию (English) или как придет в запросе
        tmdb_url = f"https://themoviedb.org{clean_path}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json;charset=utf-8"
        }

        try:
            # Проксируем запрос на серверы TMDB (в США/Европе)
            response = requests.get(tmdb_url, headers=headers)
            
            # Отдаем результат боту на Amvera
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # Разрешаем CORS
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Proxy Error: {str(e)}".encode())
