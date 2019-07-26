
class AppInfo:

    def __init__(self, namespace, version, name = "", authors = [], license_name = "", short_description = "", description = ""):
        self.namespace = namespace
        self.version = version
        self.name = name
        self.authors = authors
        self.licence = license_name
        self.short_description = short_description
        self.description = description