from transformers import AutoTokenizer

def tokenizer_minify(mname, vocab_keep_items, minified_tokenizer_name):
    tokenizer = AutoTokenizer.from_pretrained(mname, use_fast=True)
    assert tokenizer.is_fast, "This only works for fast tokenizers."
    vocab = tokenizer.get_vocab()
    training_corpus = [ vocab.keys() ] # Should be a generator of list of texts.
    new_tokenizer = tokenizer.train_new_from_iterator(training_corpus, vocab_size=vocab_keep_items)
    new_tokenizer.save_pretrained(minified_tokenizer_name)