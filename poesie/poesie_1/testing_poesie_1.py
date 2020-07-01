#!python3


from time import sleep
from aitextgen import aitextgen
from aitextgen.utils import GPT2Config


class Poesie:

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


    def get_irc_response(self, prompt, len_max, temp):

        if isinstance(prompt, str):
            resp = self.ai.generate(n=1,
                                    prompt=prompt,
                                    max_length=len_max,
                                    temperature=temp,
                                    return_as_list=True)

        return resp


    def interactif(self):

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
                print(f"\n\nVictor Hugo n'a pas écrit:\n{resp[0]}\n\n")
            else:
                print("Raté")


    def loop(self):

        try:
            resp = input("\nEntrer un début de phrase:\n")
        except:
            resp = "Ne jouer pas à ce petit jeu !"
        if not resp:
            resp = "Quoi?"

        while 1:
            resp = self.ai.generate(n=1,
                                    prompt=resp,
                                    max_length=30,
                                    temperature=1.5,
                                    return_as_list=True)

            print(f"\n\n{resp[0]}")

            resp = resp[0].replace("\n", " ")
            mots = resp.split(" ")
            rl = mots[-3:]
            resp = rl[0] + " " + rl[1] + " " + rl[2]
            sleep(5)






if __name__ == "__main__":

    atg = Poesie()
    # #atg.interactif()
    atg.loop()
