class Base:
    def __init__(self):
        self.innerHtml = '{innerHtml}'
        self.id_ = '{id_}'
        self.class_ = '{class_}'
    @property
    def html(self):
        return self.template.format(innerHtml=self.innerHtml, class_=self.class_, id_=self.id_)
    def write(self, content):
        '''Fill this element with the content you provide (text or figure).'''
        pass

class Row(Base):
    template = '''
    <div id="{id_}" class="{class_}">
        {innerHtml}
    </div>
    '''
    def __init__(self, class_ = 'row'):
        super().__init__()
        self.class_ = class_

class Column(Base):
    template = '''
    <div id="{id_}" class="{class_}">
        {innerHtml}
    </div>
    '''
    def __init__(self, class_ = 'col-auto'):
        super().__init__()
        self.class_ = class_

class Button(Base):
    template = '''
    <button id="{id_}" class="{class_}">
        {innerHtml}
    </button>
    '''
    def __init__(self, innerHtml = 'Click Me', class_ = 'btn btn-primary'):
        super().__init__()
        self.innerHtml = innerHtml
        self.class_ = class_

# class Input(Base):
#     template = '''
# <div class="mb-3 row">
#     <label for="inputPassword" class="col-sm-2 col-form-label">Password</label>
#     <div class="col-sm-10">
#         <input type="password" class="form-control" id="inputPassword">
#     </div>
# </div>
#     '''
#     def __init__(self, label = 'Input', class_ = ''):
#         super().__init()
#         self.class_ = class_

# class File(Base):
#     template = '''
# <div class="mb-3">
#   <label for="formFile" class="form-label">Default file input example</label>
#   <input class="form-control" type="file" id="formFile">
# </div>
#     '''
#     def __init__(self, label = 'File', class_ = ''):
#         super().__init()
#         self.class_ = class_

# class Textarea(Base):
#     template = '''
# <div class = "row">
#     <label for = "name">{label}</label>
#     <textarea class = "form-control" rows = "3" placeholder = ""></textarea>
# </div>
#     '''
#     def __init__(self, label = 'Textarea', class_ = ''):
#         super().__init()
#         self.class_ = class_

# class SelectOne(Base):
#     template = '''
# <div class="form-check">
#   <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
#   <label class="form-check-label" for="flexRadioDefault1">
#     Default radio
#   </label>
# </div>
# <div class="form-check">
#   <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
#   <label class="form-check-label" for="flexRadioDefault2">
#     Default checked radio
#   </label>
# </div>
#     '''
#     def __init__(self, from_, class_ = ''):
#         super().__init()
#         self.class_ = class_

# class SelectMany(Base):
#     template = '''
# <div class="form-check">
#   <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
#   <label class="form-check-label" for="flexCheckDefault">
#     Default checkbox
#   </label>
# </div>
# <div class="form-check">
#   <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked>
#   <label class="form-check-label" for="flexCheckChecked">
#     Checked checkbox
#   </label>
# </div>
#     '''
#     def __init__(self, from_, class_ = ''):
#         super().__init()
#         self.class_ = class_

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
    ):
        self.page_title = page_title
        self.css_url = css_url
        self.js_url = js_url
        self.layout = layout
        self.script = script
    
    @property
    def html(self):
        return self.template.format(
            page_title = self.page_title,
            css_url = self.css_url,
            js_url = self.js_url,
            layout = self.layout,
            script = self.script,
        )