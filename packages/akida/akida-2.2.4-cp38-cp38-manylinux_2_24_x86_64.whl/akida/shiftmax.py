from akida.core import (Layer, LayerParams, LayerType)


class Shiftmax(Layer):
    """A function similar to the softmax.

    Instead of using e as base, it uses 2 and a shift. So we replace

        softmax(x_i) = e^x_i / sum(e^x_k)

    with

        shiftmax(x_i) = 2^x_i / round(log2(sum(2^x_k)))

    This is evaluated with a shift.

    Args:
        output_bits (int): output bitwidth.
        buffer_bits (int): internal bitwidth.
    """

    def __init__(self,
                 output_bits=8,
                 buffer_bits=23,
                 name=""):
        try:
            params = LayerParams(
                LayerType.Shiftmax, {
                    "output_bits": output_bits,
                    "buffer_bits": buffer_bits
                })
            # Call parent constructor to initialize C++ bindings
            # Note that we invoke directly __init__ instead of using super, as
            # specified in pybind documentation
            Layer.__init__(self, params, name)
        except BaseException:
            self = None
            raise
