import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', user='root', password='', database='crud')
        self.cursor = self.conn.cursor()

    def create(self, nome, cpf, telefone, email):
        try:
            self.cursor.execute("INSERT INTO usuario (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)", (nome, cpf, telefone, email))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao criar registro: {e}")
            self.conn.rollback()

    def read(self):
        try:
            self.cursor.execute("SELECT * FROM usuario")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao ler registros: {e}")

    def update(self, id, nome, cpf, telefone, email):
        try:
            self.cursor.execute("UPDATE usuario SET nome = %s, cpf = %s, telefone = %s, email = %s WHERE id = %s", (nome, cpf, telefone, email, id))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar registro: {e}")
            self.conn.rollback()

    def delete(self, id):
        try:
            self.cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao excluir registro: {e}")
            self.conn.rollback()

if __name__ == "__main__":
    db = Database()
    db.create("João", "12345678901", "1234567890", "joao@email.com")
    data = db.read()
    print(data)
    db.update(1, "João Silva", "98765432109", "9876543210", "joao.silva@email.com")
    data = db.read()
    print(data)
    db.delete(1)
    data = db.read()
    print(data)
