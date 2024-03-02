import asyncio
import os
import json
import pathlib
import tkinter
import tkinter as tk
import requests

from tkinter import ttk, messagebox

token = os.environ.get('AVRAE-TOKEN')
base_url = "https://api.avrae.io/"
header = {
    "Authorization": token,
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Content-Type": "application/json",
    "Sec-FetchSite": "same-site",
    "Sec-Fetch-Mode": 'cors',
    "Sec-Fetch-Dest": "empty"
}

f = open('Workshop Updater/mapping.json')
mappings = json.load(f)

class MainWindow(tk.Tk):
    def __init__(self, width, height, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry(self.CenterWindowtoDisplay(width, height))
        self.maxsize(width, height)
        self.minsize(width, height)
        self.title("Avrae Update Pusher")

        container = tk.Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.pack(side='top', fill='both', expand=True)
        self.frames = {}
        for F in (MainMenu, CollectionMenu):
            page_name = F.__name__
            frame = F(master=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def CenterWindowtoDisplay(self, width, height):
        """Centers the window to the main display/monitor"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 1.5))
        return f"{width}x{height}+{x}+{y}"

class MainMenu(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.gvar = tk.StringVar(self)


        # GVARs
        tk.Label(self, text="GVARs", justify="left").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Combobox(self, values=sorted([x['name'] for x in mappings.get('gvars', []) if x['name'] != "" and x['file'] != ""]),
                     textvariable=self.gvar, width=30).grid(row=0, column=1, columnspan=2, sticky='w', padx=5, pady=5)

        tk.Button(self, text="Update", command=self.update_gvar, width=10)\
            .grid(row=1, column=0, sticky='s', pady=10, padx=5)
        tk.Button(self, text="Modify Collection",
                  command=lambda: controller.show_frame("CollectionMenu"), width=20)\
            .grid(row=1, column=1, columnspan=3, sticky='s', pady=10, padx=5)

    def update_gvar(self):
        if self.gvar.get():
            data = next((x for x in mappings['gvars'] if x['name'] == self.gvar.get()), None)
            if messagebox.askyesno(title="Update GVAR", message=f"Update {self.gvar.get()}?"):
                payload = get_file_content(data['file'])
                if len(payload) > 100000:
                    messagebox.showerror(title="Error", message="GVARs are limited to 100k characters.")

                gvar = self._get_gvar(data['gvar'])
                gvar['value'] = payload

                self._put_gvar(gvar)

    def _get_gvar(self, gvar_id):
        result = requests.get(f"{base_url}customizations/gvars/{gvar_id}", headers=header)

        if result.status_code != 200:
            return messagebox.showerror(title="Error getting GVAR", message=f"Error f{result.status_code}\n"
                                                                     f"Cannot get information for GVAR: {gvar_id}")

        return json.loads(result.text)

    def _put_gvar(self, gvar):
        result = requests.post(f"{base_url}customizations/gvars/{gvar['key']}", headers=header, json=gvar)

        if result.status_code != 200:
            return messagebox.showerror(title="Error updating GVAR", message=f"Error updating GVAR.\n"
                                                                             f" Error: {result.status_code}")
        return messagebox.showinfo(title="GVAR Updated", message=f"Successfully updated {gvar['key']}")

class CollectionMenu(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.alias = tk.StringVar(self)
        self.snippet = tk.StringVar(self)

        # Aliases
        tk.Label(self, text="Aliases", justify="left").grid(sticky='w', row=0, column=0, padx=5, pady=5)
        alias_combo = ttk.Combobox(self, values=self._get_list_options(mappings.get('collection', {}).get('aliases', [])),
                                   width=30,
                                   textvariable=self.alias,
                                   name="alias_combo")
        alias_combo.bind("<<ComboboxSelected>>", self.on_combobox_change)
        alias_combo.grid(row=0, sticky='w', column=1, columnspan=2, pady=5, padx=5)

        # Snippets
        tk.Label(self, text="Snippets", justify="left").grid(sticky='w', row=1, column=0, padx=5, pady=5)
        snippet_combo = ttk.Combobox(self, values=self._get_list_options(mappings.get('collection', {}).get('snippets', [])),
                                     width=30,
                                     textvariable=self.snippet,
                                     name="snippet_combo")
        snippet_combo.grid(row=1, sticky='w', column=1, columnspan=2, pady=5, padx=5)
        snippet_combo.bind("<<ComboboxSelected>>", self.on_combobox_change)
        snippet_combo.winfo_name()



        tk.Button(self, text="Update Description", width=20,
                  command=self.update_object_description).grid(row=3, column=1, sticky='w', pady=10, padx=5)
        tk.Button(self, text="Update Code", width=20,
                  command=self.update_object_code).grid(row=3, column=2, sticky='w', pady=10, padx=5)
        if mappings['collection']['desc'] != "":
            tk.Button(self, text="Update Collection Description", width=25)\
                .grid(row=3, column=0, sticky='w', pady=10, padx=5)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("MainMenu"), width=10) \
            .grid(row=4, column=0, sticky='w', padx=5, pady=10)

    def _get_list_options(self, node, parent=None):
        out = []
        for x in node:
            if x['file'] != "":
                out.append(f"{f'{parent} ' if parent else ''}{x['name']}")

            if 'subcommands' in x and  len(x['subcommands']) > 0:
                out += (self._get_list_options(x['subcommands'], x['name']))
        return out

    def _get_list_object(self, node: [], parts: []):
        for x in parts:
            for alias in node:
                if alias['name'] == x:
                    print(f"{len(parts)}\n\n{parts.index(x)+1}")
                    if  len(parts) == parts.index(x)+1:
                        return alias
                    elif 'subcommands' in alias:
                        return self._get_list_object(alias['subcommands'], parts[parts.index(x) + 1:])

    def _update_alias_information(self, alias_id, data):
        result = requests.patch(f"{base_url}workshop/alias/{alias_id}", headers=header, json=data)

        if result.status_code != 200:
            return messagebox.showerror(title="Error updating Alias", message=f"Error updating Alias.\n"
                                                                             f" Error: {result.status_code}")
        return messagebox.showinfo(title="Alias Updated", message=f"Successfully updated {data['name']}")

    def _update_snippet_information(self, snippet_id, data):
        result = requests.patch(f"{base_url}workshop/snippet/{snippet_id}", headers=header, json=data)

        if result.status_code != 200:
            return messagebox.showerror(title="Error updating Snippet", message=f"Error updating Snippet.\n"
                                                                             f" Error: {result.status_code}")
        return messagebox.showinfo(title="Snippet Updated", message=f"Successfully updated {data['name']}")

    def _update_alias_code(self, alias_id, data):
        result = requests.post(f"{base_url}workshop/alias/{alias_id}/code", headers=header, json={"content": data})

        if result.status_code != 201:
            return messagebox.showerror(title="Error updating Alias", message=f"Error updating Alias.\n"
                                                                             f" Error: {result.status_code}")

        return json.loads(result.text)

    def _activate_alias_code(self,alias_data, alias_info):
        data = {"version": alias_info['data']['version']}
        result = requests.put(f"{base_url}workshop/alias/{alias_data['id']}/active-code", headers=header, json=data)
        if result.status_code != 200:
            return messagebox.showerror(title="Error updating Alias", message=f"Error updating Alias.\n"
                                                                              f" Error: {result.status_code}")

        return messagebox.showinfo(title="Alias Updated", message=f"Successfully updated {self.alias.get()}")



    def on_combobox_change(self, event: tkinter.Event):
        if self.snippet and event.widget.winfo_name() == "alias_combo":
            self.children.get('snippet_combo').delete(0, "end")
        elif self.alias and event.widget.winfo_name() == "snippet_combo":
            self.children.get('alias_combo').delete(0, "end")

    def update_object_description(self):
        if self.alias.get():
            p = self.alias.get().split()
            alias = self._get_list_object(mappings['collection']['aliases'], p)
            if alias['desc'] == "":
                return messagebox.showerror(title="Error", message=f"No description file set for {self.alias.get()}")
            elif not messagebox.askyesno(title="Update Alias", message=f"Update {self.alias.get()}?"):
                return
            payload = get_file_content(alias['desc'])
            data = {"name": alias['name'], "docs": payload}
            self._update_alias_information(alias['id'], data)
        elif self.snippet.get():
            snippet = self._get_list_object(mappings['collection']['snippets'], self.snippet.get().split())
            if snippet['desc'] =="":
                return messagebox.showerror(title="Error", message=f"No description file set for {self.snippet.get()}")
            elif not messagebox.askyesno(title="Update Snippet", message=f"Update {self.snippet.get()}?"):
                return

    def update_object_code(self):
        if self.alias.get():
            p = self.alias.get().split()
            alias = self._get_list_object(mappings['collection']['aliases'], p)
            if alias['file'] =="":
                return messagebox.showerror(title="Error", message=f"No code file set for {self.alias.get()}")
            elif not messagebox.askyesno(title="Update Alias", message=f"Update {self.alias.get()}?"):
                return
            payload = get_file_content(alias['file'])
            out = self._update_alias_code(alias['id'], payload)
            self._activate_alias_code(alias, out)



def get_file_content(content):
    f = open(content, 'r', encoding='utf-8')

    if pathlib.Path(content).suffix == '.json':
        file_content = json.load(f)
        if type(file_content) is list:
            payload = json.dumps(flatten_json(file_content)[''], ensure_ascii=False)
        else:
            payload = json.dumps(flatten_json(file_content), ensure_ascii=False)
    else:
        payload = ''.join(f.readlines())
    return payload
def flatten_json(nested_json):
   flattened_json = {}

   def flatten(x, name=''):
      if type(x) is dict:
         for a in x:
            flatten(x[a], name + a + '_')
      else:
         flattened_json[name[:-1]] = x

   flatten(nested_json)
   return flattened_json

def load_collection(collection_id):
    out = {}

    response = requests.get(f"{base_url}workshop/collection/63e066ecd6596a5e18f1604f", headers=header)

    if response.status_code != 200:
        print("error")
        return
    else:
        collection = json.loads(response.text)
    alias_ids = collection['data']['alias_ids']
    snippet_ids = collection['data']['snippet_ids']
    aliases = get_aliases(alias_ids)
    snippets = get_snippets(snippet_ids)
    out = {"name": collection['data']['name'],
           "aliases": aliases, "snippets": snippets, "desc": "", "image": collection['data']['image']}
    return out

def load_gvars():
    response = requests.get(f"{base_url}customizations/gvars", headers=header)
    gvars = json.loads(response.text)
    all_gvars = []
    out = []
    for gvar in gvars['owned']:
        all_gvars.append({"name": "", "file": "", "gvar": f"{gvar['key']}"})

    existing_list = mappings.get('gvars', [])

    for x in all_gvars:
        if x.get('gvar', '') not in [x.get('gvar','') for x in existing_list]:
            existing_list.append(x)

    return json.dumps(existing_list)



def get_aliases(aliases: []):
    out = []
    for alias in aliases:
        response = requests.get(f'{base_url}workshop/alias/{alias}', headers=header)
        if response.status_code != 200:
            continue
        else:
            alias_data = json.loads(response.text)
            alias_obj={"name": alias_data['data']['name'], "subcommands": [],
                       "id": alias, "file": "", "desc": ""}
            if len(alias_data['data']['subcommand_ids'])>0:
                alias_obj['subcommands'] = get_aliases(alias_data['data']['subcommand_ids'])
            out.append(alias_obj)

    return out

def get_snippets(snippets: []):
    out = []
    for snippet in snippets:
        response = requests.get(f'{base_url}workshop/snippet/{snippet}', headers=header)
        if response.status_code != 200:
            continue
        else:
            snippet_data = json.loads(response.text)
            out.append({"name": snippet_data['data']['name'],
                        "id": snippet, "file": "", "desc": ""})

    return out

# test = load_collection('63e066ecd6596a5e18f1604f')
test = requests.get(f"{base_url}homebrew/spells/60f243f60dc83c7c1d3a37cc", headers=header)
data = json.dumps(json.loads(test.text)['data'])
here = 1

if __name__ == "__main__":
    app = MainWindow(600, 200)
    app.mainloop()
