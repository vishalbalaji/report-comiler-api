from pypandoc import convert_text
import yaml
import os


def make_tex(metadata_dict, markdown_text):
    metadata = yaml.dump(metadata_dict, default_flow_style=False)
    markdown_text = '---\n' + metadata + '\n---\n\n' + markdown_text

    latex_text = convert_text(
        source=markdown_text,
        to='latex',
        format='markdown',
        extra_args=(
            '--natbib',
            '--bibliography', 'refs.bib',
            '--template', os.path.join(os.getcwd(), 'assets', 'template.latex'),
            # Variables
            '-V', 'documentclass:report',
            '-V', 'classoption:a4paper',
            # Filters
            '--filter', 'pandoc-crossref',
        )
    )

    latex_text = latex_text.replace(
        '\\begin{table}[]', '\\begin{table}[htpb]\n\\centering')

    return latex_text
