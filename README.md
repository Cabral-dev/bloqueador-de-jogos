# Bloqueador de Distrações & Foco nos Estudos

Um software em Python para **autobloqueio de jogos e aplicações** durante horários de estudo. Desenvolvido para rodar de forma invisível no Windows, com interface nativa em Tkinter e uma arquitetura resiliente contra encerramentos forçados.

---

## Sobre o Projeto

Este projeto foi desenvolvido com foco em disciplina pessoal. Ele monitora continuamente os processos em execução no Windows durante horários pré-determinados e encerra automaticamente qualquer jogo ou aplicativo listado como distração, registrando a tentativa e exibindo um aviso na tela.

### Diferenciais & Arquitetura

- **Vigilância Mútua (Dois Scripts):** O projeto utiliza uma arquitetura de processo duplo (`main.py` e `guardiao.py`). Se você tentar encerrar um dos processos pelo Gerenciador de Tarefas, o outro o ressuscita em menos de 1 segundo.
- **Janelas Pop-up Inteligentes:** Pop-ups nativos em Tkinter (`Toplevel`) sempre centralizados na tela e configurados com a flag `-topmost` (sobrepõe qualquer aplicativo ativo).
- **Sem Spam de Pop-ups:** Se a janela de aviso já estiver aberta, o sistema traz a mesma janela para o topo e força o foco, sem sobrecarregar a memória do sistema.
- **Log de Tentativas:** Registra data, hora e o nome do aplicativo encerrado em um arquivo de texto no perfil do usuário (`~/historico_de_foco.txt`).
- **Execução Invisível:** Configurado para rodar via `pythonw.exe` em segundo plano na inicialização do Windows.

---

## Regras de Horários

| Dia da Semana | Horário de Bloqueio | Status |
| :--- | :--- | :--- |
| **Segunda a Quinta** | 06:00 às 19:30 | 🔒 Ativo |
| **Sexta-feira** | 06:00 às 19:00 | 🔒 Ativo |
| **Sábado e Domingo** | - | 🔓 Livre |

---

## Como Instalar e Rodar

### Pré-requisitos
- **Python 3.x** instalado.
- Biblioteca `psutil` instalada:

```bash
pip install psutil

1. Clonar e Estruturar a Pasta
Clone este repositório ou baixe os arquivos.

Mova a pasta do projeto para o diretório raiz C:\Bloqueador (para garantir a compatibilidade com os caminhos definidos nos scripts).

2. Configurar a Inicialização Automática no Windows
Pressione Win + R no teclado, digite shell:startup e pressione Enter.

Cole o arquivo main.bat contido neste repositório dentro da pasta de Inicialização do Windows.

O arquivo main.bat contém as seguintes instruções:

DOS
@echo off
cd /d "C:\Bloqueador"
start /b pythonw guardiao.py
start /b pythonw main.py
Tecnologias Utilizadas
Python 3

Tkinter (Interface gráfica nativa)

psutil (Gerenciamento e inspeção de processos do sistema)

Batch Script (Automação de boot no Windows)

Aplicativos Bloqueados por Padrão
Por padrão, a lista de monitoramento contempla os executáveis:

Roblox (robloxplayerbeta.exe)

Hydra Launcher (hydra.exe)

Minecraft (minecraft.exe)

TLauncher (tlauncher.exe)

Steam (steam.exe)

Para adicionar ou remover jogos, basta alterar a variável JOGOS no topo do arquivo main.py.

Licença
Este projeto está sob a licença MIT. Sinta-se livre para adaptar a lógica para o seu próprio fluxo de estudos e rotina!
```bash