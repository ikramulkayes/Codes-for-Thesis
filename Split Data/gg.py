from urllib.request import urlretrieve
from diagrams import Cluster, Diagram
from diagrams.generic.storage import Storage
from diagrams.custom import Custom
from diagrams.aws.ml import Sagemaker

# Download images to be used for Context and T5 Model nodes
context_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Ffree-vector%2Fbook&psig=AOvVaw3ihK1hOiBB8YlH69_A6Wmd&ust=1737888551587000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCPi8gsHZkIsDFQAAAAAdAAAAABAE"
context_icon = "book_icon.png"
urlretrieve(context_url, context_icon)

t5_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Transformer-model.svg/1200px-Transformer-model.svg.png"
t5_icon = "t5_model.png"
urlretrieve(t5_url, t5_icon)

with Diagram("T5 QA Pipeline", show=False):
    with Cluster("Inputs"):
        # Use the book image for Context
        inputs = [
            Custom("Context", context_icon),
            Storage("Question")
        ]

    t5_model = Custom("T5 Model", t5_icon)

    with Cluster("Outputs"):
        outputs = [
            Sagemaker("Parametric Answer\n(Encoded Knowledge)"),
            Sagemaker("Contextual Answer\n(From Context)")
        ]

    # Flow of data
    inputs >> t5_model >> outputs
