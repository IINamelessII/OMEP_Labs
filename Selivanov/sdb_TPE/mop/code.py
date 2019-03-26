from _pydecimal import Decimal, ROUND_UP, ROUND_FLOOR

# import numpy as np

from scipy.stats import f, t, ttest_ind, norm
import tkinter as tk
from tkinter import messagebox

class Criteries:
    @staticmethod
    def get_cohren_value(size_of_selections,qty_of_selections, significance ):
        #qty_of_selections = 4
        #size_of_selections = 4
        size_of_selections += 1

      #  significance = 0.05

        partResult1 = significance/(size_of_selections-1)
        params = [partResult1, qty_of_selections, (size_of_selections-1-1)*qty_of_selections]
        fisher = f.isf(*params)
        print(fisher)
        # fisher = 0
        result = fisher/(fisher+(size_of_selections-1-1))
        return Decimal(result).quantize(Decimal('.0001')).__float__()

    @staticmethod
    def get_student_value(f3,significance):
        return Decimal(abs(t.ppf(significance/2,f3))).quantize(Decimal('.0001')).__float__()

    @staticmethod
    def get_fisher_value(f3,f4,significance):
        return Decimal(abs(f.isf(significance,f4,f3))).quantize(Decimal('.0001')).__float__()

class myGUI:
    def __init__(self, master):
        self.master = master
        self.qty_of_result = 0
        master.title("Gкр")

        # centring master window
        windowWidth = master.winfo_reqwidth()
        windowHeight = master.winfo_reqheight()
        positionRight = int(master.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(master.winfo_screenheight() / 2 - windowHeight / 2)
        master.geometry("+{}+{}".format(positionRight, positionDown))
        # centring end

        self.labelstart = tk.Label(master, text="Програма для обчислення Gкр, Tкр, Fкр")
        self.label1 = tk.Label(master, text="Введіть рівень значущості")
        self.e1 = tk.Entry(master)
        self.e1.insert(0, "0.05")
        self.label2 = tk.Label(master, text="Введіть кількість ступенів вільності f1 (m-1)")
        self.e2 = tk.Entry(master)
        self.e2.insert(0, "4")
        self.label3 = tk.Label(master, text="Введіть кількість ступенів вільності f2 (N)")
        self.e3 = tk.Entry(master)
        self.e3.insert(0, "4")
        self.label4 = tk.Label(master, text="Введіть кількість значущіх коеф. d (f4 = N - d)")
        self.e4 = tk.Entry(master)
        self.e4.insert(0, "2")
        for i in [self.labelstart,self.label1,self.e1,self.label2,self.e2,self.label3,self.e3,self.label4,self.e4]:
            i.pack()
        self.run = tk.Button(master, text="Обчислити", command=self.func_run)
        self.run.pack()


    def center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def func_run(self):
        try:
            q = float(self.e1.get())
            d = int(self.e4.get())
            f1 = int(self.e2.get())
            f2 = int(self.e3.get())
            if f2 < d or (q<0 or q>1):
                raise ArithmeticError()

            f3 = f1*f2
            f4 = f2 - d
            new_result = tk.Toplevel(self.master)
            new_result.title("Результат #" + str(self.qty_of_result))
            params = [tk.Label(new_result, text="q = " + str(q)),
                      tk.Label(new_result, text="f1 = "+ str(f1)),
                      tk.Label(new_result, text="f2 = "+ str(f2)),
                      tk.Label(new_result, text="f3 = f1*f2 = "+ str(f3)),
                      tk.Label(new_result, text="Gкр = "+str(Criteries.get_cohren_value(f2,f1,q))),
                      tk.Label(new_result, text="Tкр = "+str(Criteries.get_student_value(f3,q))),
                      tk.Label(new_result, text="Fкр = "+str(Criteries.get_fisher_value(f3,f4,q)))
                      ]
            for i in params:
                i.pack()
            new_result.geometry("300x150+0+"+str(100*self.qty_of_result))
            self.qty_of_result += 1
        except ArithmeticError:
            messagebox.showerror("Помилка", "0>q>1 or N<d")
        except:
            messagebox.showerror("Помилка", "Введіть дані корректно. q - float, f1 - int, f2 - int, d - int")


root = tk.Tk()
my_gui = myGUI(root)
root.mainloop()
# input("enter:")

# print(round(Criteries.get_cohren_value(12,9,0.05),4))

# ===== small cohren table
# cohren_table = []
# znachimost = 0.01
# for i in range(2, 10):
#     row = []
#     for j in range(1,10):
#         row.append(Criteries.get_cohren_value(i,j,znachimost))
#     cohren_table.append(row)
#
# cohren_table = np.array(cohren_table)
# print(cohren_table)

# print(round(Criteries.get_fisher_value(16,2,0.05),5))
