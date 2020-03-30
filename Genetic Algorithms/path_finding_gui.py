import tkinter as tk
import threading
from os import system
import networkzero as nw0

root = tk.Tk()

left = tk.Frame(root)
left.grid(row=0, column=0, sticky=tk.N)

sizes = tk.LabelFrame(left, text="Sizes")
sizes.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

tk.Label(sizes, text="Width of window:").grid(row=0, column=0)
width = tk.Entry(sizes)
width.grid(row=0, column=1, padx=2, pady=2)
width.insert(0, "400")

tk.Label(sizes, text="Height of window:").grid(row=1, column=0)
height = tk.Entry(sizes)
height.grid(row=1, column=1, padx=2, pady=2)
height.insert(0, "300")

tk.Label(sizes, text="Size of sprites:").grid(row=2, column=0)
sprites = tk.Entry(sizes)
sprites.grid(row=2, column=1, padx=2, pady=2)
sprites.insert(0, "16")

misc = tk.LabelFrame(left, text="Miscellaneous")
misc.grid(row=1, column=0, padx=2, pady=2)

tk.Label(misc, text="Frames per second:").grid(row=0, column=0)
fps = tk.Entry(misc)
fps.grid(row=0, column=1, padx=2, pady=2)
fps.insert(0, "50")

state = tk.IntVar()

show = tk.Checkbutton(misc, text="Show output in console?", variable=state, onvalue=1, offvalue=0)
show.grid(row=1, column=0, padx=2, pady=2, columnspan=2)

name = 1

tk.Label(misc, text="Name to broadcast:").grid(row=2, column=0)
broadcasting = tk.Entry(misc)
broadcasting.grid(row=2, column=1, padx=2, pady=2)
broadcasting.insert(0, "path_finding_"+str(name))

right = tk.Frame(root)
right.grid(row=0, column=1, sticky=tk.N)

settings = tk.LabelFrame(right, text="Genetic Algorithm Settings")
settings.grid(row=0, column=1, padx=2, pady=2, sticky=tk.N)

tk.Label(settings, text="Generations per run:").grid(row=0, column=0)
generations = tk.Entry(settings)
generations.grid(row=0, column=1, padx=2, pady=2)
generations.insert(0, "100")

tk.Label(settings, text="Population per generation:").grid(row=1, column=0)
population = tk.Entry(settings)
population.grid(row=1, column=1, padx=2, pady=2)
population.insert(0, "100")

tk.Label(settings, text="Length of DNA:").grid(row=2, column=0)
length = tk.Entry(settings)
length.grid(row=2, column=1, padx=2, pady=2)
length.insert(0, "250")

tk.Label(settings, text="Mutation rate (out of 1):").grid(row=3, column=0)
rate = tk.Entry(settings)
rate.grid(row=3, column=1, padx=2, pady=2)
rate.insert(0, "0.1")


def run_ga():
    command = "python path_finding.py "
    command += width.get()
    command += " "
    command += height.get()
    command += " "
    command += sprites.get()
    command += " "
    command += fps.get()
    command += " "
    command += generations.get()
    command += " "
    command += population.get()
    command += " "
    command += length.get()
    command += " "
    command += rate.get()
    command += " "
    command += broadcasting.get()
    command += " "
    command += str(state.get())
    system(command)


def run():
    global name
    name += 1
    broadcasting.delete(0, tk.END)
    broadcasting.insert(0, "path_finding_" + str(name))
    threads = threading.Thread(target=run_ga)
    threads.start()


tk.Button(right, text="Run", width=38, height=4, command=run).grid(row=1, column=1, padx=2, pady=2)

console = tk.LabelFrame(root, text="Stats from last ran program")
console.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=tk.W)

tk.Label(console, text="Generation:").grid(row=0, column=0, padx=2, pady=2)
genvar = tk.StringVar()
genvar.set("None")
tk.Label(console, textvariable=genvar).grid(row=0, column=1, padx=2, pady=2)
tk.Label(console, text="Iteration:").grid(row=1, column=0, padx=2, pady=2)
itervar = tk.StringVar()
itervar.set("None")
tk.Label(console, textvariable=itervar).grid(row=1, column=1, padx=2, pady=2)
tk.Label(console, text="Best distance last generation:").grid(row=2, column=0, padx=2, pady=2)
bdlgvar = tk.StringVar()
bdlgvar.set("None")
tk.Label(console, textvariable=bdlgvar).grid(row=2, column=1, padx=2, pady=2)
tk.Label(console, text="Best distance this generation:").grid(row=3, column=0, padx=2, pady=2)
bdtgvar = tk.StringVar()
bdtgvar.set("None")
tk.Label(console, textvariable=bdtgvar).grid(row=3, column=1, padx=2, pady=2)
tk.Label(console, text="DNA mutation count:").grid(row=0, column=2, padx=2, pady=2)
dmvar = tk.StringVar()
dmvar.set("None")
tk.Label(console, textvariable=dmvar).grid(row=0, column=3, padx=2, pady=2)
tk.Label(console, text="Dead:").grid(row=1, column=2, padx=2, pady=2)
deadvar = tk.StringVar()
deadvar.set("None")
tk.Label(console, textvariable=deadvar).grid(row=1, column=3, padx=2, pady=2)
tk.Label(console, text="Paused:").grid(row=2, column=2, padx=2, pady=2)
pvar = tk.StringVar()
pvar.set("False")
tk.Label(console, textvariable=pvar).grid(row=2, column=3, padx=2, pady=2)

stop = False


def network_manager():
    address = nw0.advertise("GeneticAlgorithmsPathFindingGUIConsole")
    while True:
        message = nw0.wait_for_message_from(address, autoreply=True)
        genvar.set(message["generation"])
        itervar.set(message["iteration"])
        bdlgvar.set(message["bestlastgen"]+" ("+message["bestlastgenper"]+"% left)")
        bdtgvar.set(message["bestthisgen"]+" ("+message["bestthisgenper"]+"% left)")
        dmvar.set(message["dnamutcount"])
        deadvar.set(message["dead"]+" ("+message["deadper"]+"% of population)")
        pvar.set(str(message["paused"]))
        if stop:
            break


netman = threading.Thread(target=network_manager)
netman.start()

root.title("Genetic Algorithms: Path Finding GUI")
root.mainloop()
stop = True
