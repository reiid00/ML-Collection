import matplotlib.pyplot as plt

def plot_positional_encodings(encodings, outfile=None):
    plt.figure(figsize=(10, 10))
    plt.imshow(encodings, cmap='viridis', aspect='auto')
    plt.colorbar()
    plt.title("Positional Encodings")
    plt.xlabel("Embedding Dimension")
    plt.ylabel("Token Position")
    if outfile is not None:
        plt.savefig(outfile)
    plt.show()