#!python3

# roman_2


from aitextgen import aitextgen
from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2Config
from aitextgen import aitextgen


class Training:
    """
    https://docs.aitextgen.io/tutorials/colab/

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

    def __init__(self, vocab_size, file_name):

        self.vocab_size = vocab_size
        self.file_name = file_name
        self.config = self.get_config()
        self.vocab_file = None
        self.merges_file = None

    def get_config(self):
        """
        This is the configuration class to store the configuration of a :class:`~transformers.GPT2Model`.
        It is used to instantiate an GPT-2 model according to the specified arguments, defining the model
        architecture. Instantiating a configuration with the defaults will yield a similar configuration to that of
        the GPT-2 `small <https://huggingface.co/gpt2>`__ architecture.

        Configuration objects inherit from  :class:`~transformers.PretrainedConfig` and can be used
        to control the model outputs. Read the documentation from  :class:`~transformers.PretrainedConfig`
        for more information.


        Args:
            vocab_size (:obj:`int`, optional, defaults to 50257):
                Vocabulary size of the GPT-2 model. Defines the different tokens that
                can be represented by the `inputs_ids` passed to the forward method of :class:`~transformers.GPT2Model`.
            n_positions (:obj:`int`, optional, defaults to 1024):
                The maximum sequence length that this model might ever be used with.
                Typically set this to something large just in case (e.g., 512 or 1024 or 2048).
            n_ctx (:obj:`int`, optional, defaults to 1024):
                Dimensionality of the causal mask (usually same as n_positions).
            n_embd (:obj:`int`, optional, defaults to 768):
                Dimensionality of the embeddings and hidden states.
            n_layer (:obj:`int`, optional, defaults to 12):
                Number of hidden layers in the Transformer encoder.
            n_head (:obj:`int`, optional, defaults to 12):
                Number of attention heads for each attention layer in the Transformer encoder.
            activation_function (:obj:`str`, optional, defaults to 'gelu'):
                Activation function selected in the list ["relu", "swish", "gelu", "tanh", "gelu_new"].
            resid_pdrop (:obj:`float`, optional, defaults to 0.1):
                The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.
            embd_pdrop (:obj:`int`, optional, defaults to 0.1):
                The dropout ratio for the embeddings.
            attn_pdrop (:obj:`float`, optional, defaults to 0.1):
                The dropout ratio for the attention.
            layer_norm_epsilon (:obj:`float`, optional, defaults to 1e-5):
                The epsilon to use in the layer normalization layers
            initializer_range (:obj:`float`, optional, defaults to 16):
                The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
            summary_type (:obj:`string`, optional, defaults to "cls_index"):
                Argument used when doing sequence summary. Used in for the multiple choice head in
                :class:`~transformers.GPT2DoubleHeadsModel`.
                Is one of the following options:

                - 'last' => take the last token hidden state (like XLNet)
                - 'first' => take the first token hidden state (like Bert)
                - 'mean' => take the mean of all tokens hidden states
                - 'cls_index' => supply a Tensor of classification token position (GPT/GPT-2)
                - 'attn' => Not implemented now, use multi-head attention
            summary_use_proj (:obj:`boolean`, optional, defaults to :obj:`True`):
                Argument used when doing sequence summary. Used in for the multiple choice head in
                :class:`~transformers.GPT2DoubleHeadsModel`.
                Add a projection after the vector extraction
            summary_activation (:obj:`string` or :obj:`None`, optional, defaults to :obj:`None`):
                Argument used when doing sequence summary. Used in for the multiple choice head in
                :class:`~transformers.GPT2DoubleHeadsModel`.
                'tanh' => add a tanh activation to the output, Other => no activation.
            summary_proj_to_labels (:obj:`boolean`, optional, defaults to :obj:`True`):
                Argument used when doing sequence summary. Used in for the multiple choice head in
                :class:`~transformers.GPT2DoubleHeadsModel`.
                If True, the projection outputs to config.num_labels classes (otherwise to hidden_size). Default: False.
            summary_first_dropout (:obj:`float`, optional, defaults to 0.1):
                Argument used when doing sequence summary. Used in for the multiple choice head in
                :class:`~transformers.GPT2DoubleHeadsModel`.
                Add a dropout before the projection and activation

        Example::

            from transformers import GPT2Model, GPT2Config

            # Initializing a GPT2 configuration
            configuration = GPT2Config()

            # Initializing a model from the configuration
            model = GPT2Model(configuration)

            # Accessing the model configuration
            configuration = model.config

            "activation_function": "gelu_new",
            "attn_pdrop": 0.1,
            "bos_token_id": 0,uint16
            "dropout": 0.0,
            "embd_pdrop": 0.1,
            "eos_token_id": 0,
            "initializer_range": 0.02,
            "layer_norm_epsilon": 1e-05,
            "max_length": 64,
            "model_type": "gpt2",
            "n_ctx": 4,
            "n_embd": 4,
            "n_head": 1,
            "n_layer": 1,
            "n_positions": 4,
            "resid_pdrop": 0.1,
            "summary_activation": null,
            "summary_first_dropout": 0.1,
            "summary_proj_to_labels": true,
            "summary_type": "cls_index",
            "summary_use_proj": true,
            "vocab_size": 40000

        """

        conf = GPT2Config(
                                vocab_size=self.vocab_size,
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
        print(conf)
        return conf

    def get_aitextgen(self):
        """
        Class that serves as the main aitextgen object for training and generation.

        :param model: Either the file path of a PyTorch GPT-2 model, or a string
        representing the Huggingface model to download.
        :param config: Either a file path of a config.json representing the model,
        or a GPT2Config with the model architecture.
        :param vocab_file: Path to a vocab file (generated by train_tokenizer())
        :param merges_file: Path to a merges file (generated by train_tokenizer())
        :param cache_dir: folder path which downloaded models will be stored and loaded
        :param tf_gpt2: model indicator of OpenAI-distributed version of GPT-2.
        This will convert the model to PyTorch if not present.
        :param to_gpu: Whether to load the model into the GPU after loading
        (good for generation)
        :param to_fp16: Whether to convert the model to FP16 before loading
        to GPU (for supported GPUs only)
        :param verbose: Whether to enable logging from base Huggingface packages
        :param torchscript: Whether the input model is a TorchScript traced model
        :param ts_to_trace: Whether to prep the input model to be exported to TorchScript
        :param bos_token: String to override the beginning-of-string token
        :param eos_token: String to override the end-of-string token
        :param unk_token: String to override the unknown token
        """
        print("Load aitextgen")
        ai = aitextgen(   vocab_file=self.vocab_file,
                            merges_file=self.merges_file,
                            config=self.config)
        print("Done.")
        return ai

    def get_data(self):
        """
        Class that merges TextDataset and LineByLineTextDataset from
        run_language_modeling.py in transformers, plus
        adds more ways to ingest text such as with CSVs.

        :param file_path: A string indicating the relative file path of the text
        to be tokenized, or the cached dataset.
        :param vocab_file: Path to a vocab file (generated by train_tokenizer())
        :param merges_file: Path to a merges file (generated by train_tokenizer())
        :param texts: A list of input texts (if providing texts manually)
        :param line_by_line: A boolean to indicate if the input file should be read
        line by line (True) or as a full text (False).
        :param from_cache: A string indicating if loading from a pregenerated MsgPack
        dump.
        :param header: A boolean indicating if loading from a CSV, if it has a header.
        :param save_cache: A boolean indicating whether to save the tokenized
        dataset as a MsgPack dump to load later.
        :param cache_destination: A string indicating where to save the cache.
        :param block_size: An integer indicating maximum length of the text document
        (usually set by the model architecture)
        :param tokenized_texts: Texts that are already tokenized; only should
        be used by merge_datasets().
        :param text_delim: delimiter to use to split bulk texts (default paragraph breaks)
        :param bos_token: String to override the beginning-of-string token
        :param eos_token: String to override the end-of-string token
        :param unk_token: String to override the unknown token
        :param pad_token: String to override the padding token
        :param progress_bar_refresh_rate: How often to update progress bar when loading
        """

        print("ComputeTokenDataset")
        tk = TokenDataset(  self.file_name,
                            vocab_file=self.vocab_file,
                            merges_file=self.merges_file,
                            block_size=64)  # 64
        print("Done.")
        return tk

    def training(self):
        """
        train_data: Union[str, TokenDataset],
        output_dir: str = "trained_model",
        fp16: bool = False,
        fp16_opt_level: str = "O1",
        n_gpu: int = -1,
        n_tpu_cores: int = 0,
        max_grad_norm: float = 0.5,
        gradient_accumulation_steps: int = 1,
        seed: int = None,
        learning_rate: float = 1e-4,
        weight_decay: float = 0.05,
        adam_epsilon: float = 1e-8,
        warmup_steps: int = 0,
        num_steps: int = 5000,
        save_every: int = 1000,
        generate_every: int = 1000,
        n_generate: int = 1,
        loggers: List = None,
        batch_size: int = 1,
        num_workers: int = None,
        benchmark: bool = True,
        avg_loss_smoothing: float = 0.01,
        save_gdrive: bool = False,
        run_id: str = f"ATG_{datetime.utcnow():%Y%m%d_%H%M%S}",
        progress_bar_refresh_rate: int = 10,
        **kwargs,
    ) -> None:

        Trains/finetunes the model on the provided file/dataset using pytorch-lightning.

        :param train_data: Either a TokenDataset containing the samples to be trained, or
        a string containing the text to be trained (shortcut instead of dataset)
        :param output_dir: A string indicating where to store the resulting
        model file folder.
        :param fp16: Boolean whether to use fp16, assuming using a compatible GPU/TPU.
        :param fp16_opt_level: Option level for FP16/APEX training.
        :param n_gpu: Number of GPU to use (-1 implies all available GPUs)
        :param n_tpu_cores: Number of TPU cores to use (should be a multiple of 8)
        :param max_grad_norm: Maximum gradient normalization
        :param gradient_accumulation_steps: Number of gradient acc steps
        :param seed: Interger representing the training seed.
        :param learning_rate: Training learnign rate for the default AdamW optimizer.
        :param weight_decay: Weight decay for the default AdamW optimizer.
        :param warmup_steps: Warmrup steps for the default AdamW optimizer.
        :param num_steps: Number of samples through the dataset.
        :param save_every: Number of steps for each time to save the model to disk
        :param generate_every: Number of steps for each time to generate sample text
        :param n_generate: Number of texts to generate when generate_every occurs.
        :param loggers: pytorch-lightning logger(s) to log results.
        :param batch_size: Number of input samples per batch
        :param num_workers: Number of DataLoader workers
        :param benchmark: If using GPU, whether to use cudnn.benchmarkl
        :param avg_loss_smoothing: Smoothing factor for Avg loss in progress bar
        :param save_gdrive: If using Colab, whether to save the notebook
        to Google Drive at each save_every
        :param run_id: Run identifier; used for save_gdrive
        :param progress_bar_refresh_rate: How often to update
        the progress bar while training.

        batch_size: Batch size of the model training; setting it too high will cause
        the GPU to go OOM.
        """

        # Génère les fichiers aitextgen-vocab.json et aitextgen-merges.txt
        train_tokenizer(self.file_name, vocab_size=self.vocab_size)
        self.vocab_file = "aitextgen-vocab.json"
        self.merges_file = "aitextgen-merges.txt"

        ai = self.get_aitextgen()
        # #ai.to_fp16()
        data = self.get_data()

        print("Début du training:")
        # #ai.train(data, batch_size=32, num_steps=300000)  # 32
        ai.train(data, batch_size=16, num_steps=1.2e6)



if __name__ == "__main__":

    file_name  =  "./roman_wo_en.txt"
    VOCAB_SIZE = 40000
    t = Training(VOCAB_SIZE, file_name)
    t.training()

"""
TokenDataset:Encoding 125,208 sets of tokens from ./roman_wo_en.txt
debut Loss: 8.002 — Avg: 10.300

"""
