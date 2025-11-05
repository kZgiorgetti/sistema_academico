import math

def tokenize(text):
    return [w.lower() for w in text.split()]

def tfidf(corpus):
    # Calcula TF-IDF simples
    docs = [tokenize(text) for text in corpus]
    vocab = set(word for doc in docs for word in doc)
    idf = {}
    N = len(docs)
    for word in vocab:
        idf[word] = math.log(N / sum(1 for doc in docs if word in doc))
    vectors = []
    for doc in docs:
        tf = {w: doc.count(w) / len(doc) for w in doc}
        vec = {w: tf.get(w, 0) * idf[w] for w in vocab}
        vectors.append(vec)
    return vectors, vocab

def cosine_similarity(vec1, vec2):
    num = sum(vec1[w] * vec2.get(w, 0) for w in vec1)
    den1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    den2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    return num / (den1 * den2) if den1 * den2 != 0 else 0

def recommend_activity(activities, query):
    if not activities:
        return {"message": "Nenhuma atividade disponível"}
    corpus = activities + [query]
    vectors, vocab = tfidf(corpus)
    query_vec = vectors[-1]
    sims = [cosine_similarity(v, query_vec) for v in vectors[:-1]]
    idx = sims.index(max(sims))
    return {"recommended": activities[idx], "similarity": sims[idx]}


# ====== TESTE DIRETO ======
if __name__ == "__main__":
    atividades = [
        "Aula sobre redes de computadores e TCP IP",
        "Introdução à inteligência artificial e aprendizado de máquina",
        "Desenvolvimento de sistemas distribuídos em Python",
        "Estrutura de dados e algoritmos em C",
        "Engenharia de software ágil e metodologias Scrum e Kanban"
    ]

    consulta = input("Descreva o tema da atividade que deseja (ex: programação em rede): ")

    resultado = recommend_activity(atividades, consulta)

    print("\n🔍 Recomendação de atividade com base na IA:")
    print(f"Atividade sugerida: {resultado['recommended']}")
    print(f"Similaridade: {resultado['similarity']:.3f}")
