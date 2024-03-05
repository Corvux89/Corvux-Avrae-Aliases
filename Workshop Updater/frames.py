import tkinter as tk
from tkinter import filedialog, ttk
from utils import *


ioFileTypes = [('QuickMenu Files', '*.io'), ('All Files', '*.*')]
gvarFileTypes = [('GVAR Files', '*.gvar'), ('All Files', '*.*')]
jsonFileTypes = [('JSON Files', '*.json'), ('All Files', '*.*')]
aliasFileTypes = [('Alias Files', '*.alias'), ('All Files', '*.*')]
snippetFileTypes = [('Snippet Files', '*.snippet'), ('All Files', '*.*')]

class QuickMenu(tk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.is_topmost = False
        self.current_file = os.path.basename(sys.argv[1])
        self.ext = os.path.splitext(self.current_file)[1]
        self.name = os.path.splitext(self.current_file)[0]

        tk.Button(self, text="1. Push Update", command=self.push_update)\
            .grid(row=0, column=0, pady=10, padx=5)
        self.bind_all('1', self.push_update)

        tk.Button(self, text="2. Pull Update", command=self.pull_update)\
            .grid(row=0, column=1, pady=10, padx=5)
        self.bind_all('2', self.pull_update)

        tk.Button(self, text="3. Pull Description", command=self.pull_description)\
            .grid(row=0, column=2, pady=10, padx=5)
        self.bind_all('3', self.pull_description)

        tk.Button(self, text="Pull Alias",
                  command=lambda: controller.show_frame("AliasSelect")).grid(row=1, column=0, pady=10, padx=5, sticky="w")

        tk.Button(self, text="Pull Snippet", command=lambda: controller.show_frame("SnippetSelect"))\
            .grid(row=1, column=1, pady=10, padx=5, sticky="w")

        tk.Button(self, text="Main Menu", command=lambda: controller.show_frame("SettingsMenu"))\
            .grid(row=2, column=0, padx=5, pady=10, columnspan=2, sticky="w")

    def pull_description(self, *args):
        if not self.is_topmost:
            return
        elif self.ext.lower() == '.alias':
            alias_id = self.controller.collection.get('aliases', {}).get(self.name, "")
            get = AvraeRest("GET", f"workshop/alias/{alias_id}")
            alias_data = json.loads(get.text)['data']
            with open(os.path.join(os.path.dirname(sys.argv[1]), f"{self.name}.md"), mode="w+", encoding="utf-8") as outfile:
                outfile.write("".join(alias_data['docs']).replace('\r',''))
            messagebox.showinfo(title="Alias Document Saved", message=f"Alias Documentation Sucessfully saved!")
            self.controller.destroy()
        else:
            messagebox.showerror(title="Error", message="This probably doesn't have a description")

    def pull_update(self, *args):
        if not self.is_topmost:
            return
        if self.ext.lower() == '.alias':
            print("alias")
        elif self.ext.lower() == '.snippet':
            print("snippet")
        elif self.ext.lower() == '.md':
            print('readme stuff')
        elif self.ext.lower() in ['.json', '.gvar']:
            if gvar_id := UUID_PATTERN.search(self.name):
                get = AvraeRest("GET", f"/customizations/gvars/{gvar_id.group(0)}")
                if get.status_code in [200, 201]:
                    gvar = json.loads(get.text)
                    with open(sys.argv[1], mode="w+", encoding="utf-8") as outfile:
                        outfile.write(gvar['value'])
                    messagebox.showinfo(title="GVAR Loaded", message=f"Successfully loaded GVAR: {gvar_id.group(0)}")
                else:
                    messagebox.showerror(title="Error", message=f"Error getting GVAR")
            else:
                messagebox.showerror(title="Error", message=f"Invalid GVAR ID")
        else:
            messagebox.showerror(title="Error", message="Invalid file type to update")

        self.controller.destroy()

    def push_update(self, *args):
        if not self.is_topmost:
            return

        if self.ext.lower() == '.alias':
            if alias_id := self.controller.collection.get('aliases', {}).get(self.name, None):
                data = getFileContent(sys.argv[1])
                if len(data) > 100000:
                    messagebox.showerror(title="Error", message="Aliases are limited to 100k characters")
                self._updateCollectionContent("alias", "code", alias_id, {"content": data})
            else:
                messagebox.showerror(title="Error", message="Invalid Alias")

        elif self.ext.lower() == '.snippet':
            if snippet_id := self.controller.collection.get('snippets', {}).get(self.name, None):
                data = getFileContent(sys.argv[1])
                if len(data)>100000:
                    messagebox.showerror(title="Error", message="Snippets are limited to 100k characters")
                self._updateCollectionContent("snippet", "code", snippet_id, {"content": data})
            else:
                messagebox.showerror(title="Error", message="Invalid Snippet")

        elif self.ext.lower() == '.md':
            if alias_id := self.controller.collection.get('aliases', {}).get(self.name, None):
                data = getFileContent(sys.argv[1])
                name = self.name.split()[-1]
                self._updateCollectionContent("alias", "docs", alias_id, {"name": name, "docs": data})
            elif snippet_id := self.controller.collection.get('snippets', {}).get(self.name, None):
                data = getFileContent(sys.argv[1])
                name = self.name.split()[-1]
                self._updateCollectionContent("snippet", "docs", snippet_id, {"name": name, "docs": data})
            elif self.name == "readme":
                get = AvraeRest("GET", f"workshop/collection/{self.controller.collection.get('collection','')}/full")
                data = getFileContent(sys.argv[1])
                if get.status_code in [200, 201]:
                    collection_data = json.loads(get.text)['data']
                    patch = AvraeRest("PATCH", f"workshop/collection/{self.controller.collection.get('collection', '')}",
                                      {"name": collection_data['name'],
                                       "description": data,
                                       "image": collection_data['image']},
                                      )
                    if patch.status_code in [200, 201]:
                        messagebox.showinfo(title="Success!", message=f"Successfully updated Workshop content:\n"
                                                                      f"Collection: {collection_data['name']}\n"
                                                                      f"ID: {self.controller.collection.get('collection', '')}")
                else:
                    messagebox.showerror(title="Error", message="Error getting collection information")

        elif self.ext.lower() in ['.json', '.gvar']:
            data = getFileContent(sys.argv[1])
            if gvar_id := UUID_PATTERN.search(self.name):
                if len(data) > 100000:
                    messagebox.showerror(title="Error", message="GVARs are limited to 100k characters")

                get = AvraeRest("GET", f"/customizations/gvars/{gvar_id.group(0)}")
                gvar = json.loads(get.text)
                gvar['value'] = data
                post = AvraeRest("POST", f"/customizations/gvars/{gvar_id.group(0)}", gvar)
                if post.status_code in [200, 201]:
                    messagebox.showinfo(title="GVAR Updated", message=f"Successfully update GVAR: {gvar_id.group(0)}")
                else:
                    messagebox.showerror(title="Error", message=f"Error updating GVAR")
            else:
                messagebox.showerror(title="Error", message=f"Invalid GVAR ID")

        self.controller.destroy()

    def _updateCollectionContent(self, type: str = "alias",key: str = "code", id: str = "", data = None):
        status = None
        if key == "code":
            post = AvraeRest("POST", f"workshop/{type.lower()}/{id}/code", data)
            version = json.loads(post.text)['data']['version']
            put = AvraeRest("PUT", f"workshop/{type.lower()}/{id}/active-code", {"version": version})
            status = put.status_code
        elif key == "docs":
            patch = AvraeRest("PATCH", f"workshop/{type.lower()}/{id}", data)
            status = patch.status_code

        if status in [201, 200]:
            messagebox.showinfo(title="Success!", message=f"Successfully update workshop content:\n\n"
                                                          f"Collection: {self.controller.collection.get('name', '')}\n"
                                                          f"Type: {type.title()}\n"
                                                          f"Name: {self.name}\n"
                                                          f"ID: {id}")
        else:
            messagebox.showerror(title="Error", message=f"Unable to update {type.lower()}: {self.name}")

class SettingsMenu(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.collection_id = tk.StringVar(self, value='63e066ecd6596a5e18f1604f')
        self.is_topmost = False

        # QuickMenu Input
        tk.Label(self, text="Collection ID: ", justify="left").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.collection_id, width=30).grid(row=0,column=1,columnspan=4, padx=5, pady=5)

        # Buttons
        tk.Button(self, text="Pull New Collection Data", command=self.get_collection_data).grid(row=1,column=0, padx=5, pady=10)
        tk.Button(self, text="Update Existing Collection", command=self.update_collection).grid(row=1, column=2, padx=5,pady=10)
        tk.Button(self, text="Get GVARs", command=lambda: controller.show_frame('GVAR')).grid(row=1, column=3, padx=5,
                                                                                                pady=10)

        tk.Button(self, text="Update Secret Key", command=lambda: controller.show_frame("AvraeSecret"))\
            .grid(row=2, column=0, padx=5, pady=10, columnspan=3, sticky='w')

    def update_collection(self):
        file = filedialog.askopenfile(mode='r',
                                      title='Select collection file',
                                      initialdir=os.path.abspath(os.path.join(sys.argv[1], os.pardir)),
                                      filetypes=ioFileTypes,
                                      defaultextension=ioFileTypes)
        if not file:
            return
        collection = json.load(file)

        if 'collection' in collection:
            self.collection_id = tk.StringVar(value=collection['collection'])
            self.get_collection_data(file)

    def get_collection_data(self, out = None):
        get = AvraeRest("GET", f"workshop/collection/{self.collection_id.get()}/full")
        collection = json.loads(get.text)['data']
        id_dict = {"name": collection['name'],
                   "collection": self.collection_id.get(),
                   "aliases": {},
                   "snippets": {}}

        for alias in collection.get('aliases', []):
            self.find_sub_aliases(alias, id_dict,"")

        for snippet in collection.get('snippets', []):
            id_dict['snippets'][snippet.get('name')] = snippet.get('_id')

        if not out:
            out = filedialog.asksaveasfile(initialdir=os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                                           mode='w',
                                           filetypes=ioFileTypes,
                                           defaultextension=ioFileTypes,
                                           initialfile='collection.io')
        else:
            f = out.name
            out.close()
            out = open(f, mode='w+')
        if out:
            out.write(json.dumps(id_dict, indent=2))
            out.close()
            if len(collection.get('description', '')) > 0:
                with open(os.path.join(os.path.dirname(out.name), f"readme.md"), mode="w+", encoding="utf-8") as outfile:
                    outfile.write(collection.get('description',""))

    def find_sub_aliases(self, alias: dict, out: dict, curName: str):
        curName = f"{curName} {alias['name']}".strip()
        out['aliases'][curName] = alias['_id']
        for subalias in alias.get('subcommands'):
            self.find_sub_aliases(subalias, out, curName)

class AvraeSecret(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.secret = tk.StringVar(self, value=os.environ['AVRAE_TOKEN'])
        self.is_topmost = False

        # QuickMenu Input
        tk.Label(self, text="Avrae Secret Key ID: ", justify="left").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.secret, width=30).grid(row=0, column=1, columnspan=4, padx=5, pady=5)

        tk.Button(self, text="Main Menu", command=lambda: controller.show_frame("SettingsMenu"))\
            .grid(row=1, column=0, padx=5,pady=10)

        self.secret.trace_add('write', callback=self.callback)

    def callback(self, *args):
        os.environ['AVRAE_TOKEN'] = self.secret.get()

class GVAR(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.gvar = tk.StringVar(self)
        self.is_topmost = False

        # QuickMenu Input
        tk.Label(self, text="GVAR ID: ", justify="left").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry = tk.Entry(self, textvariable=self.gvar, width=50)
        self.entry.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

        tk.Button(self, text="Save GVAR", command=self.get_gvar) \
            .grid(row=1, column=0, padx=5, pady=10)
        tk.Button(self, text="Main Menu", command=lambda: controller.show_frame("SettingsMenu")) \
            .grid(row=1, column=1, padx=5, pady=10)
    def get_gvar(self):
        if gvar_id := UUID_PATTERN.search(self.gvar.get()):
            get = AvraeRest('GET', f'/customizations/gvars/{gvar_id.group(0)}')
            gvar_data = json.loads(get.text)["value"]
            if len(self.controller.collection) == 0:
                if isJSON(gvar_data):
                    out = filedialog.asksaveasfilename(initialdir=os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                                                   filetypes=jsonFileTypes,
                                                   defaultextension=jsonFileTypes,
                                                   initialfile=f"{gvar_id.group(0)}.json")
                else:
                    out = filedialog.asksaveasfilename(initialdir=os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                                                       filetypes=gvarFileTypes,
                                                       defaultextension=gvarFileTypes,
                                                       initialfile=f"{gvar_id.group(0)}.gvar")
            else:
                out = os.path.join(os.path.dirname(sys.argv[1]),f"{gvar_id.group(0)}.gvar")

            if out:
                with open(out, mode='w+', encoding='utf-8') as outfile:
                    outfile.write(gvar_data)
                messagebox.showinfo(title="GVAR Saved", message=f"GVAR Sucessfully saved!")
                self.entry.delete(0, 'end')
        else:
            messagebox.showerror(title="Error", message=f"Invalid GVAR ID")

class SnippetSelect(tk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.is_topmost = False
        self.snippet = tk.StringVar(self)

        tk.Label(self, text="Snippet", justify="left").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Combobox(self, values=list(self.controller.collection.get('snippets', {})),
                             textvariable=self.snippet, width=30)\
            .grid(row=0, column=1, columnspan=2, sticky='w', padx=5, pady=5)

        tk.Button(self, text="Back",
                  command=lambda: controller.show_frame("QuickMenu"), width=20) \
            .grid(row=1, column=0,pady=10, padx=5)
        tk.Button(self, text="Pull",
                  command=self.pull_snippet, width=20) \
            .grid(row=1, column=1,pady=10, padx=5)

    def pull_snippet(self):
        snippet_id = self.controller.collection.get('snippets', {}).get(self.snippet.get(), "")
        get = AvraeRest("GET", f"workshop/snippet/{snippet_id}")
        snippet_data = json.loads(get.text)['data']
        with open(os.path.join(os.path.dirname(sys.argv[1]), f"{snippet_data['name']}.snippet"),mode="w+", encoding="utf-8") as outfile:
            outfile.write("".join(snippet_data['code']).replace('\r',''))
        if len(snippet_data['docs']) > 0:
            with open(os.path.join(os.path.dirname(sys.argv[1]), f"{self.snippet.get()}.md"), mode="w+",encoding="utf-8") as outfile:
                outfile.write("".join(snippet_data['docs']).replace('\r', ''))
        messagebox.showinfo(title="Snippet Saved", message=f"Snippet Sucessfully saved!")
        self.controller.destroy()

class AliasSelect(tk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.is_topmost = False
        self.alias = tk.StringVar(self)

        tk.Label(self, text="Alias", justify="left").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Combobox(self, values=list(self.controller.collection.get('aliases', {})),
                             textvariable=self.alias, width=30)\
            .grid(row=0, column=1, columnspan=2, sticky='w', padx=5, pady=5)

        tk.Button(self, text="Back",
                  command=lambda: controller.show_frame("QuickMenu"), width=20) \
            .grid(row=1, column=0,pady=10, padx=5)
        tk.Button(self, text="Pull",
                  command=self.pull_alias, width=20) \
            .grid(row=1, column=1,pady=10, padx=5)

    def pull_alias(self):
        alias_id = self.controller.collection.get('aliases', {}).get(self.alias.get(), "")
        get = AvraeRest("GET", f"workshop/alias/{alias_id}")
        alias_data = json.loads(get.text)['data']
        with open(os.path.join(os.path.dirname(sys.argv[1]), f"{self.alias.get()}.alias"),mode="w+", encoding="utf-8") as outfile:
            outfile.write("".join(alias_data['code']).replace('\r',''))
            if len(alias_data['docs']) > 0:
                with open(os.path.join(os.path.dirname(sys.argv[1]), f"{self.alias.get()}.md"), mode="w+", encoding="utf-8") as outfile:
                    outfile.write("".join(alias_data['docs']).replace('\r',''))
        messagebox.showinfo(title="Alias Saved", message=f"Alias Sucessfully saved!")
        self.controller.destroy()
