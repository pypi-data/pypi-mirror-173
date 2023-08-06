"""
The DocHandler processes a single python file into a page for your documentation.
"""
import ast
import importlib.util
import sys

from rubberdoc.config_provider import RubberDocConfig



class BaseDocHandler:
    """BaseDocHandler contains core functionality for converting python files to markdown.  

    Methods beginning with 'wrap_' can be overridden to create a custom DocHandler, similar
    to how the MaterialMKDocHandler does so.
    """
    def __init__(self, file_path: str, config: RubberDocConfig):
        self.file_path = file_path
        self.config = config
        self.doc: list = list()
        self.code: list = list()
    
    def process(self) -> str:
        """Processes a file to markdown."""        
        with open(self.file_path, 'r') as o:
            if str(self.file_path).endswith('.md'):
                return o.read()
            self.source_code = o.read()
            tree = ast.parse(self.source_code)
            self.__module_docstring(tree)
            self.__walk_tree(tree)
        return ''.join(self.doc)
    
    def __module_docstring(self, tree):
        module_docstring = ast.get_docstring(tree)
        if module_docstring:
            self.doc.append(module_docstring + '  \n')
    
    def __walk_tree(self, tree):
        for node in tree.body:
            level = 1
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                self.process_node(level, node)
                if isinstance(node, ast.ClassDef):
                    level += 1
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            self.process_node(level, child, node)
    
    def process_node(self, level: int, node: ast.ClassDef | ast.FunctionDef, parent=None):
        """ Processes a function or class **node** into markdown and appends to doc.  

        This function can be overriden to determine the order of parsed elements of the node. 
        __params__  
        - `level` _int_  level for indentation purposes  
        - `node` _ast.ClassDef | ast.FunctionDef_ the current node to be processed  
        - `parent` _ast.ClassDef | None_ the parent class if a function node  
        """
        if parent:
            self.doc.append(self.wrap_func_cls_lbl(parent.name))
        
        # function or class name
        self.doc.append(self.wrap_func_cls_name(level, node))
        
        
        docstring = self.get_docstring(node)
        source_code = self.get_node_code(node)
        
        self.doc.append(self.wrap_docstring(docstring))
        if self.config.output['include_source_code']:
            self.doc.append(self.wrap_codeblock(source_code))
    
    def get_docstring(self, node: ast.ClassDef | ast.FunctionDef) -> str:
        """Returns the docstring of the class or function **node**.  
        
        If no docstring is found in the node, a default is returned. 
        This default can be set in the configuration file
        """
        return ast.get_docstring(node) or self.config.output['no_docstring_default']
    
    def get_node_code(self, node: ast.ClassDef | ast.FunctionDef) -> str:
        """Returns the codeblock of the class or function **node**."""
        return ast.get_source_segment(self.source_code, node)
    
    def get_function_params(self, node: ast.FunctionDef) -> list[str]:
        """Returns a list of parameters for the function **node**.  

        I would like to have this show the parameter types, but couldn't figure
        out how to do so. If you figure it out - please let me know!        
        """
        return [f"{a.arg}" for a in node.args.args]
    
    def get_class_bases(self, node: ast.ClassDef) -> list[str]:
        return [b.id for b in node.bases]
    
    def get_node_return_type(self, node: ast.ClassDef | ast.FunctionDef) -> str:
        return node.returns.id if node.returns else ''
    
    def wrap_func_cls_lbl(self, parent_name: str) -> str:
        return parent_name + '  \n'
    
    def wrap_func_cls_name(self, level: int, node: ast.ClassDef | ast.FunctionDef) -> str:
        # avoid markdown collisions with dunder methods
        node_name = node.name
        if node_name.startswith('_') and node_name.endswith('_'):
            node_name = f"\{node_name}"

        # if class inherits let it be known!
        inherits = ''
        if isinstance(node, ast.ClassDef):
            bases = self.get_class_bases(node)
            if bases:
                inherits = f" ({', '.join(bases)})"

        return (f"{'#' * (level + 1)} "
                f"{'__def__ ' if isinstance(node, ast.FunctionDef) else '__class__ '}"
                f"{node_name}{inherits}  \n")
    
    def wrap_docstring(self, docstring: str) -> str:
        """Wraps the provided docstring for markdown.  
        
        If you are using RubberDoc generation from a python script,
        you could subclass the DocHandler and override this method to your
        preferred style.
        """
        return docstring + "  \n"
    
    def wrap_codeblock(self, code: str) -> str:
        """Wraps the provided codeblock for markdown.  
        
        If you are using RubberDoc generation from a python script,
        you could subclass the DocHandler and augment this method to your
        preferred style.
        """
        c = '```\n'
        c += code
        c += '\n```\n'
        return c
    

