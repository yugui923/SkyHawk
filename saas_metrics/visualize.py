import matplotlib.pyplot as plt
import seaborn as sns


def heatmap(df):
    sns.set_theme()

    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 5))  # setup window
    sns.heatmap(df.T, center=0, cmap="PiYG", annot=True, fmt=',.0f', linewidths=.5)  # plot heatmap
    plt.gcf().subplots_adjust(left=0.2)  # add left padding

    return
