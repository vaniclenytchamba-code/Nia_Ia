
import os
import json
import threading
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup


# =====================================
# CONFIGURACAO DA NIA
# =====================================

PASTA = "/storage/emulated/0/Download"

CAMINHO_FUNDO = os.path.join(PASTA, "fundo.png")
CAMINHO_NIA = os.path.join(PASTA, "nia.png")
CAMINHO_MEMORIA = os.path.join(PASTA, "nia_memoria.json")

# Coloca aqui a tua chave valida do OpenRouter.
API_KEY = "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"

URL_API = "https://openrouter.ai/api/v1/chat/completions"
MODELO = "openrouter/free"

LARANJA = (0.95, 0.39, 0.08, 1)
FUNDO = (0.035, 0.045, 0.085, 1)
CARTAO = (0.10, 0.12, 0.18, 1)
BRANCO = (0.96, 0.97, 1, 1)
CINZENTO = (0.67, 0.70, 0.77, 1)

Window.clearcolor = FUNDO
Window.softinput_mode = "pan"


# =====================================
# PERSONALIDADE DA NIA
# =====================================

INSTRUCOES = """
Tu es a Nia, uma inteligencia artificial conversacional.

Responde de forma natural, clara, amigavel e util,
preferencialmente em portugues europeu.

O teu criador chama-se Zeferino Tomás,
mais conhecido como Wizkhay ou Wizkei.

O filho do teu criador chama-se Ebenesis.
Segundo as informacoes fornecidas, nasceu em
1 de abril de 2025.

Nia significa Nambalo, Inteligencia Artificial.

O meu criador nasceu em 14 de fevereiro de 2003.

O nome da mae de Ebenesis e Isabel
Catarina Candogo Sapalalo,
mas chamam-lhe Isa.

o meu criador sabe falar inglês, e domina.
informática, como ajustar dispositivos,
criar aplicativos com python kivy, pygame,
sabe criar também inteligencia artificial,
projectos de alta qualidade.

Ela e descrita pelo criador como uma boa pessoa,
agradavel e corajosa.

Ela gosta de cantar e ouvir musica.

Nao inventes informacoes pessoais.
Para perguntas gerais, responde normalmente.
Mantem o contexto da conversa.
"""


def mensagens_iniciais():
    return [{
        "role": "system",
        "content": INSTRUCOES
    }]


# =====================================
# BOTOES ARREDONDADOS
# =====================================

class BotaoNia(Button):

    def __init__(self, cor=LARANJA, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = BRANCO
        self.bold = True

        with self.canvas.before:
            self.cor_fundo = Color(*cor)
            self.forma = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(13)]
            )

        self.bind(
            pos=self.atualizar,
            size=self.atualizar
        )

    def atualizar(self, *args):
        self.forma.pos = self.pos
        self.forma.size = self.size


# =====================================
# BALOES DE CONVERSA COM COPIAR
# =====================================

class Balao(BoxLayout):

    def __init__(self, texto, utilizador=False, **kwargs):

        self.texto_original = str(texto)

        super().__init__(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(80),
            padding=[dp(13), dp(10), dp(13), dp(10)],
            spacing=dp(5),
            **kwargs
        )

        if utilizador:
            cor = (0.78, 0.29, 0.07, 1)
            nome = "Tu"
        else:
            cor = (0.105, 0.125, 0.19, 1)
            nome = "Nia"

        with self.canvas.before:
            Color(*cor)
            self.forma = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

        self.bind(
            pos=self.atualizar,
            size=self.atualizar,
            minimum_height=self.setter("height")
        )

        self.titulo = Label(
            text=nome,
            color=BRANCO if utilizador else (1, 0.72, 0.42, 1),
            bold=True,
            font_size="12sp",
            size_hint=(1, None),
            height=dp(20),
            halign="left",
            valign="middle"
        )

        self.titulo.bind(
            size=self.atualizar_titulo
        )

        self.corpo = Label(
            text=self.texto_original,
            color=BRANCO,
            font_size="15sp",
            size_hint=(1, None),
            height=dp(24),
            halign="left",
            valign="top"
        )

        self.corpo.bind(
            width=self.atualizar_largura_texto,
            texture_size=self.atualizar_altura_texto
        )

        self.botao_copiar = Button(
            text="Copiar",
            size_hint=(None, None),
            size=(dp(80), dp(30)),
            font_size="12sp",
            color=(1, 0.72, 0.42, 1),
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        self.botao_copiar.bind(
            on_release=self.copiar_texto
        )

        self.add_widget(self.titulo)
        self.add_widget(self.corpo)

        linha_copiar = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(30)
        )

        linha_copiar.add_widget(BoxLayout())
        linha_copiar.add_widget(self.botao_copiar)

        self.add_widget(linha_copiar)

        Clock.schedule_once(self.preparar_texto, 0)
        Clock.schedule_once(self.preparar_texto, 0.1)

    def atualizar(self, *args):
        self.forma.pos = self.pos
        self.forma.size = self.size

    def atualizar_titulo(self, instancia, tamanho):
        instancia.text_size = tamanho

    def atualizar_largura_texto(self, instancia, largura):
        instancia.text_size = (max(1, largura), None)

    def atualizar_altura_texto(self, instancia, tamanho):
        instancia.height = max(
            dp(24),
            tamanho[1] + dp(4)
        )

    def preparar_texto(self, *args):
        self.corpo.text_size = (
            max(1, self.corpo.width),
            None
        )

        self.corpo.texture_update()

        self.corpo.height = max(
            dp(24),
            self.corpo.texture_size[1] + dp(4)
        )

    def copiar_texto(self, *args):
        try:
            Clipboard.copy(self.texto_original)
            self.botao_copiar.text = "Copiado!"

            Clock.schedule_once(
                self.restaurar_botao_copiar,
                2
            )

        except Exception as erro:
            print("Erro ao copiar:", erro)
            self.botao_copiar.text = "Erro"

    def restaurar_botao_copiar(self, *args):
        self.botao_copiar.text = "Copiar"


# =====================================
# APLICACAO PRINCIPAL
# =====================================

