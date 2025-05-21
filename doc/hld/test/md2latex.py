#!/usr/bin/env python3

import re
import sys

def markdown_to_latex(input_file, output_file=None):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().split('\n')

    latex = [
        r'\begin{itemize}'
    ]

    current_section = None
    in_list = False

    for line in content:
        # Обработка заголовков
        if line.startswith('#'):
            if in_list:
                latex.append(r'\end{enumerate}')
                in_list = False
            current_section = line[2:].strip()
            latex.append(r'\item \textbf{' + current_section + r'}:')

        # Обработка списков
        elif line.startswith('-'):
            if not in_list:
                latex.append(r'\begin{enumerate}')
                in_list = True
            list_item = line[2:].strip()
            latex.append(r'\item ' + list_item)

        # Обработка изображений
        elif line.startswith('['):
            img_path = re.search(r'\[(.*?)\]', line).group(1)
            latex.append(r'\includegraphics{' + img_path + '}')

        # Обработка обычного текста
        elif line.strip() and current_section:
            if in_list:
                latex.append(r'\end{enumerate}')
                in_list = False
            latex[-1] += ' ' + line.strip()

    if in_list:
        latex.append(r'\end{enumerate}')

    latex.extend([
        r'\end{itemize}',
    ])

    print('\n'.join(latex))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python md2latex.py input.md")
        sys.exit(1)

    markdown_to_latex(sys.argv[1])
