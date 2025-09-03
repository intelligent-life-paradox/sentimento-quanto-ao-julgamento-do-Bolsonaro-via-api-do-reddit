📊 **Análise de Sentimento: Reações ao Julgamento de Bolsonaro no Reddit**
Este projeto é uma aplicação web containerizada que realiza análise de sentimento em tempo real sobre discussões no subreddit r/brasil a respeito do julgamento do ex-presidente Jair Bolsonaro e da cúpula militar, com foco nos eventos ocorridos em 2 de setembro de 2025.
A aplicação permite que o usuário selecione um tópico de busca relacionado ao julgamento e visualiza a distribuição de sentimentos (Positivo,muito positivo, Negativo, muito negativo, Neutro) dos posts e comentários mais recentes. O modelo tabularisai/multilingual-sentiment-analysis não necessariamente serve para medir associação política do autor de algum comentário, pense nele mais como uma métrica do sentimento que o autor passa ao escrever algo. 



*Contexto do Julgamento (02 de Setembro de 2025) Gerado por IA*:
Em 2 de setembro de 2025, o Supremo Tribunal Federal (STF) deu início a uma das fases mais críticas do julgamento envolvendo o ex-presidente Jair Bolsonaro e membros da cúpula militar de seu governo. As acusações centrais giram em torno da investigação sobre a tentativa de golpe de Estado após as eleições de 2022.
Nesta data, o plenário do STF começou a analisar as evidências coletadas pela Polícia Federal, que incluem trocas de mensagens, vídeos de reuniões e depoimentos que apontam para uma suposta articulação para anular o resultado eleitoral e manter o então presidente no poder. O ministro Alexandre de Moraes, relator do caso, apresentou seu voto, que foi acompanhado por uma intensa cobertura midiática e gerou uma onda de manifestações e debates acalorados nas redes sociais, tornando-se um dos tópicos mais comentados do dia.
Este projeto visa capturar e analisar o sentimento da comunidade do Reddit, uma das maiores plataformas de discussão do Brasil, em relação a este evento histórico.




 *Tecnologias Utilizadas*
  Este projeto foi construído utilizando um conjunto de ferramentas modernas de Data Science e DevOps, empacotadas para garantir portabilidade e facilidade de execução.

  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg" alt="Docker" width="40"> 
 	<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="40">	
  Streamlit
  
  Reddit API 
  
  <img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" alt="Hugging Face" width="40">	
	<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg" alt="Pandas" width="40">	


 
**Como executar o projeto**


para rodar esta aplicação na sua máquina, você precisará ter o Docker Desktop instalado!
1. Pré-requisitos
Docker Desktop: Instale aqui
Credenciais da API do Reddit:
	Crie um aplicativo do tipo "script" na página de aplicativos do Reddit.
	Você precisará do seu client_id, client_secret e username.


2. Configuração
Clone este repositório:
   
	Bash


	git clone https://github.com/este_repositorio.git
	

	
 Crie o arquivo de ambiente:
		Crie um arquivo chamado .env na raiz do projeto e adicione suas credenciais do Reddit:

	REDDIT_CLIENT_ID="SEU_CLIENT_ID_AQUI"
	REDDIT_CLIENT_SECRET="SEU_CLIENT_SECRET_AQUI"
	REDDIT_USER_AGENT="script:analise-app:v1 (by /u/SEU_USERNAME_AQUI)"


3. Build e Execução
Construa a imagem Docker:
	Este comando pode levar vários minutos na primeira vez, pois ele baixará e instalará todas as dependências.
   	
	Bash


	docker build -t analise-sentimento .
	
 
 	Execute o container:
		Bash


		docker run -p 8501:8501 --env-file .env analise-sentimento
	Acesse a aplicação:
	Abra seu navegador e acesse http://localhost:8501.

5. Se por algum motivo esse caminho de execução não funcionar, passe seus suas credenciais via bash(powershell) na hora de rodar o container da seguinte maneira:

   		docker run -p 8501:8501 -e REDDIT_CLIENT_ID="SEU_NOVO_CLIENT_ID" -e REDDIT_CLIENT_SECRET="SEU_NOVO_CLIENT_SECRET" -e REDDIT_USER_AGENT="script:nome-do-novo-app:v1 (by /u/seu_username)" analise-julgamento

 Ps:  por motivos de R$ não quero disponibilizar a imagem do container em algum serviço de nuvem, porém esse tutorial é bom o bastante para você rodar sua própria aplicação num container local. Caso você queira ver a aplicação rodando numa URL pública que não incorre em nenhum gasto para o autor, veja o file Aplicativo do Streamlit URL



