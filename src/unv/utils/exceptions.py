import traceback
import logging


def exception_handler(ex_type, exception, tb, with_class_dict=False):
    """Print the usual traceback information. With extended stack info."""
    original_tb = tb
    while True:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    message = '\n'.join([
        '', "Original exception:",
        '{}: {}'.format(getattr(ex_type, '__name__', 'undefined'), exception),
        ''.join(traceback.format_tb(original_tb)),
        "Extended context:",
        ''.join(iter_format_exception_stack(
            stack, with_class_dict=with_class_dict
        ))
    ])
    logging.error(message)


def iter_format_exception_stack(stack, with_class_dict=False):
    for frame in stack:
        yield "Frame [{}] in {} at line {}\n".format(
            frame.f_code.co_name,
            frame.f_code.co_filename,
            frame.f_lineno
        )
        for key, value in frame.f_locals.items():
            yield "\t{} = ".format(key)
            try:
                yield repr(value)
                if hasattr(value, '__dict__') and with_class_dict:
                    yield "\n"
                    for inner_key, inner_value in value.__dict__.items():
                        yield "\t\t{} = ".format(inner_key)
                        try:
                            yield repr(inner_value)
                        except: # noqa
                            yield "<Error>"
                yield "\n"
            except:  # noqa
                yield "<Error>"
