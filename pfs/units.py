class GenericUnit:
    '''Generic Process Unit class'''

    def __init__(self, inputs, outputs):

        if not isinstance(inputs, list):
            self.inputs = [inputs]

        if not isinstance(outputs, list):
            self.outputs = [outputs]
    
    def get_transfer_function(self):
        raise NotImplementedError('Feature not implemented in generic class; use sub class.')

    def get_output(self, objdir):
        tf = self.get_transfer_function()
        input_objects = [objdir[inp] for inp in self.inputs]
        output = tf(*[iobj.get_output() for iobj in input_objects])
