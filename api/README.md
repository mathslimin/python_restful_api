pip install mdx_smartypants

mdx_smartypants/core.py
41行
self.configs = dict(configs) 修改为 self.configs = dict(configs or {})
https://bitbucket.org/jeunice/mdx_smartypants/pull-request/2/fix-using-the-extension-with-no-config/diff

pip install smartypants
pip install markdown
python markdown_doc.py -o api.html API_Documentation.md
