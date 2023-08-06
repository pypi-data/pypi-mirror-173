import os
from pathlib import Path
import re

from rubberdoc.config_provider import RubberDocConfig
from rubberdoc.doc_handler import BaseDocHandler



class RubberDoc:
    """The helpful Rubber Duck that listens and writes!  

    We will put more information here as we go. For now, let's just leave it be.
    """
    def __init__(self, config: RubberDocConfig, doc_handler: BaseDocHandler):
        self.config: RubberDocConfig = config
        self.doc_handler: BaseDocHandler = doc_handler

    def generate(self, input_directory: str, output_directory: str):
        """Generates documentation from docstrings in the provided directory.  
        
        **params**:  
        - input_directory: _str_ the path to the directory for generating code  
        - output_directory: _str_ the path to the directory for the generated documents  
        """
        self.__clean_mds(output_directory)
        for (dirpath, _, filenames) in os.walk(input_directory):          
            if '__pycache__' in str(dirpath):
                continue
            for filename in filenames:
                if self.__wants_to_write(Path(dirpath, filename)):
                    write_path = (
                        Path(output_directory) 
                        / Path(dirpath, filename).relative_to(input_directory).parent
                        / self.__rename_file(Path(filename).stem))
                    print('writing: ', write_path)
                    handler = self.doc_handler(
                        file_path=Path(dirpath) / filename,
                        config=self.config)
                    processed_doc = handler.process()
                    self.save(
                        to=write_path, 
                        content=processed_doc)

    def __clean_mds(self, out_dir: str):
        for (dirpath, _, filenames) in os.walk(out_dir):
            for file in filenames:
                if file.endswith('.md'):
                    os.remove(Path(dirpath, file))
            try:
                os.rmdir(dirpath)
            except: 
                pass
    
    def __wants_to_write(self, file_path: str) -> bool:
        """checks config to determine if this file should be written.  
        
        **returns** __bool__
        """
        write_it = False
        for inc in self.config.input['include']:
            if re.search(inc, str(file_path)):
                write_it = True 
        for exc in self.config.input['exclude']:
            if re.search(exc, str(file_path)):
                write_it = False
        return write_it

    def save(self, to: str, content: str):
        os.makedirs(to.parent, exist_ok=True)
        with open(to, 'w+') as o:
            o.write(content)

    def __rename_file(self, filename):
        rn = self.config.output['rename']
        fn = rn.get(filename, filename)
        return fn + '.md'
