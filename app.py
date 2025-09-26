import streamlit as st
import pandas as pd
import praw
from transformers import pipeline
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

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
    'política brasileira',
    'Manifestações', 
    'Donald Trump',
    'Eduardo Bolsonaro',
    "STF",
    "Julgamento do 8 de janeiro"]
# Usa o cache do Streamlit para carregar o modelo de IA só uma vez

@st.cache_resource
def load_model():
    """Carrega o modelo de análise de sentimento da Hugging Face."""
    model_name = "tabularisai/multilingual-sentiment-analysis"
    return pipeline("text-classification", model=model_name)

sentiment_analyzer = load_model()

# --- Lógica ---

def get_reddit_posts(query, subreddit_name="brasil", limit=100):
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
        submissions = subreddit.search(query, limit=limit, sort="new")

        content_list = []
        one_week_ago = datetime.utcnow() - timedelta(days=7)

        for post in submissions:
            post_time = datetime.utcfromtimestamp(post.created_utc)
            if post_time < one_week_ago:
                continue

            content_list.append({
                "text": post.title,
                "created_utc": post.created_utc
            })
            # Evita carregar muita coisa, carrega apenas os comentários mais votados
            post.comments.replace_more(limit=0)
            # Pega os 10 comentários mais relevantes ( os mais votados)

            for comment in post.comments.list()[:10]:
                comment_time = datetime.utcfromtimestamp(comment.created_utc)
                if comment_time < one_week_ago:
                    continue
                
                # Ignora comentários que têm https em alguma parte do texto
                if 'http' or '[removed]' not in comment.body.strip().lower():
                    content_list.append({
                        "text": comment.body,
                        "created_utc": comment.created_utc
                    })

        if not content_list:
            st.warning("Nenhum post ou comentário encontrado na última semana para sua busca.")
            return None

        return pd.DataFrame(content_list)

    except Exception as e:
        st.error(f"Ocorreu um erro ao buscar dados do Reddit: {e}")
        return None

def analyze_sentiment(df):
    """Aplica o modelo de análise de sentimento em cada texto do DataFrame."""
    if df is None:
        return None
    
    texts=[text[:512] for text in df["text"].tolist()]

    # modificação para ajeitar o problema de não processar textos com mais de 512 caracteres
    results = sentiment_analyzer(texts)

    # rótulos do modelo s
    df['sentimento'] = [result['label'] for result in results]
    df['confianca'] = [round(result['score'], 2) for result in results]

    return df

# --- Interface Gráfica com Streamlit ---

st.set_page_config(page_title="Análise de Sentimento do Reddit", layout="wide")
st.title("Análise de Sentimento sobre a política Brasileira no Reddit")
st.markdown("Selecione um termo de busca para analisar o sentimento de posts e comentários recentes no subreddit `r/brasil`.")

# Cria um menu dropdown com as queries pré-definidas
selected_query = st.selectbox("Selecione o termo de busca:", QUERIES)

if st.button(f"Analisar Sentimento para '{selected_query}'"):
    with st.spinner("Buscando e analisando discussões no Reddit... Isso pode levar um momento."):
        # 1. Busca os dados do Reddit
        reddit_df = get_reddit_posts(selected_query)

        # 2. Analisa o sentimento se  dados  encontrados
        if reddit_df is not None and not reddit_df.empty:
            results_df = analyze_sentiment(reddit_df)

            st.success(f"Análise concluída! {len(results_df)} itens (títulos e comentários) analisados.")
            
            results_df['data'] = pd.to_datetime(results_df['created_utc'], unit='s').dt.date
            
            sentiment_over_time = results_df.groupby(['data', 'sentimento']).size().unstack(fill_value=0)
            
            st.subheader("Evolução do Sentimento na Última Semana")
            st.markdown("O gráfico mostra a contagem diária de comentários/títulos para cada categoria de sentimento.")
            st.line_chart(sentiment_over_time)
            
            st.divider()

            # 3. resultados
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Distribuição Geral de Sentimentos")
                sentiment_counts = results_df['sentimento'].value_counts()
                st.bar_chart(sentiment_counts)

            with col2:
                st.subheader("Amostra dos Dados")
                # Mostra o texto, sentimento e a confiança do modelo
                st.dataframe(results_df[['text', 'sentimento', 'confianca']], height=400)
            st.balloons()