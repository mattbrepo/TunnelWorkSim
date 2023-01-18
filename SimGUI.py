import tkinter
import customtkinter
import TunnelWorkSim

SIMULATION_TIME = 24 * 10 # 10 days of simulation time 

# -- Global
root = customtkinter.CTk()
slider_num_workers_value = tkinter.IntVar()
slider_num_workers_value.set(10)
slider_num_slots_value = tkinter.IntVar()
slider_num_slots_value.set(7)
avg_session_time_value = tkinter.DoubleVar()
avg_session_time_value.set(1)
avg_resting_time_value = tkinter.DoubleVar()
avg_resting_time_value.set(0.25)
slider_max_sessions_value = tkinter.IntVar()
slider_max_sessions_value.set(7)
long_resting_time_value = tkinter.IntVar()
long_resting_time_value.set(14)

man_hours_worked_value = tkinter.IntVar()
man_hours_worked_value.set(0)

# -- Functions
def add_slider_control(root, y, name, value, min, max):
  label = customtkinter.CTkLabel(master=root, text=name)
  label.place(relx=0.2, rely=y, anchor=tkinter.CENTER)
  slider = customtkinter.CTkSlider(master=root, from_=min, to=max, variable=value)
  slider.place(relx=0.5, rely=y, anchor=tkinter.CENTER)
  labelVal = customtkinter.CTkLabel(master=root, textvariable=value)
  labelVal.place(relx=0.8, rely=y, anchor=tkinter.CENTER)

def num_workers_slider_event(value):
  #global num_workers
  #num_workers = round(value, 0)
  #print(num_workers)
  #return num_workers
  pass

def button_event():
  man_hours_worked = TunnelWorkSim.simpy_simulation(SIMULATION_TIME, slider_num_slots_value.get(), slider_num_workers_value.get(), avg_session_time_value.get(), 
                                                    slider_max_sessions_value.get(), long_resting_time_value.get(), avg_resting_time_value.get())
  man_hours_worked_value.set(round(man_hours_worked, 0))

# -- GUI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root.geometry("800x500")
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# input sliders
add_slider_control(root, 0.1, "Number of workers", slider_num_workers_value, 5, 100)
add_slider_control(root, 0.2, "Number of working slots", slider_num_slots_value, 1, 20)
add_slider_control(root, 0.3, "Average working session time (hr)", avg_session_time_value, 0.5, 4)
add_slider_control(root, 0.4, "Average resting time (hr)", avg_resting_time_value, 0.25, 1)
add_slider_control(root, 0.5, "Maximum working sessions", slider_max_sessions_value, 4, 10)
add_slider_control(root, 0.6, "Long resting time (hr)", long_resting_time_value, 5, 20)

# result label
label = customtkinter.CTkLabel(master=root, text="Simulation hours: " + str(SIMULATION_TIME) + ", man-hours worked: ")
label.place(relx=0.2, rely=0.8, anchor=tkinter.CENTER)
labelVal = customtkinter.CTkLabel(master=root, textvariable=man_hours_worked_value)
labelVal.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

# start button
button = customtkinter.CTkButton(master=root, text="Start", command=button_event)
button.pack(padx=20, pady=10)

root.mainloop()