import connexion, logging

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger/swagger.yaml')
application = app.app


if __name__ == '__main__':
    app.run(port=8050)
