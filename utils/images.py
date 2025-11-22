# utils/images.py
import io
import matplotlib.pyplot as plt

def plot_values(ys, title=None):
    buf = io.BytesIO()
    plt.figure(figsize=(8,4))
    plt.plot(ys)
    if title:
        plt.title(title)
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf
