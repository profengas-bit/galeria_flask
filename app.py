import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ---------------- Configurações ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # limite de 5 MB por arquivo
app.secret_key = os.environ.get("SECRET_KEY", "troque-esta-chave")  # usada pelas mensagens flash

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "webp"}

# Garante que a pasta de uploads existe
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def arquivo_permitido(nome):
    """Confere se o arquivo tem uma extensão de imagem aceita."""
    return "." in nome and nome.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS


def listar_imagens():
    """Lista só as imagens da pasta de uploads (ignora .gitkeep etc.)."""
    return sorted(f for f in os.listdir(app.config["UPLOAD_FOLDER"]) if arquivo_permitido(f))


# ---------------- Rotas ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 1. O campo "imagem" veio no formulário?
        if "imagem" not in request.files:
            flash("Nenhum arquivo enviado.", "erro")
            return redirect(request.url)

        arquivo = request.files["imagem"]

        # 2. O usuário escolheu um arquivo?
        if arquivo.filename == "":
            flash("Nenhum arquivo selecionado.", "erro")
            return redirect(request.url)

        # 3. Extensão válida? Então salva no servidor.
        if arquivo_permitido(arquivo.filename):
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            flash("Imagem enviada com sucesso!", "ok")
            return redirect(url_for("ver_imagem", nome=nome_seguro))

        flash("Tipo de arquivo não permitido. Use PNG, JPG, GIF ou WEBP.", "erro")
        return redirect(request.url)

    # GET: mostra o formulário e a galeria
    return render_template("index.html", imagens=listar_imagens())


@app.route("/imagem/<nome>")
def ver_imagem(nome):
    nome = secure_filename(nome)
    if not os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], nome)):
        abort(404)
    return render_template("imagem.html", nome=nome)


@app.route("/excluir/<nome>", methods=["POST"])
def excluir_imagem(nome):
    nome = secure_filename(nome)
    caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome)
    if os.path.exists(caminho) and arquivo_permitido(nome):
        os.remove(caminho)
        flash(f"Imagem '{nome}' excluída.", "ok")
    else:
        flash("Imagem não encontrada.", "erro")
    return redirect(url_for("index"))


@app.errorhandler(413)
def arquivo_grande(_erro):
    flash("Arquivo grande demais (máximo 5 MB).", "erro")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
