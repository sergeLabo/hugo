#!python3


from aitextgen import aitextgen
from aitextgen.utils import GPT2Config


class AiTextGen:

    def __init__(self):
        """Charge le gpt2 model de /aitextgen si existe,
        sinon le télécharge dans /aitextgen."""

        self.prompt = "Romeo: "
        self.config = self.get_config()
        print("Config chargée.")
        print("    soit:\n", self.config)

        print("Création de aitextgen():")
        ai = aitextgen()
        print("Done.")

        self.vocab_file = "aitextgen-vocab.json"
        self.merges_file = "aitextgen-merges.txt"

        print("Chargement du modèle pytorch ...")
        self.ai = aitextgen(model="./trained_model/pytorch_model.bin",
                            vocab_file=self.vocab_file,
                            merges_file=self.merges_file,
                            config=self.config)


    def get_config(self):
        """La config du modèle

        self.config = GPT2Config {
                                  "activation_function": "gelu_new",
                                  "attn_pdrop": 0.1,
                                  "bos_token_id": 0,
                                  "dropout": 0.0,
                                  "embd_pdrop": 0.1,
                                  "eos_token_id": 0,
                                  "initializer_range": 0.02,
                                  "layer_norm_epsilon": 1e-05,
                                  "max_length": 1024,
                                  "model_type": "gpt2",
                                  "n_ctx": 1024,
                                  "n_embd": 768,
                                  "n_head": 12,
                                  "n_layer": 12,
                                  "n_positions": 1024,
                                  "resid_pdrop": 0.1,
                                  "summary_activation": null,
                                  "summary_first_dropout": 0.1,
                                  "summary_proj_to_labels": true,
                                  "summary_type": "cls_index",
                                  "summary_use_proj": true,
                                  "vocab_size": 20000
                                }
        """

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


    def get_irc_response(self, prompt, len_max, temp):

        if isinstance(prompt, str):
            resp = self.ai.generate(n=1,
                                    prompt=prompt,
                                    max_length=len_max,
                                    temperature=temp,
                                    return_as_list=True)

        return resp


    def interactif(self):
        """
        See this article by Huggingface engineer Patrick von Platen for how sampling and these parameters are used in practice.

        n: Number of texts generated.
        max_length: Maximum length of the generated text (default: 200; for GPT-2, the maximum is 1024.)
        prompt: Prompt that starts the generated text and is included in the generate text. (used to be prefix in previous tools)
        temperature: Controls the "craziness" of the text (default: 0.7)
        top_k: If nonzero, limits the sampled tokens to the top k values. (default: 0)
        top_p: If nonzero, limits the sampled tokens to the cumulative probability

        Some lesser-known-but-still-useful-parameters that are unique to Transformers:

        num_beams: If greater than 1, executes beam search for cleaner text.
        repetition_penalty: If greater than 1.0, penalizes repetition in a text to avoid infinite loops.
        length_penalty: If greater than 1.0, penalizes text proportional to the length
        no_repeat_ngram_size: Token length to avoid repeating given phrases.

        input_context = 'The dog'
        input_ids = tokenizer.encode(input_context, return_tensors='pt')  # encode input context
        """

        while 1:
            try:
                prompt = input("Entrer un début de phrase:\n")
            except:
                prompt = "Ne jouer pas à ce petit jeu !"

            print(f'Prompt = {prompt}')
            print(f'type de prompt = {type(prompt)}')

            if isinstance(prompt, str) and len(prompt) > 4:
                resp = self.ai.generate(n=1,
                                        prompt=prompt,
                                        max_length=100,
                                        temperature=0.8,
                                        return_as_list=True)
                print(f"\n\nLa Labo n'a pas écrit:\n{resp[0]}\n\n")
            else:
                print("Raté")


if __name__ == "__main__":

    atg = AiTextGen()
    atg.interactif()
