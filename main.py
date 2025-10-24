# Tela principal do PDV
from modules import db, login

if __name__ == "__main__":
    db.criar_tabelas()
    app = login.TelaLogin()
    app.mainloop()
