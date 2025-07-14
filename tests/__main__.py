from .mock_server import create_app

app = create_app()
app.run(port=8081, debug=False, use_reloader=False)
