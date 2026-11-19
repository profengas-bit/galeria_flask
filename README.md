# Galeria Flask

Aplicação Flask para enviar imagens, guardá-las no servidor e exibi-las em uma galeria (com opção de excluir).

## Como rodar

```bash
python -m venv venv
# Windows: venv\Scripts\activate   |   Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000

## Estrutura

```
galeria_flask/
├── app.py              ← rotas: upload, ver imagem, excluir
├── requirements.txt
├── static/uploads/     ← imagens enviadas ficam aqui
└── templates/
    ├── base.html       ← layout e mensagens
    ├── index.html      ← formulário + galeria
    └── imagem.html     ← uma imagem em tamanho grande
```

## Publicar no GitHub (checklist)

1. Crie a conta em github.com (Sign up) → plano Free.
2. Settings → Public profile: foto, nome, bio.
3. Settings → Emails: marque "Keep my email addresses private" e copie o e-mail `...@users.noreply.github.com`.
4. Settings → Password and authentication: ative o 2FA.
5. Instale o Git (git-scm.com) e configure:
   ```bash
   git config --global user.name "Seu Nome"
   git config --global user.email "seu-email-noreply"
   git config --global init.defaultBranch main
   ```
6. Conecte via SSH:
   ```bash
   ssh-keygen -t ed25519 -C "seu-email-noreply"
   # copie o conteúdo de ~/.ssh/id_ed25519.pub
   # GitHub → Settings → SSH and GPG keys → New SSH key → cole
   ssh -T git@github.com
   ```
7. No GitHub, crie o repositório vazio `galeria_flask` e, dentro desta pasta:
   ```bash
   git remote add origin git@github.com:SEU-USUARIO/galeria_flask.git
   git push -u origin main
   ```
   (Este projeto já vem com `git init` e o primeiro commit feitos.)
