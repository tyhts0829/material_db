#%%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class MaterialDB:
    import_data = pd.read_excel("material_property_data.xlsx",)
    material_data = import_data.set_index(
        ["material", "property", "source", "item"]
    ).sort_index()

    def __init__(self, material):
        self.material = material
        self.young = self.material_data.loc[(self.material, "young_modulus")].dropna(
            how="all", axis=1
        )
        self.poisson = self.material_data.loc[(self.material, "poisson_ratio")].dropna(
            how="all", axis=1
        )
        self.tec = self.material_data.loc[(self.material, "tec")].dropna(
            how="all", axis=1
        )
        self.density = self.material_data.loc[(self.material, "density")].dropna(
            how="all", axis=1
        )

    def show_table(self):
        return print(self.material_data.loc[(self.material)].dropna(how="all", axis=1))

    def calc_young_modulus(self, temp):
        self.k = np.polyfit(
            self.young.values[1], self.young.values[2], self.young.values[0][0]
        )
        self.p = np.poly1d(self.k)
        return round(self.p(temp), 0)

    def calc_tec(self, temp):
        self.k = np.polyfit(
            self.tec.values[1], self.tec.values[2], self.tec.values[0][0]
        )
        self.p = np.poly1d(self.k)
        return round(self.p(temp), 3)

    def calc_poisson_ratio(self, temp):
        self.k = np.polyfit(
            self.poisson.values[1], self.poisson.values[2], self.poisson.values[0][0]
        )
        self.p = np.poly1d(self.k)
        return round(self.p(temp), 3)

    def calc_density(self, temp):
        self.k = np.polyfit(
            self.density.values[1], self.density.values[2], self.density.values[0][0]
        )
        self.p = np.poly1d(self.k)
        return round(self.p(temp), 3)

    def show_graph(self):
        sns.set()
        self.fig = plt.figure(figsize=(12, 3), tight_layout=True)
        self.fig.suptitle(self.material, fontweight="semibold")

        self.k_young = np.polyfit(
            self.young.values[1], self.young.values[2], self.young.values[0][0]
        )
        self.x_young = np.linspace(
            np.min((self.young.values[1])) - 100,
            np.max((self.young.values[1]) + 100),
            2000,
        )
        self.p_young = np.poly1d(self.k_young)
        self.y_young = self.p_young(self.x_young)
        self.ax_young = self.fig.add_subplot(141)
        self.ax_young.scatter(self.young.values[1], self.young.values[2])
        self.ax_young.plot(self.x_young, self.y_young, c="r")
        self.ax_young.set_xlabel("temperature[degC]")
        self.ax_young.set_ylabel("young modulus[MPa]")
        self.ax_young.set_ylim(0)
        self.ax_young.grid(True)

        self.k_poisson = np.polyfit(
            self.poisson.values[1], self.poisson.values[2], self.poisson.values[0][0]
        )
        self.x_poisson = np.linspace(
            np.min((self.poisson.values[1])) - 100,
            np.max((self.poisson.values[1]) + 100),
            2000,
        )
        self.p_poisson = np.poly1d(self.k_poisson)
        self.y_poisson = self.p_poisson(self.x_poisson)
        self.ax_poisson = self.fig.add_subplot(142)
        self.ax_poisson.scatter(self.poisson.values[1], self.poisson.values[2])
        self.ax_poisson.plot(self.x_poisson, self.y_poisson, c="r")
        self.ax_poisson.set_xlabel("temperature[degC]")
        self.ax_poisson.set_ylabel("poisson ratio")
        self.ax_poisson.set_ylim(0)
        self.ax_poisson.grid(True)

        self.k_tec = np.polyfit(
            self.tec.values[1], self.tec.values[2], self.tec.values[0][0]
        )
        self.x_tec = np.linspace(
            np.min((self.tec.values[1])) - 100,
            np.max((self.tec.values[1]) + 100),
            2000,
        )
        self.p_tec = np.poly1d(self.k_tec)
        self.y_tec = self.p_tec(self.x_tec)
        self.ax_tec = self.fig.add_subplot(143)
        self.ax_tec.scatter(self.tec.values[1], self.tec.values[2])
        self.ax_tec.plot(self.x_tec, self.y_tec, c="r")
        self.ax_tec.set_xlabel("temperature[degC]")
        self.ax_tec.set_ylabel("tec[x10**-6]")
        self.ax_tec.set_ylim(0)
        self.ax_tec.grid(True)

        self.k_density = np.polyfit(
            self.density.values[1], self.density.values[2], self.density.values[0][0]
        )
        self.x_density = np.linspace(
            np.min((self.density.values[1])) - 100,
            np.max((self.density.values[1]) + 100),
            2000,
        )
        self.p_density = np.poly1d(self.k_density)
        self.y_density = self.p_density(self.x_density)
        self.ax_density = self.fig.add_subplot(144)
        self.ax_density.scatter(self.density.values[1], self.density.values[2])
        self.ax_density.plot(self.x_density, self.y_density, c="r")
        self.ax_density.set_xlabel("temperature[degC]")
        self.ax_density.set_ylabel("density[g/cm**3]")
        self.ax_density.set_ylim(0)
        self.ax_density.grid(True)

        plt.show()

    @classmethod
    def show_all_graph(cls):  # show_graphメソッドを使っている限り、全材料のグラフを一覧させるのは難しい、、、、
        material_list = list(
            dict.fromkeys(cls.material_data.index.get_level_values("material"))
        )  # indexのmaterialを取得しdect.fromkeysで重複削除してリスト化
        num = list(range(len(material_list)))
        m = []
        for i in range(len(num)):
            m += [i]
            m[i] = MaterialDB(material_list[i])
            m[i].show_graph()


# m1 = MaterialDB("SUJ2")
# print(
#     m1.calc_young_modulus(250),
#     m1.calc_poisson_ratio(250),
#     m1.calc_tec(250),
#     m1.calc_density(250),
# )
# m1.show_table()
# m1.show_graph()
# MaterialDB.show_all_graph()

# %%
