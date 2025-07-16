from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

DATABASE = "data.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (telegram_id TEXT PRIMARY KEY, saldo REAL DEFAULT 0, giros INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS keys (key TEXT PRIMARY KEY, dias INTEGER, usada INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return "Painel ativo. Bot online."

@app.route("/login", methods=["POST"])
def login():
    telegram_id = request.json.get("telegram_id")
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT saldo, giros FROM users WHERE telegram_id = ?", (telegram_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"saldo": user[0], "giros": user[1]})
    else:
        return jsonify({"erro": "Usuário não encontrado"}), 404

@app.route("/ativar_key", methods=["POST"])
def ativar_key():
    telegram_id = request.json.get("telegram_id")
    key = request.json.get("key")
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT dias, usada FROM keys WHERE key = ?", (key,))
    result = c.fetchone()
    if not result:
        return jsonify({"erro": "Key inválida"}), 404
    dias, usada = result
    if usada:
        return jsonify({"erro": "Key já usada"}), 400
    c.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))
    c.execute("UPDATE users SET saldo = saldo + ?, giros = giros + 1 WHERE telegram_id = ?", (dias, telegram_id))
    c.execute("UPDATE keys SET usada = 1 WHERE key = ?", (key,))
    conn.commit()
    conn.close()
    return jsonify({"status": "Key ativada com sucesso!"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))