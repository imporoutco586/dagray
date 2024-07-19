# import tkinter as tk
# import __init__
# from __init__ import defs
# class DefinitionsUI:
#     def __init__(self, definitions):
#         self.definitions = definitions
        
#         self.root = tk.Tk()
#         self.root.title("Definitions")
        
#         self.assets_label = tk.Label(self.root, text="Assets:")
#         self.assets_label.pack()
        
#         self.assets_text = tk.Text(self.root)
#         self.assets_text.pack()
        
#         self.schedules_label = tk.Label(self.root, text="Schedules:")
#         self.schedules_label.pack()
        
#         self.schedules_text = tk.Text(self.root)
#         self.schedules_text.pack()
        
#         self.sensors_label = tk.Label(self.root, text="Sensors:")
#         self.sensors_label.pack()
        
#         self.sensors_text = tk.Text(self.root)
#         self.sensors_text.pack()
        
#         self.jobs_label = tk.Label(self.root, text="Jobs:")
#         self.jobs_label.pack()
        
#         self.jobs_text = tk.Text(self.root)
#         self.jobs_text.pack()
        
#         self.resources_label = tk.Label(self.root, text="Resources:")
#         self.resources_label.pack()
        
#         self.resources_text = tk.Text(self.root)
#         self.resources_text.pack()
        
#         self.asset_checks_label = tk.Label(self.root, text="Asset Checks:")
#         self.asset_checks_label.pack()
        
#         self.asset_checks_text = tk.Text(self.root)
#         self.asset_checks_text.pack()
        
#         self.update_ui()
        
#     def update_ui(self):
#         assets = "\n".join([str(asset) for asset in self.definitions.assets])
#         self.assets_text.delete(1.0, tk.END)
#         self.assets_text.insert(tk.END, assets)
        
#         schedules = "\n".join([str(schedule) for schedule in self.definitions.schedules])
#         self.schedules_text.delete(1.0, tk.END)
#         self.schedules_text.insert(tk.END, schedules)
        
#         sensors = "\n".join([str(sensor) for sensor in self.definitions.sensors])
#         self.sensors_text.delete(1.0, tk.END)
#         self.sensors_text.insert(tk.END, sensors)
        
#         jobs = "\n".join([str(job) for job in self.definitions.jobs])
#         self.jobs_text.delete(1.0, tk.END)
#         self.jobs_text.insert(tk.END, jobs)
        
#         resources = "\n".join([f"{key}: {value}" for key, value in self.definitions.resources.items()])
#         self.resources_text.delete(1.0, tk.END)
#         self.resources_text.insert(tk.END, resources)
        
#         asset_checks = "\n".join([str(check) for check in self.definitions.asset_checks])
#         self.asset_checks_text.delete(1.0, tk.END)
#         self.asset_checks_text.insert(tk.END, asset_checks)
        
#         self.root.after(1000, self.update_ui)
        
#     def start(self):
#         self.root.mainloop()

# # 使用示例
# defs_ui = DefinitionsUI(defs)
# defs_ui.start()
