from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Используем тройные кавычки для многострочного текста
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Мой DevOps Проект</title>
    </head>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #282c34; color: white; text-align: center; padding-top: 100px;">
        
        <h1 style="font-size: 60px; color: #61dafb;">
            восьмой тест с добавлением текста
        </h1>
        
        <p style="font-size: 20px;">
            Микросервис успешно развернут в кластере через Jenkins CI/CD!
        </p>
        
        <p style="font-size: 14px; color: #98c379; font-style: italic;">
            Теперь мы умеем менять дизайн, шрифты и цвета напрямую из кода.
        </p>
        
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
