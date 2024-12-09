import matplotlib.pyplot as plt


class Plotter:
    """
    Class that defines plot objects used to visualize \n
    the results of the machine learning model.
    """

    def __init__(self, name, val1, val1_legend, x_label, val2, val2_legend, y_label):
        self.name = name
        self.val1 = val1
        self.val1_legend = val1_legend
        self.x_label = x_label
        self.val2 = val2
        self.val2_legend = val2_legend
        self.y_label = y_label

    def __str__(self):
        return f"Plot of: {self.name}"

    def make_plot(self):

        plt.plot(self.val1, label=self.val1_legend)
        plt.plot(self.val2, label=self.val2_legend)
        plt.title(self.name)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.legend()
        plt.show()