class MaterialMKDocHandler(BaseDocHandler):
    """Documentation generated centered towards Material theme for MKDocs.  
    
    This is the preferred generator for RubberDoc. 
    If you run the generator from the commandline, this theme is used by default.
    It expects that you have a few additions into the mkdocs.yml file:  
    ```
    markdown_extensions:
        - pymdownx.tabbed:
            alternate_style: true
    ```
    """
    def __init__(self, file_path: str, config: RubberDocConfig):
        super().__init__(file_path=file_path, config=config)
    
    def process_node(self, level: int, node: ast.ClassDef | ast.FunctionDef, parent=None):
        if parent:
            self.doc.append(self.wrap_func_cls_lbl(parent.name))
        
        # function or class name
        self.doc.append(self.wrap_func_cls_name(level, node))
        
        if isinstance(node, ast.FunctionDef):
            self.doc.append(self.wrap_function_params(node))
        
        docstring = self.get_docstring(node)
        source_code = self.get_node_code(node)
        
        self.doc.append(self.wrap_docstring(docstring))
        if self.config.output['include_source_code']:
            self.doc.append(self.wrap_codeblock(source_code))
        self.doc.append('\n---  \n')
    
    def wrap_function_params(self, node: ast.FunctionDef) -> str:
        params = self.get_function_params(node) or ''
        if params:
            params = f"**Params:** `{', '.join(params)}`  \n"
        return params
    
    def wrap_func_cls_lbl(self, parent_name: str):
        return f"<label class='class-label'>{parent_name}</label>  \n"
    
    def wrap_docstring(self, docstring: str) -> str:
        """Wraps the provided docstring for markdown.  
        
        If you are using RubberDoc generation from a python script,
        you could subclass the DocHandler and augment this method to your
        preferred style.
        """
        d = '=== "Documentation"\n'
        d += '\n'.join(f"    {d}" for d in docstring.splitlines())
        d += "  \n\n"
        return d
    
    def wrap_codeblock(self, code: str) -> str:
        """Wraps the provided codeblock for markdown.  
        
        If you are using RubberDoc generation from a python script,
        you could subclass the DocHandler and augment this method to your
        preferred style.
        """
        c = '=== "Code"\n'
        c += '    ```py\n'
        c += '\n'.join(f"    {l}" for l in code.splitlines())
        c += '\n    ```  \n'
        c += "  \n\n"
        return c


def doc_handler_selection(config: RubberDocConfig, style: str) -> BaseDocHandler | None:
    """Determines the DocHandler to provide given a `RubberDocConfig` and `style`"""
    cust_fp = config.output['custom_doc_handler_filepath']
    cust_cls = config.output['custom_doc_handler_class_name']
    handler = None
    if cust_fp and cust_cls:
        spec = importlib.util.spec_from_file_location(cust_cls, cust_fp)
        foo = importlib.util.module_from_spec(spec)
        sys.modules[cust_cls] = foo
        spec.loader.exec_module(foo)
        handler = getattr(foo, cust_cls, None)
    elif style.lower() == 'material':
        handler = MaterialMKDocHandler
    elif style.lower() == 'default':
        handler = BaseDocHandler
    return handler