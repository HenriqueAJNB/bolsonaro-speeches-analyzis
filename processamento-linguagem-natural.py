import string
import nltk
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

# Read text files as a corpus
diretorio_corpos = "arquivos/"
discursos = nltk.corpus.reader.plaintext.PlaintextCorpusReader(diretorio_corpos, '.*')

# Function to remove stop words
def filtra_stopwords(lista: list) -> list:
    return [palavra for palavra in lista if palavra not in stopwords]

# Function to remove punctuation
def remove_pontuacao(palavra: str) -> str:
    palavra_sem_pontuacao = palavra.translate(str.maketrans({char:None for char in string.punctuation}))
    return palavra_sem_pontuacao

# Function for visualization plot
def gerar_grafico(eixo_x, eixo_y, titulo_grafico, titulo_imagem, destacar=0):
    bar_list = plt.barh(y=eixo_y, width=eixo_x, color="gray")
    for bar in bar_list[-destacar:]:
        bar.set_color("royalblue")
    plt.title(titulo_grafico, fontsize=30)
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    for x, y in enumerate(eixo_x):
        plt.text(y * 1.05, x - 0.1, str(y), fontsize=15)
    plt.tick_params(axis='x', labelsize=0, length = 0)
    plt.savefig(titulo_imagem, dpi=300, bbox_inches='tight')
    plt.show()

# Set all words to lowercase
lista_de_palavras = [palavra.lower() for palavra in discursos.words()]

# Remove punctuation
palavras_sem_pontuacao = [remove_pontuacao(palavra) for palavra in lista_de_palavras if palavra]
palavras_sem_pontuacao = list(filter(None, palavras_sem_pontuacao))

# Define the list of stopwords
stopwords = nltk.corpus.stopwords.words('portuguese')
stopwords.append("aí") # Added this word that is a stop word but was not in the nltk bag of stop words.

# Removing stop words
palavras_sem_stopwords = filtra_stopwords(palavras_sem_pontuacao)

# Counting isolated words (Bag of words)
contagem_palavras = pd.DataFrame(Counter(palavras_sem_stopwords).most_common(), columns=["palavra", "frequencia"]).sort_values(by = 'frequencia')


# Bigram analyzis
bigramas = nltk.collocations.BigramCollocationFinder.from_words(palavras_sem_stopwords)

# Calculate bigram's frequencies
bigrama_freq = bigramas.ngram_fd.items()

# Create a pandas DataFrame for the bigrams and frequencies
df_bigrama_freq = pd.DataFrame(list(bigrama_freq), columns = ['bigrama', 'frequencia']).sort_values(by = 'frequencia')
df_bigrama_freq["bigrama"] = df_bigrama_freq.bigrama.apply(str)

# Trigram analyzis
trigramas = nltk.collocations.TrigramCollocationFinder.from_words(palavras_sem_stopwords)

# Calculate trigram's frequencies
trigrama_freq = trigramas.ngram_fd.items()

# Create a pandas DataFrame for the trigrams and frequencies
df_trigrama_freq = pd.DataFrame(list(trigrama_freq), columns = ['trigrama', 'frequencia']).sort_values(by = 'frequencia')
df_trigrama_freq["trigrama"] = df_trigrama_freq.trigrama.apply(str)

# Set some configuration for plotting
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 15),
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large'}
plt.rcParams.update(params)

# Generating visualization for isolated words
gerar_grafico(eixo_x = contagem_palavras.frequencia,
              eixo_y = contagem_palavras.palavra, 
              titulo_grafico = "President Bolsonaro speeches:\n Rank of 15 most common isolated words found",
              titulo_imagem = "palavras-isoladas.png",
              destacar=3)

# Generating visualization for bigrams
gerar_grafico(eixo_x = df_bigrama_freq.frequencia,
              eixo_y = df_bigrama_freq.bigrama, 
              titulo_grafico = "President Bolsonaro speeches:\n Rank of 15 most common bigrams",
              titulo_imagem = "bigrama.png",
              destacar=3)

# Generating visualization for trigrams
gerar_grafico(eixo_x = df_trigrama_freq.frequencia,
              eixo_y = df_trigrama_freq.trigrama, 
              titulo_grafico = "President Bolsonaro speeches:\n Rank of 15 most common trigrams",
              titulo_imagem = "trigrama.png",
              destacar=2)
