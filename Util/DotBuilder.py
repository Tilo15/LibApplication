
class DotBuilder(object):

    def __init__(self, delimiter = ".", prefix = ""):
        # Get base object
        base = super()

        # Set "obj" and "instance" attributes
        base.__setattr__("delimiter", delimiter)
        base.__setattr__("prefix", prefix)

    def __getattribute__(self, attr):
        # Get the base object
        base = super()

        # Get "obj" and "instance" attributes
        delimiter = base.__getattribute__("delimiter")
        prefix = base.__getattribute__("prefix")

        # Add a delimiter between prefix and the attr if this is not the first item
        if(prefix != ""):
            return DotBuilder(delimiter, "{0}{1}{2}".format(prefix, delimiter, attr))

        # First item
        return DotBuilder(delimiter, attr)

    def __str__(self):
        return super().__getattribute__("prefix")
