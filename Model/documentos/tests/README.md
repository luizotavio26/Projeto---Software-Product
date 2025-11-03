# Teste de criação de documentos

Os documentos são criados utilizando a biblioteca **FPDF**, uma ferramenta poderosa e leve para gerar arquivos **PDF** em Python.

📘 **Link oficial:** [https://www.fpdf.org/?lang=es](https://www.fpdf.org/?lang=es)

---

## ⚙️ Instalação

Antes de tudo, instale a biblioteca:

```bash
pip install fpdf
```

Mini documento do fpdf

## 📄 Estrutura do Documento

### 1.add_page()

```
 pdf.add_page()
```

- Adiciona uma nova página ao documento.

### 2.set_auto_page_break(auto=True, margin=10)

```
pdf.set_auto_page_break(auto=True, margin=15)
```

- Define quebra automática de página.
- margin define o espaço inferior antes de criar nova página.

### 3.alias_nb_pages(alias='{{nb}}')

```
 pdf.alias_nb_pages()
```

- Cria um alias para o número total de páginas, útil em rodapés.

### 4.pdf.set_font('Arial', 'B', 16)

```
 pdf.set_font('Arial', 'B', 16)
```

- Define a fonte do texto.
  - **family**: nome da fonte (**Arial**, **Courier**, **Times**, etc.)
  - **style**: estilo da fonte (**B** para negrito, **I** para itálico
  - **size**: tamanho da fonte (ex: 12)

### 5.cell(w, h, txt='', border=0, ln=0, align='', fill=False, link='')

```
 pdf.cell(40, 10, 'Olá Mundo!', 1, 1, 'C')
```

- Cria uma célula de texto.
  - **w**, **h**: largura e altura
  - **txt**: texto a exibir
  - **border**: 0 (sem borda) ou 1 (com borda))
  - **ln**: 1 pula linha após a célula
  - **align**: **'L'**,**'C'**,**'R'** (alinhamento)
  - **fill**: preenche o fundo
  - **link:**: cria hiperlink

### 6.multi_cell(w, h, txt, border=0, align='J')

```
pdf.multi_cell(0, 10, 'Texto longo\ncom várias linhas')
```

- Cria um bloco de texto com quebra automática de linha.

### 7.text(x, y, txt)

```
pdf.text(10, 50, "Texto posicionado em (10, 50)")
```

- Escreve texto diretamente nas coordenadas **(x, y)**.

### 8.write(h, txt)

```
pdf.write(8, "Texto contínuo com quebra de linha automática.")
```

- Escreve texto em formato de parágrafo contínuo.

### 9.set_text_color(r, g=-1, b=-1)

```
 set_text_color(r, g=-1, b=-1)
```

- Define a cor do texto em RGB.

## 🖼️Imagens e Formatação

### 10.image(name, x=None, y=None, w=0, h=0, type='', link='')

```
 pdf.image('logo.png', x=10, y=8, w=33)
```

- Insere uma imagem
  - **x, y**: posição
  - **w, h**: tamanho
  - **type**: formato (**'PNG'**, **'JPG'**, etc.)
  - **link**: transforma a imagem em link clicável

### 11.set_draw_color(r, g=-1, b=-1)

```
 pdf.set_draw_color(0, 0, 255)
```

- Define cor para bordas e linhas.

### 12.set_fill_color(r, g=-1, b=-1)

```
pdf.set_fill_color(220, 220, 220)
```

- Define cor de preenchimento de células e fundos.

### 13.set_line_width(width)

```
pdf.set_line_width(0.5)
```

- Define espessura de linhas e bordas.

## 🧭 Posições e Layout

### 14.set_xy(x, y)

```
pdf.set_xy(50, 100)
```

- Define a posição atual do cursor (x, y).

### 15.set_x(x) e set_y(y)

```
pdf.set_x(20)  pdf.set_y(30)
```

- Move o cursor apenas no eixo X ou Y.

### 16.pdf.ln(10)

```
pdf.ln(10)
```

- Pula uma linha de altura h (semelhante a \n no texto).

## 📚 Cabeçalhos e Rodapés (personalizados)

Você pode sobrescrever métodos dentro de uma classe filha:

```
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Cabeçalho do Documento', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
```

## 📊 Utilidades

### 17.page_no()

```
pdf.cell(0, 10, f'Página {pdf.page_no()}')
```

- Retorna o número da página atual.

### 18.set_margins(left, top, right=-1)

```
pdf.set_margins(15, 10, 15)
```

- Define margens esquerda, superior e direita.

### 19.get_x() / get_y()

```
x = pdf.get_x()
y = pdf.get_y()
```

- Retorna a posição atual do cursor.

Exportação

```
pdf.output('meu_documento.pdf')
```

- Gera e salva o PDF.
  - **name**: nome do arquivo
  - **dest**:
    - **'F'**: salva em arquivo (padrão)
    - **'S'**: retorna como string
    - **'B'**: retorna bytes
    - **'L'**: abre inline no navegador
    - **'D'**: força download

⚙️ Exemplo Completo

```
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatório de Faturamento", ln=True, align="C")

pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "CNPJ: 12.345.678/0001-90", ln=True)
pdf.multi_cell(0, 10, "Este é um exemplo de geração de PDF usando a biblioteca FPDF.\n"
                      "Você pode adicionar texto, imagens, tabelas e muito mais.")

pdf.output("exemplo.pdf")
```

🧠 Dica Fina

Use multi_cell() para textos longos e cell() para layouts em tabela.
Combine set_fill_color() e set_draw_color() para criar estilos personalizados.

📘 Resumo Rápido de Métodos:

| Método             | Função                              |
| ------------------ | ----------------------------------- |
| `add_page()`       | Adiciona nova página                |
| `set_font()`       | Define a fonte                      |
| `cell()`           | Cria uma célula de texto            |
| `multi_cell()`     | Texto com quebra automática         |
| `image()`          | Adiciona imagem                     |
| `set_text_color()` | Muda cor do texto                   |
| `set_fill_color()` | Cor de fundo                        |
| `set_draw_color()` | Cor da borda                        |
| `output()`         | Gera o arquivo PDF                  |
| `page_no()`        | Retorna número da página            |
| `set_xy()`         | Define posição atual                |
| `ln()`             | Pula linha                          |
| `alias_nb_pages()` | Cria marcador para total de páginas |

✍️ Autor: João Pedro Silva Antunes
📅 Data: Outubro de 2025
🧰 Projeto: Geração de PDFs com Python (FPDF)
