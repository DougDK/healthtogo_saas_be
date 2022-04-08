from healthtogo.web.main import main_app

application = main_app()

if __name__ == '__main__':
    application.run(host='0.0.0.0', threaded=True)  # nosec: B104
