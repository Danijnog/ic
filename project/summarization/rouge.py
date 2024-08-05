from rouge_score import rouge_scorer

def compare_models(generated_first_summary, generated_second_summary, models):
    # Referência para avaliação
    referencia = """
    - Discussão sobre a situação política do Brasil
    - Embate político no Telegram
    - Notícias sobre o Banco Mundial
    - Notícias e discussões relacionado a estupro, aborto e fake news
    - Críticas a Lula e Bolsonaro por parte de apoiadores de ambos os lados
    - Notícias sobre Dino e Anderson Torres
    - Organização para protestos em Brasília
    """

    # Realizar a avaliação de sumarização
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores_from_first_model = scorer.score(generated_first_summary, referencia)
    scores_from_second_model = scorer.score(generated_second_summary, referencia)

    print("Métricas de avaliação para cada modelo: ")
    print()
    for idx, modelo in enumerate(models):
        scores = [scores_from_first_model, scores_from_second_model][idx]
        print(f"Modelo: {modelo}")
        for metric_name, metric_scores in scores.items():
            print(f"{metric_name.upper()}: Precision: {metric_scores.precision: .4f}, Recall: {metric_scores.recall:.4f}, Score: {metric_scores.fmeasure:.4f}")
            print()