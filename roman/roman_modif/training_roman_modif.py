#!python3

# roman_modif


from my_aitextgen import aitextgen
from my_aitextgen.TokenDataset import TokenDataset
from my_aitextgen.tokenizers import train_tokenizer
from my_aitextgen.utils import GPT2ConfigCPU, GPT2Config


class Training:

    def __init__(self, vocab_size, file_name):

        self.vocab_size = vocab_size
        self.file_name = file_name
        self.config = self.get_config()
        self.vocab_file = None
        self.merges_file = None

    def get_config(self):

        # #conf = GPT2Config(
                                # #vocab_size=self.vocab_size,
                                # #n_positions=1024,
                                # #n_ctx=1024,
                                # #n_embd=768,
                                # #n_layer=12,
                                # #n_head=12,
                                # #bos_token_id=0,
                                # #eos_token_id=0,
                                # #max_length=1024,
                                # #dropout=0.0
                            # #)
        # #print(conf)
        # #return conf
        return GPT2ConfigCPU()

    def get_aitextgen(self):

        print("Load aitextgen")
        ai = aitextgen(   vocab_file=self.vocab_file,
                            merges_file=self.merges_file,
                            config=self.config)
        print("Done.")
        return ai

    def get_data(self):

        print("ComputeTokenDataset")
        tk = TokenDataset(  self.file_name,
                            vocab_file=self.vocab_file,
                            merges_file=self.merges_file,
                            block_size=64)  # 64
        print("Done.")
        return tk

    def training(self):

        # Génère les fichiers aitextgen-vocab.json et aitextgen-merges.txt
        train_tokenizer(self.file_name, vocab_size=self.vocab_size)
        self.vocab_file = "aitextgen-vocab.json"
        self.merges_file = "aitextgen-merges.txt"

        ai = self.get_aitextgen()
        data = self.get_data()

        print("Début du training:")
        ai.train(data, batch_size=32, num_steps=1000,
                     save_every=100, generate_every=100,
                     benchmark=True)


if __name__ == "__main__":

    file_name  =  "./roman_modif.txt"
    VOCAB_SIZE = 1000
    t = Training(VOCAB_SIZE, file_name)
    t.training()


"""

"""
