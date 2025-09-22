# EscapeRoom




Basicamente segue o projeto de visão computacional que aciona o Step-motor
- O código funciona através da configuração de uma sequência-alvo com o openCV. (configurada como "UAU" atualmente). A partir da detecção da sequência-alvo, o código enviará sinal via comunicação serial CMO6 (precisa de adaptação para linux)
-O Arquivo mainControlador.py serve para ser embarcado num micro-controlador via Thonny e ouve comunicação serial via CMO6 --- ESPECÍCIFICO PARA WINDOWS.

---Ainda irei trabalhar para embarcar tudo na Raspberry pi 3 que Será utilizada no projeto.
