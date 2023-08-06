class _BaseElement:
    def __init__(self):
        self.innerHtml = '{innerHtml}'
        self.id_ = '{id_}'
        self.class_ = '{class_}'
        self.label = '{label}'
    @property
    def html(self):
        return self.template.format(innerHtml=self.innerHtml, class_=self.class_, id_=self.id_, label=self.label)
    def write(self, content):
        '''Fill this element with the content you provide (text or figure).'''
        pass

class Row(_BaseElement):
    template = '''
    <div id="{id_}" class="{class_}">
        {innerHtml}
    </div>
    '''
    def __init__(self, class_ = 'row pt-3'):
        super().__init__()
        self.class_ = class_

class Column(_BaseElement):
    template = '''
    <div id="{id_}" class="{class_}">
        {innerHtml}
    </div>
    '''
    def __init__(self, n_out_of_12='auto', class_ = 'col-auto'):
        super().__init__()
        self.class_ = f'col-md-{n_out_of_12}'
        if class_ != 'col-auto':
            self.class_ = class_

class Button(_BaseElement):
    template = '''
    <button id="{id_}" class="{class_}">
        {innerHtml}
    </button>
    '''
    def __init__(self, innerHtml = 'Click Me', class_ = 'btn btn-primary'):
        super().__init__()
        self.innerHtml = innerHtml
        self.class_ = class_

class Input(_BaseElement):
    template = '''
<div class="{class_}">
    <label for="{id_}" class="col-sm-2 col-form-label">{label}</label>
    <div class="col-sm-10">
        <input type="text" class="form-control" id="{id_}">
    </div>
</div>
    '''
    def __init__(self, label = 'Input text', class_ = 'mb-3 row'):
        super().__init__()
        self.class_ = class_
        self.label = label

class File(_BaseElement):
    template = '''
<div class="{class_}">
  <label for="{id_}" class="form-label">{label}</label>
  <input class="form-control" type="file" id="{id_}">
</div>
    '''
    def __init__(self, label = 'Upload file', class_ = 'mb-3 row'):
        super().__init__()
        self.class_ = class_
        self.label = label

class Textarea(_BaseElement):
    template = '''
<div class = "{class_}">
    <label for = "{id_}" class="form-label">{label}</label>
    <textarea id="{id_}" class = "form-control" rows = "3" placeholder = ""></textarea>
</div>
    '''
    def __init__(self, label = 'Input lone text', class_ = 'mb-3 row'):
        super().__init__()
        self.class_ = class_
        self.label = label

class SelectOne(_BaseElement):
    template = '''
<form class="{class_}" id="{id_}">
<label for="{id_}" class="form-label">{label}</label>
  {innerHtml}
</form>
    '''
    _item = '''
<div class="form-check">
  <input class="form-check-input" type="radio" name="index" id="{i}" value={index} {checked}>
  <label class="form-check-label" for="{i}">
    {i}
  </label>
</div>
'''
    def __init__(self, from_, label='Select one', default_index=-1, class_ = 'mb-3 row'):
        super().__init__()
        self.class_ = class_
        self.label = label
        self.from_ = from_
        self.default_index = default_index
        self.template = self.template.replace('{innerHtml}', self.inner_html)

    @property
    def inner_html(self):
        inner = ''
        for index, i in enumerate(self.from_):
            checked = ''
            if index == self.default_index:
                checked = 'checked'
            inner += self._item.format(i=i, index=index, checked=checked)
        return inner

class SelectMulti(_BaseElement):
    template = '''
<form id="{id_}" class="{class_}">
<label for="{id_}" class="form-label">{label}</label>
  {innerHtml}
</form>
    '''
    _item = '''
<div class="form-check">
  <input class="form-check-input" type="checkbox" name="index" value="{index}" id="{i}" {checked}>
  <label class="form-check-label" for="{i}">
    {i}
  </label>
</div>
    '''
    def __init__(self, from_, label='Select one or more', default_index=[], class_ = 'mb-3 row'):
        super().__init__()
        self.class_ = class_
        self.label = label
        self.from_ = from_
        self.default_index = default_index
        self.template = self.template.replace('{innerHtml}', self.inner_html)

    @property
    def inner_html(self):
        inner = ''
        for index, i in enumerate(self.from_):
            checked = ''
            if index in self.default_index:
                checked = 'checked'
            inner += self._item.format(i=i, index=index, checked=checked)
        return inner

class Text(_BaseElement):
    template = '''
<h{n} id ="{id_}" class="{class_}">{content}</h{n}>
'''
    def __init__(self, content, size_level=0, class_=' '):
        super().__init__()
        self.class_ = class_
        self.content = content
        self.l = size_level
        self.template = self.htm()
    def htm(self):
        if self.l > -1 and self.l < 6:
            _ = self.template.replace('{n}', str(6-self.l))
            return _.replace('{content}', self.content)
        else:
            raise TypeError('big_level should be a integer form 0 to 5')

################################################################################################################################
class Page:
    template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <link rel="stylesheet" href="{css_url}" />
  <script defer src="{js_url}"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
</head>
<body class="container">
  {layout}

  <py-config>
    packages = {packages}
  </py-config>

  <py-script id="pyspage">
{script}
  </py-script>
</body>
</html>
'''
    def __init__(self,
        page_title = 'pyspage',
        css_url = 'https://pyscript.net/latest/pyscript.css',
        js_url = 'https://pyscript.net/latest/pyscript.js',
        layout = '',
        script = '',
        packages = '[]'
    ):
        self.page_title = page_title
        self.css_url = css_url
        self.js_url = js_url
        self.layout = layout
        self.script = script
        self.packages = packages
    
    @property
    def html(self):
        return self.template.format(
            page_title = self.page_title,
            css_url = self.css_url,
            js_url = self.js_url,
            layout = self.layout,
            script = self.script,
            packages = self.packages,
        )