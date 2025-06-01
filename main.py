# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

#настройки запуска
hostName = "localhost" # Адрес для доступа по сети
serverPort = 2020 # Порт для доступа по сети

class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        requested_path = self.path  # Получаем запрошенный путь (например, "/", "/main", "/contacts")

        # Отладочный вывод: посмотрим, что запросил браузер
        print(f"DEBUG: Браузер запросил путь: '{requested_path}'")

        if requested_path == "/":
            filename_to_serve = "main.html"
        elif requested_path == "/main":
            filename_to_serve = "main.html"
        elif requested_path == "/contacts":
            filename_to_serve = "contacts.html"
        elif requested_path == "/category":
            filename_to_serve = "category.html"
        elif requested_path == "/catalog":
            filename_to_serve = "catalog.html"
        else:
            # Если запрошенный путь не соответствует ни одному из известных
            print(f"DEBUG: Запрошенный путь '{requested_path}' не соответствует ни одному правилу. Возвращаем 404.")
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                bytes("<h1>404 Not Found</h1><p>Страница не найдена или не обрабатывается сервером.</p>", "utf-8"))
            return
        # Отладочный вывод: какой файл сервер пытается открыть
        print(f"DEBUG: Сервер пытается открыть файл: '{filename_to_serve}'")

        # Проверяем, существует ли файл перед попыткой его открыть
        if not os.path.exists(filename_to_serve):
            print(
                f"DEBUG: Файл '{filename_to_serve}' НЕ СУЩЕСТВУЕТ по абсолютному пути: '{os.path.abspath(filename_to_serve)}'")
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                bytes(f"<h1>404 Not Found</h1><p>Файл '{filename_to_serve}' не найден на сервере.</p>", "utf-8"))
            return

        try:
            # Открываем и читаем содержимое файла
            with open(filename_to_serve, "r", encoding="utf-8") as file:
                data = file.read()

            # Отправляем успешный ответ
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")  # Обязательно указывайте charset
            self.end_headers()
            self.wfile.write(bytes(data, "utf-8"))

        except Exception as e:
            # Обработка других возможных ошибок при чтении файла
            print(f"DEBUG: Произошла ошибка при чтении файла {filename_to_serve}: {e}")
            self.send_response(500)  # Код 500 Internal Server Error
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes(f"<h1>500 Internal Server Error</h1><p>Ошибка сервера: {e}</p>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass  # Корректная остановка сервера по Ctrl+C

    webServer.server_close()
    print("Server stopped.")