# Source

The paper itself is not redistributed here — fetch it from arXiv and convert it locally:

```bash
curl -sL -A "Mozilla/5.0" https://arxiv.org/html/2603.20617v3 -o paper_v3.html
python tohtml.py paper_v3.html paper_v3.txt
```

`tohtml.py` flattens LaTeXML's HTML to text while preserving the maths: it pulls the
LaTeX out of each `<math alttext="...">` attribute rather than dropping it, so the
propositions stay readable in a terminal.

Paper: Brett Hemenway Falk and Gerry Tsoukalas, *The AI Layoff Trap*,
[arXiv:2603.20617](https://arxiv.org/abs/2603.20617), CC BY-NC-SA 4.0.
