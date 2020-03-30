from importlib import import_module


class BaseExtension:
    def __init__(self, path):
        self.path = path
        self.module = None


class FileExtension(BaseExtension):
    def __init__(self, path):
        super().__init__(path)

        try:
            self.module = import_module(str(self.path).replace('/', '.'))
        except Exception as e:
            print(e)
            self.module = None

    def has_setup(self):
        try:
            self.module.setup
        except AttributeError:
            return False
        return True

    def get_version(self):
        return getattr(self.module, '__version__', 'None')

    def __str__(self):
        return str(self.path).replace('/', '.')

    def __repr__(self):
        return str(self.path).replace('/', '.')


class PyExtension(BaseExtension):
    def __init__(self, path):
        super().__init__(path)

        try:
            self.module = import_module(str(self.path).replace('/', '.')[:-3])
        except Exception:
            print(e)
            self.module = None

    def has_setup(self):
        try:
            self.module.setup
        except AttributeError:
            return False
        return True

    def get_version(self):
        return getattr(self.module, '__version__', None)

    def __str__(self):
        return str(self.path).replace('/', '.')[:-3]

    def __repr__(self):
        return str(self.path).replace('/', '.')[:-3]
