# Relatório
## 02/10/2025
### Resumo
Essa foi a semana de mexer com RFID, o prazo era até o dia 27/09, mas Calebe disse que tava ok passar, então comprei 2 leitores pelo mercado livre, que chegaram na segunda-feira. Desde o dia da entrega
fique estudando como os leitores de RFID funcionam. O código foi implementado com sucesso e acredito que é só mudar as configurações do programa que ele vai funcionar para vários leitores, não só dois. 
Também acredito que esse programa já pode ser usado no escape room, pelo menos pelo que eu sei de informação sobre os desafios.

### O que foi implementado
- EscapeRoom.ino:
  
  Esse arquivo já existia, mas agora ele comporta o programa que talvez rode no microcontrolador do escape room. É o arquivo principal que deve ser carregado.
  No topo do programa há algumas constantes que servem para configurar o programa para o uso, não sei quantos livros serão usados no desafio, Calebe não respondeu a minha pergunta, então fiz
  expansível, vai comportar vários junto enquanto tiver pinos suficientes no Microcontrolador. Tudo está comentado e explicado no código, acesso o arquivo e configure o que for necessário. 
  Constei com a saída lógica após a leitura correta dos cartões e tags, imagino que isso se ligue num relê que destrave alguma tranca, e também imaginei que seria necessário um botão mestre
  que ative o sinal lógico independente do estado dos leitores.

### Pensamentos e dificuldades
Ter um objetivo mais concreto me fez sentir melhor escrevendo o código, sabendo que eu tinha um objetivo concreto em mente. A maior dificuldade foi o fato de eu não conseguir pegar os leitores 
com Calebe, pois estou no interior, mas isso foi resolvido no Mercado Livre, tive que gastar um dinheiro mas tudo bem pois aumento minha coleção de componentes eletrônicos.

### Próximos passos
Sinceramente, não sei, é esperar o feedback, ver se algo precisa ser mudado.

## 25/09/2025
### Resumo
Alguma coisa aconteceu e o relatório deste dia não está aqui, não sei o que aconteceu na hora de commitar mas eu escrevi. Bem, eu lembro o que foi feito, então só vai ficar com o resumo.

Eu escrevi a documentação das classes que criei e um tutorial de como instalá-las. Foi isso, bem pouco.
## 19/09/2025
### Resumo
Foram implementados quatro módulos para o Arduino, eles são bem genéricos, pois ainda não tem nada muito concreto planejado

### O que foi implementado
- Coroutine: Wrapper que adiciona cooldown a funções, não permitindo a chamada enquanto esse cooldown não estiver zerado, abrindo a possibilidade para ciclos e delays não bloqueantes
- ChestLock: Abstração de como será o baú que Calebe descreveu
- SimpleInput: Wrapper idiomático para funções padrões do Arduino voltado a pinos de input
- SimpleOutput: Wrapper idiomático para funções padrões do Arduino voltado a pinos de output

### Pensamentos e dificuldades
Por enquanto só aquela briga convencional com o compilador do c++, estou tentando usar as funcionalidades da linguagem ao invés de 
só ficar no C básico bruto. 

A maior dificuldade é a falta de concretude de como as coisas serão implementadas, não tenho a pinagem e nem os componentes que vão ser usados. 
As vezes sinto que isso que já escrevi talvez tenha de ser descartado, pois não sei exatamente o que será usado. Estou atirando no escuro.

Por enquanto os códigos todos foram testados em um Arduino Uno e não num Nano. Isso se deve ao fato de que acho melhor de prototipar no Uno, mas
logo testarei no Nano. E creio que isso não tem tanto problema, o microcontrolador dos dois são muito parecidos.

### Próximos passos
- Documentar melhor dentro do código o que já está feito
- Criar exemplos de uso para visualização dentro da Arduino IDE
- Escrever documentação de instalação da biblioteca na Arduino IDE
- Testar os códigos no Arduino Nano
- ~~Módulo de relógio digital em tela LCD~~[^1]

[^1]: Não será mais necessário fazer esse módulo

