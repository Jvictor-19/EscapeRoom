# Relatório
## 25/09/2025
### Resumo
Documentação feita e testes no Arduino Nano foram realizados.

### O que foi feito
- Testei os módulos no Arduino Nano e funcionaram corretamente, eu sabia que não teria tanto problema pois as arquiteturas são muito parecidas, mas tive que testar
- Escrevi comentários explicando cada componentezinho de cada uma das classes que escrevi, acredito que isso ajudará caso alguém mexa nesse código futuramente

### Pensamentos e dificuldades
Não tive muita dificuldade, foi apenas escrever.

Tá chegando perto da data de entrega, 27/09, sinto que não fiz tanto comparado com a parte do raspberry pi, pelo que foi mostrado tá bem legal.
Mas eu ainda não tenho nada muito concreto, pelo menos Calebe já apareceu com o componente que será usado para a parte do livro. Mas eu realmente queria
um mapa das conexões que serão feitas nos pinos.

### Próximos passos
- Criar exemplos de uso para visualização dentro da Arduino IDE
- Escrever um módulo para o leitor RFID que Calebe mostrou

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