class NiaApp(App):

    def build(self):

        self.title = "Nia IA"

        self.mensagens = self.carregar_memoria()
        self.a_processar = False
        self.boas_vindas_visiveis = True

        self.raiz = FloatLayout()

        # Fundo da aplicacao
        if os.path.exists(CAMINHO_FUNDO):

            self.imagem_fundo = Image(
                source=CAMINHO_FUNDO,
                allow_stretch=True,
                keep_ratio=False,
                opacity=0.42,
                size_hint=(1, 1),
                pos_hint={"x": 0, "y": 0}
            )

            self.raiz.add_widget(self.imagem_fundo)

        # Camada escura
        self.principal = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=[dp(12), dp(8), dp(12), dp(10)],
            size_hint=(1, 1)
        )

        with self.principal.canvas.before:
            Color(0.025, 0.035, 0.07, 0.80)

            self.fundo_principal = Rectangle(
                pos=self.principal.pos,
                size=self.principal.size
            )

        self.principal.bind(
            pos=self.atualizar_fundo,
            size=self.atualizar_fundo
        )

        self.raiz.add_widget(self.principal)

        self.criar_cabecalho()
        self.criar_boas_vindas()
        self.criar_conversa()
        self.criar_caixa_mensagem()

        self.restaurar_historico()

        return self.raiz

    # =================================
    # CABECALHO
    # =================================

    def criar_cabecalho(self):

        cabecalho = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(65),
            spacing=dp(10)
        )

        if os.path.exists(CAMINHO_NIA):

            avatar = Image(
                source=CAMINHO_NIA,
                size_hint=(None, None),
                size=(dp(51), dp(51)),
                allow_stretch=True,
                keep_ratio=False
            )

            cabecalho.add_widget(avatar)

        informacao = BoxLayout(
            orientation="vertical",
            spacing=dp(1)
        )

        nome = Label(
            text="[b]Nia[/b]",
            markup=True,
            color=BRANCO,
            font_size="23sp",
            halign="left",
            valign="middle",
            size_hint_y=0.58
        )

        nome.bind(
            size=lambda obj, valor:
            setattr(obj, "text_size", valor)
        )

        estado = Label(
            text="[color=36D98A]●[/color] Pronta para conversar",
            markup=True,
            color=CINZENTO,
            font_size="12sp",
            halign="left",
            valign="middle",
            size_hint_y=0.42
        )

        estado.bind(
            size=lambda obj, valor:
            setattr(obj, "text_size", valor)
        )

        informacao.add_widget(nome)
        informacao.add_widget(estado)
        cabecalho.add_widget(informacao)

        menu = BotaoNia(
            text="Menu",
            cor=CARTAO,
            size_hint=(None, None),
            size=(dp(65), dp(46)),
            font_size="13sp"
        )

        menu.bind(on_release=self.abrir_menu)
        cabecalho.add_widget(menu)

        self.principal.add_widget(cabecalho)

    # =================================
    # BOAS-VINDAS FIXAS
    # =================================

    def criar_boas_vindas(self):

        self.boas_vindas = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(225),
            spacing=dp(5),
            padding=[dp(8), dp(4), dp(8), dp(4)]
        )

        if os.path.exists(CAMINHO_NIA):

            imagem = Image(
                source=CAMINHO_NIA,
                size_hint=(1, None),
                height=dp(125),
                allow_stretch=True,
                keep_ratio=True
            )

            self.boas_vindas.add_widget(imagem)

        else:

            simbolo = Label(
                text="◉",
                color=LARANJA,
                font_size="70sp",
                size_hint=(1, None),
                height=dp(125)
            )

            self.boas_vindas.add_widget(simbolo)

        titulo = Label(
            text="[b]Olá, eu sou a Nia![/b]",
            markup=True,
            color=BRANCO,
            font_size="22sp",
            size_hint=(1, None),
            height=dp(36)
        )

        subtitulo = Label(
            text="Como posso ajudar-te hoje?",
            color=CINZENTO,
            font_size="14sp",
            size_hint=(1, None),
            height=dp(28)
        )

        self.boas_vindas.add_widget(titulo)
        self.boas_vindas.add_widget(subtitulo)

        self.principal.add_widget(self.boas_vindas)

    # =================================
    # CONVERSA COM DESLIZAMENTO
    # =================================

    def criar_conversa(self):

        self.scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(4),
            scroll_type=["bars", "content"]
        )

        self.lista = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing=dp(12),
            padding=[dp(2), dp(12), dp(2), dp(12)]
        )

        self.lista.bind(
            minimum_height=self.lista.setter("height")
        )

        self.scroll.add_widget(self.lista)
        self.principal.add_widget(self.scroll)

    # =================================
    # CAIXA DE MENSAGEM
    # =================================

    def criar_caixa_mensagem(self):

        linha = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(55),
            spacing=dp(8)
        )

        self.entrada = TextInput(
            hint_text="Conversa com a Nia...",
            multiline=False,
            font_size="15sp",
            foreground_color=BRANCO,
            hint_text_color=CINZENTO,
            cursor_color=LARANJA,
            padding=[dp(14), dp(15)],
            background_normal="",
            background_active="",
            background_color=CARTAO
        )

        self.entrada.bind(
            on_text_validate=self.enviar_mensagem
        )

        self.botao_enviar = BotaoNia(
            text="Enviar",
            font_size="14sp",
            size_hint=(None, 1),
            width=dp(60)
        )

        self.botao_enviar.bind(
            on_release=self.enviar_mensagem
        )

        linha.add_widget(self.entrada)
        linha.add_widget(self.botao_enviar)

        self.principal.add_widget(linha)

    # =================================
    # ENVIAR MENSAGEM
    # =================================

    def enviar_mensagem(self, *args):

        if self.a_processar:
            return

        pergunta = self.entrada.text.strip()

        if not pergunta:
            return

        if not API_KEY.strip():
            self.adicionar_balao(
                "Coloca a tua chave do OpenRouter na variavel API_KEY.",
                False
            )
            return

        self.entrada.text = ""
        self.a_processar = True

        self.botao_enviar.disabled = True
        self.botao_enviar.text = "..."

        self.remover_boas_vindas()
        self.adicionar_balao(pergunta, True)

        self.mensagens.append({
            "role": "user",
            "content": pergunta
        })

        self.guardar_memoria()

        contexto = list(self.mensagens)

        threading.Thread(
            target=self.consultar_ia,
            args=(contexto,),
            daemon=True
        ).start()

    # =================================
    # CONSULTAR OPENROUTER
    # =================================

    def consultar_ia(self, contexto):

        try:

            resposta = requests.post(
                URL_API,
                headers={
                    "Authorization": "Bearer " + API_KEY.strip(),
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODELO,
                    "messages": contexto
                },
                timeout=90
            )

            try:
                dados = resposta.json()
            except ValueError:
                dados = {}

            if resposta.status_code == 200:

                escolhas = dados.get("choices", [])
                texto = ""

                if escolhas:
                    texto = (
                        escolhas[0]
                        .get("message", {})
                        .get("content", "")
                    )

                if isinstance(texto, list):
                    partes = []

                    for item in texto:
                        if isinstance(item, dict):
                            partes.append(item.get("text", ""))

                    texto = "\n".join(partes)

                if not isinstance(texto, str):
                    texto = str(texto)

                if not texto.strip():
                    texto = "Nao recebi uma resposta valida. Tenta novamente."

                Clock.schedule_once(
                    lambda dt, t=texto:
                    self.resposta_recebida(t, True),
                    0
                )

            elif resposta.status_code == 429:

                Clock.schedule_once(
                    lambda dt: self.resposta_recebida(
                        "O servico esta temporariamente limitado "
                        "ou ocupado. Aguarda um pouco e tenta novamente.",
                        False
                    ),
                    0
                )

            else:

                detalhe = dados.get("error", {})

                if isinstance(detalhe, dict):
                    detalhe = detalhe.get("message", str(detalhe))

                mensagem_erro = (
                    "Nao foi possivel obter uma resposta. Codigo HTTP: "
                    + str(resposta.status_code)
                    + "\n"
                    + str(detalhe)
                )

                Clock.schedule_once(
                    lambda dt, t=mensagem_erro:
                    self.resposta_recebida(t, False),
                    0
                )

        except requests.exceptions.Timeout:

            Clock.schedule_once(
                lambda dt: self.resposta_recebida(
                    "A ligacao demorou demasiado tempo. "
                    "Verifica a Internet e tenta novamente.",
                    False
                ),
                0
            )

        except requests.exceptions.RequestException:

            Clock.schedule_once(
                lambda dt: self.resposta_recebida(
                    "Não consegui ligar-me a Internet. "
                    "Verifica a tua ligação e tenta novamente.",
                    False
                ),
                0
            )

        except Exception as erro:

            Clock.schedule_once(
                lambda dt, t=str(erro):
                self.resposta_recebida(
                    "Ocorreu um erro: " + t,
                    False
                ),
                0
            )

    # =================================
    # MOSTRAR RESPOSTA
    # =================================

    def resposta_recebida(self, texto, guardar_contexto=True):

        self.adicionar_balao(texto, False)

        if guardar_contexto:
            self.mensagens.append({
                "role": "assistant",
                "content": texto
            })

            self.guardar_memoria()

        self.a_processar = False
        self.botao_enviar.disabled = False
        self.botao_enviar.text = "Enviar"

    # =================================
    # ADICIONAR BALOES
    # =================================

    def adicionar_balao(self, texto, utilizador):

        linha = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(80),
            spacing=dp(5),
            padding=[dp(2), dp(2), dp(2), dp(2)]
        )

        balao = Balao(
            texto,
            utilizador=utilizador
        )

        recipiente = BoxLayout(
            orientation="vertical",
            size_hint=(0.88, None),
            height=dp(80)
        )

        recipiente.add_widget(balao)

        espaco = BoxLayout(
            size_hint=(0.12, None),
            height=dp(80)
        )

        if utilizador:
            linha.add_widget(espaco)
            linha.add_widget(recipiente)
        else:
            linha.add_widget(recipiente)
            linha.add_widget(espaco)

        def atualizar_altura_linha(*args):
            altura = max(dp
