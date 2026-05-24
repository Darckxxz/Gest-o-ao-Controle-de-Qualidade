from src.app import create_app

# Ponto de entrada da aplicação TaskFlow
if __name__ == '__main__':
    app = create_app()
    print("TaskFlow rodando em: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
