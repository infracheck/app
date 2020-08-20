from infracheck import app

if __name__ == '__main__':
    app.run(port=9999)
    del app
    print(app)
