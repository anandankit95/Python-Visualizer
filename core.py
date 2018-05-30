import json
import sys
import inspect
from utils import (get_obj_type, set_trace)
from visualize import visualize

class CallSequence():
    def __init__(self):
        self.top_call_sequence = {'seq': []}
        self.current_call_sequence = self.top_call_sequence
        self.stack = [self.top_call_sequence]
        '''
        print("***************************************************************************************************")
        print(self.stack)
        print("***************************************************************************************************")
        '''
        self.record_local_vars = False
        #self.depth = 0

   

    def trace(self, frame, event, arg):
        # if there is no previous frame or if we reach max depth, ignore and return
        
        if not frame.f_back:
                
            return self.trace

        # if a function is being called, create and push a stack record and continue
        if event == 'call':
            #self.increase_depth()
            

            self.record_local_vars = True

            caller_code = frame.f_back.f_code  #frame.f_back refers callers frame in reference to current frame
            #print("ON CALL")
            #print(caller_code)
            callee_code = frame.f_code  # obtain the called function code
            #print(callee_code)

            # get the file names, converting to relative names if necessary
            caller_file_name = caller_code.co_filename

            callee_file_name = callee_code.co_filename

            # create a stack record representation
            new_call_sequence = {
                'seq': [], # what do we call next?
                "function_name": callee_code.co_name, #name of the current function
                'extra': { # extra details
                    'caller_location':
                    "{}:{}".format(caller_file_name, frame.f_back.f_lineno),
                    'callee_location':
                    "{}:{}".format(callee_file_name,
                                   frame.f_code.co_firstlineno),
                }
            } # return values and params get added later

            self.stack[-1]['seq'].append(new_call_sequence)
            self.stack.append(new_call_sequence)
            self.stack[-1]['arguments'] = get_obj_type(frame.f_locals)
            '''print("------------------------------------------------------------------------------------------------")
            print(self.stack)
        print("------------------------------------------------------------------------------------------------")'''
        # If a function has returned, pop the stack record, and add return details to the seq param of the caller function record
        elif event == 'return':
            if self.stack[-1] is self.top_call_sequence:
                return self.trace
            #print("ON RETURN") 
            #self.decrease_depth()
            self.stack[-1]['return'] = get_obj_type(arg)
            self.stack[-1]['return_lineno'] = frame.f_lineno
            self.stack.pop()
           

        return self.trace

    def visualize(self):
        #print(self.top_call_sequence.keys())
        #print("top call seq",self.top_call_sequence)
        visualize(self.top_call_sequence)

    def tracer(self):
        set_trace(self.trace)
        #print(type(self.trace))

    def unset_tracer(self):
        set_trace(None)


if __name__ == '__main__':
    
    file_name = sys.argv[1]
    seq = CallSequence()
    seq.tracer()
    execfile(file_name)
    seq.unset_tracer()
    print("------ PRINTING TREE VISUALIZATION -----")
    seq.visualize()
    
