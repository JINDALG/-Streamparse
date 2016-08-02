import Tkinter
import tkFileDialog
import os
area_value=None
time_value=None
path=None

def select(dirLabel,top):
	global path
	currdir = os.getcwd()
	path = tkFileDialog.askdirectory(parent=top, initialdir=currdir, title='Please select a directory')
	dirLabel.config(text=path)
	dirLabel.update_idletasks()

def submitFun(area,time,top):
	global area_value,time_value
	area_value = int(area.get())
	time_value = int(time.get())
	top.destroy()


def GUI():
	top = Tkinter.Tk()
	top.title("StreamParse")
	top.geometry("600x400")


	row = Tkinter.Frame(top)
	l1 = Tkinter.Label(row, text = 'Minimum Area', anchor = 'w', width=15)
	l1.pack(side = Tkinter.LEFT, pady=10)
	area = Tkinter.Entry(row, bd=5)
	area.pack(side = Tkinter.RIGHT, expand=Tkinter.YES,pady=10)
	row.pack(side = Tkinter.TOP)

	row = Tkinter.Frame(top)
	l1 = Tkinter.Label(row, text = 'Time Differnce Between snapshot', anchor = 'w', width=50)
	l1.pack(side = Tkinter.TOP)
	time = Tkinter.Scale(row, from_ = 0, to = 150, tickinterval = 10, orient = Tkinter.HORIZONTAL, length = 600)
	time.set(30)
	time.pack()
	row.pack(pady=20)

	row = Tkinter.Frame(top)
	dirLabel = Tkinter.Label(row, anchor = 'w', width=50,font=("Helvetica", 15))
	dirLabel.pack(side = Tkinter.TOP)
	row.pack(pady=20)

	row = Tkinter.Frame(top)
	browse  =Tkinter.Button(row, text='Upload', command = lambda: select(dirLabel,top))
	browse.pack()
	row.pack(pady = 30)



	# top.bind('<Return>', (lambda event, e=ents: self.fetch(e)))   
	submit = Tkinter.Button(top, text="Start Motion Detection", command = lambda :submitFun(area,time,top))
	submit.pack(pady=20)

	top.mainloop()

	return path, area_value, time_value



print GUI()