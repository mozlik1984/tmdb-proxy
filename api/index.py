from http.server import BaseHTTPRequestHandler
import requests
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- Вшитый токен (v9.3-FINAL) ---
        TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ODY4NWUxMzYzZTc3NjUxMDNjODA5OThmNDg0MTYwMyIsInN1YiI6IjY2MTAwYmUyZGEyOTFhMDE2MzhhYjYwNiIsInNjcCI6WyJhcGlfcmVhZCJdLCJ2ZXIiOjF9.yX7-U_vNf_r9C8mI5_v2R7mN9eR0W4h8I3Y2W9L1U_8"
        
        # 1. Очищаем путь от префикса /api, который добавляет Vercel
        path = self.path.replace('/api', '')
        
        # 2. Если путь пустой, по умолчанию запрашиваем Бойцовский клуб (ID: 550) для теста
        if not path or path == "/":
            target_url = "https://themoviedb.org"
        else:
            # Иначе пробрасываем запрос как есть к API v3
            target_url = f"https://themoviedb.org{path}"

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json;charset=utf-8"
        }

        try:
            # Делаем запрос к TMDB
            response = requests.get(target_url, headers=headers)
            
            # Отправляем ответ клиенту
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*') # Для работы с любыми доменами
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            error_msg = {"error": "Proxy Error", "details": str(e)}
            self.wfile.write(json.dumps(error_msg).encode())
