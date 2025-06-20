import torch

def extract_attention_words(model, tokenizer, text):
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs, output_attentions=True)
        attentions = outputs.attentions  # Tuple: (num_layers, batch, num_heads, seq_len, seq_len)
        # Mean over layers & heads
        attn_matrix = torch.stack(attentions).mean(dim=0).mean(dim=1).squeeze(0)  # shape: [seq_len, seq_len]
        token_importance = attn_matrix.sum(dim=0)
        token_importance = token_importance / token_importance.sum()
        tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        word_scores = []
        for tok, score in zip(tokens, token_importance):
            if tok not in ["[CLS]", "[SEP]", "[PAD]"]:
                word_scores.append({"token": tok, "score": round(float(score), 4)})
        top_tokens = sorted(word_scores, key=lambda x: x["score"], reverse=True)[:5]
        return top_tokens
    except Exception as e:
        print("Attention extraction error:", e)
        return []
