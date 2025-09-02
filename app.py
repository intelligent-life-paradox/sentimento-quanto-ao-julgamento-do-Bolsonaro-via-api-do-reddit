import streamlit as st
import pandas as pd
import praw
from transformers import pipeline
from dotenv import load_dotenv
import os

# --- Configuração e odelo ---

# Carrega as variáveis de ambiente  do meu .env
load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# queries 
QUERIES = [
    "Bolsonaro preso",
    "Bolsonaro inocente",
    "Julgamento do Bolsonaro",
    "Alexandre de Moraes",
    "Julgamento do Golpe",
    "STF",
    "Julgamento da cúpula militar",
    "Julgamento do 8 de janeiro"]
# Usa o cache do Streamlit para carregar o modelo de IA só uma vez
@st.cache_resource
def load_model():
    """Carrega o modelo de análise de sentimento da Hugging Face."""
    model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    return pipeline("sentiment-analysis", model=model_name)

sentiment_analyzer = load_model()

# --- Lógica ---

def get_reddit_posts(query, subreddit_name="brasil", limit=15):
    """Busca posts e comentários no Reddit usando a biblioteca PRAW."""
    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
        st.error("Credenciais do Reddit não encontradas! Verifique seu arquivo .env.")
        return None
    
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
        
        subreddit = reddit.subreddit(subreddit_name)
        # Busca por posts (submissions) que contenham a query no título ou no corpo
        submissions = subreddit.search(query, limit=limit)
        
        content_list = []
        for post in submissions:
           
            content_list.append({"text": post.title})
            # Evita carregar muita coisa, carrega apenas os comentários mais votados
            post.comments.replace_more(limit=0)
            # Pega os 10 comentários mais relevantes ( os mais votados)
            for comment in post.comments.list()[:10]:
                content_list.append({"text": comment.body})

        if not content_list:
            st.warning("Nenhum post ou comentário encontrado para sua busca.")
            return None

        return pd.DataFrame(content_list)

    except Exception as e:
        st.error(f"Ocorreu um erro ao buscar dados do Reddit: {e}")
        return None

def analyze_sentiment(df):
    """Aplica o modelo de análise de sentimento em cada texto do DataFrame."""
    if df is None:
        return None
    
    # O pipeline processa a lista de textos de uma vez 
    results = sentiment_analyzer(df["text"].tolist())
    
    # Os rótulos do modelo são 'Positive', 'Negative', 'Neutral'.
    df['sentimento'] = [result['label'] for result in results]
    df['confianca'] = [round(result['score'], 2) for result in results]
    
    return df

# --- Interface Gráfica com Streamlit ---

st.set_page_config(page_title="Análise de Sentimento do Reddit", layout="wide")
st.title("Análise de Sentimento sobre o Julgamento da cúpula militar e Bolsonaro no Reddit")
st.markdown("Selecione um termo de busca para analisar o sentimento de posts e comentários recentes no subreddit `r/brasil`.")

# Cria um menu dropdown com as queries pré-definidas
selected_query = st.selectbox("Selecione o termo de busca:", QUERIES)

if st.button(f"Analisar Sentimento para '{selected_query}'"):
    with st.spinner("Buscando e analisando discussões no Reddit... Isso pode levar um momento."):
        # 1. Busca os dados do Reddit
        reddit_df = get_reddit_posts(selected_query)

        # 2. Analisa o sentimento se os dados foram encontrados
        if reddit_df is not None:
            results_df = analyze_sentiment(reddit_df)
            
            st.success(f"Análise concluída! {len(results_df)} itens (títulos e comentários) analisados.")
            
            # 3. resultados
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Distribuição de Sentimentos")
                sentiment_counts = results_df['sentimento'].value_counts()
                st.bar_chart(sentiment_counts)
            
            with col2:
                st.subheader("Amostra dos Dados")
                # Mostra o texto, sentimento e a confiança do modelo
                st.dataframe(results_df[['text', 'sentimento', 'confianca']], height=300)