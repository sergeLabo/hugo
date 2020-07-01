#!python3

# poesie hugo 1


from aitextgen import aitextgen
from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2Config
from aitextgen import aitextgen


def get_config():

    return GPT2Config(
                            vocab_size=10000,
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

    file_name  =  "./poesie_clean.txt"

    train_tokenizer(file_name)
    vocab_file = "aitextgen-vocab.json"
    merges_file = "aitextgen-merges.txt"

    config = get_config()
    ai = aitextgen(vocab_file=vocab_file, merges_file=merges_file, config=config)

    data = TokenDataset(file_name,
                        vocab_file=vocab_file,
                        merges_file=merges_file,
                        block_size=64)

    ai.train(data, batch_size=32, num_steps=180000)

    ai.generate(5, prompt="Les artistes ")

training()


"""
temps de trining 26:37:34
poesie hugo 1
Encoding 50,741 sets of tokens from ./poesie_clean.txt
debut Loss: 6.521 — Avg: 8.438 — GPU Mem: 5174 MB:
fin   Loss: 0.140 — Avg: 0.141

Finetune GPT-2

The next cell will start the actual finetuning of GPT-2 in aitextgen. It runs
for num_steps, and a progress bar will appear to show training progress, current
loss (the lower the better the model), and average loss (to give a sense on loss
trajectory).

The model will be saved every save_every steps in trained_model by default, and
when training completes. If you mounted your Google Drive, the model will also
be saved there in a unique folder.

The training might time out after 4ish hours; if you did not mount to Google
Drive, make sure you end training and save the results so you don't lose them! (if this happens frequently, you may want to consider using Colab Pro)

Important parameters for train():

    line_by_line: Set this to True if the input text file is a single-column CSV,
    with one record per row. aitextgen will automatically process it optimally.
    from_cache: If you compressed your dataset locally (as noted in the previous
    section) and are using that cache file, set this to True.
    num_steps: Number of steps to train the model for.
    generate_every: Interval of steps to generate example text from the model;
    good for qualitatively validating training.
    save_every: Interval of steps to save the model: the model will be saved in
    the VM to /trained_model.
    save_gdrive: Set this to True to copy the model to a unique folder in your
    Google Drive, if you have mounted it in the earlier cells

Here are other important parameters for train() that are useful but you likely
do not need to change.

    learning_rate: Learning rate of the model training.
    batch_size: Batch size of the model training; setting it too high will cause
    the GPU to go OOM.
"""
