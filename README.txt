1. Suba esse projeto no GitHub.
2. No Render.com, escolha "Novo serviço Web".
3. Configure as variáveis de ambiente:
   - BOT_TOKEN = o token do seu bot
   - API_URL = URL pública que o Render gerar (ex: https://painelbot.onrender.com)
4. Configure o start command como:
   gunicorn main:app & python3 bot.py