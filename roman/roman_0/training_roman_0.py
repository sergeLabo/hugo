#!python3

# roman 0


from aitextgen import aitextgen
from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2Config
from aitextgen import aitextgen


def get_config():

    return GPT2Config(
                            vocab_size=20000,
                            n_positions=1024,
                            n_ctx=1024,
                            n_embd=768,
                            n_layer=12,
                            n_head=12,
                            bos_token_id=0,
                            eos_token_id=0,
                            max_length=1024,
                            dropout=0.0
                        )

def training():

    file_name  =  "./roman_clean.txt"

    train_tokenizer(file_name)
    vocab_file = "aitextgen-vocab.json"
    merges_file = "aitextgen-merges.txt"

    config = get_config()
    ai = aitextgen(vocab_file=vocab_file, merges_file=merges_file, config=config)

    data = TokenDataset(file_name,
                        vocab_file=vocab_file,
                        merges_file=merges_file,
                        block_size=64)

    # #ai.train(data, batch_size=32, num_steps=300000)

    # #ai.generate(5, prompt="Les artistes ")

training()

"""
roman_0
131,710 sets of tokens from ./roman_clean.txt.
Loss: 0.210 — Avg: 0.207
"""
