from dataclasses import dataclass
import json


@dataclass
class Files:
    '''Works with files input and output in different formats.
    '''

    path_in: str = None
    path_out: str = None


    def convert_jupyter(self, nb_exporter):
        '''Converts a upyter notebook into a different format using a
        nbconvert selected exporter method.
        '''

        doc = nb_exporter.from_filename(self.path_in)
        with open(self.path_out, 'w') as file:
            file.write(doc[0])


    def open_json(self):
        '''Opens the JSON file into a dictionary.
        '''

        with open(self.path_in) as file:
            dict_file = json.load(file)
        
        return dict_file
    

    def code_to_md(self):
        '''Extracts the Python code into a Markdown file with the
        language highlights.
        '''
        
        with open(self.path_in) as file_in:
            code = file_in.read()
            md_start = '```python\n\n'
            md_end = '\n\n```'
            code = md_start + code + md_end
        with open(self.path_out, 'w') as file_out:
            file_out.write(code)