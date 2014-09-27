import inspect

__author__ = 'zats'


def all_subclasses_of_class(class_ref):
    result = []
    subclasses = class_ref.__subclasses__()
    for subclass in subclasses:
        if not inspect.isabstract(subclass):
            result.append(subclass)
        recusrive_result = all_subclasses_of_class(subclass)
        if recusrive_result:
            result += recusrive_result
    return result
