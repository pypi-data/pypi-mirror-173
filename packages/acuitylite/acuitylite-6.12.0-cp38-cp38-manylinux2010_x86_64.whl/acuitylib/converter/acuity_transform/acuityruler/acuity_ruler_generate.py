import json
import sys
import os
import dill

ruler_list = list()

r_instancenorm = {
"ruler_name": "r_instancenorm",
"src_ops_alias": ["pooling", "squared_difference", "pooling_1", "Add", "Rsqrt", "Multiply", "Multiply_1", \
                  "Multiply_2", "Subtract", "Add_1", 'variable', 'variable_1', 'variable_2'],
"src_inter_flow": [["pooling:out0", "squared_difference:in1"],
                   ["squared_difference:out0", "pooling_1:in0"],
                   ["pooling_1:out0", "Add:in0"],  # add:in1
                   ["Add:out0", "Rsqrt:in0"],
                   ["Rsqrt:out0", "Multiply:in0"], # multiply:in1
                   ["Multiply:out0", "Multiply_1:in1"],
                   ["Multiply_1:out0", "Add_1:in0"],
                   ["Multiply:out0", "Multiply_2:in1"],
                   ["pooling:out0", "Multiply_2:in0"],
                   ["Multiply_2:out0", "Subtract:in1"],
                   ["Subtract:out0", "Add_1:in1"],
                   ["variable:out0", "Multiply:in1"],
                   ["variable_1:out0", "Subtract:in0"],
                   ["variable_2:out0", "Add:in1"]
                   ],
"src_in_anchor": [["I:out0", "Multiply_1:in0"], ["I:out0", "squared_difference:in0"], ["I:out0", "pooling:in0"]],
"src_out_tensor": ["Add_1:out0"],
"acu_lys_alias": ["instancenormalize"],
"src_acu_in_tensor_map": [["I:out0", "instancenormalize:in0"]],
"src_acu_out_tensor_map": [["Add_1:out0", "instancenormalize:out0"]],
"param_map":{
    "instancenormalize":{
        'eps': ['FLOAT', 'CODE', "self.tensor_to_numpy(tensor['variable_2:out0'], 'data')"],
        'axis': ['INTS', 'CODE', "list(range(2, self.get_output_shape(node['Add_1'])[0]))"],
    }
},
"blob_map": {
    "instancenormalize": {'bias': ['CODE', "self.get_value_attr(node['variable_1'], 'data')"],
                                'scale': ['CODE', "self.get_value_attr(node['variable'], 'data')"],}
},

"acu_inter_flow": [],
"priority_tip": 0,
"extension": [
    ["CODE", "self.qnt_out_tensor(acu_ly['instancenormalize'], tensor['Add_1:out0'], 0)"],
],
"pre_condition": None,
"src_ops_main_version": None,
"src_ops_minior_version": [1, -1]}
ruler_list.append(r_instancenorm)

r_lstm = {
"ruler_name": "r_lstm",
"src_ops_alias": ["concat", "fullconnect", "split", "sigmoid", "sigmoid_1", "multiply", "tanh", \
                  'variable', "add", "sigmoid_2", "multiply_1", "add_1", "tanh_1", "multiply_2"],
"src_inter_flow": [["concat:out0", "fullconnect:in0"],
                   ["fullconnect:out0", "split:in0"],
                   ["split:out3", "sigmoid:in0"],
                   ["sigmoid:out0", "multiply_2:in0"],
                   ["split:out0", "sigmoid_1:in0"],
                   ["sigmoid_1:out0", "multiply:in0"],
                   ["multiply:out0", "add_1:in1"],
                   ["add_1:out0", "tanh_1:in0"],
                   ["tanh_1:out0", "multiply_2:in1"],
                   ["split:out1", "tanh:in0"],
                   ["tanh:out0", "multiply:in1"],
                   ["split:out2", "add:in0"],
                   ["variable:out0", "add:in1"],
                   ["add:out0", "sigmoid_2:in0"],
                   ["sigmoid_2:out0", "multiply_1:in0"],
                   ["multiply_1:out0", "add_1:in0"],
                   ],
"src_in_anchor": [["I:out0", "concat:in0"], ["I_1:out0", "concat:in1"], ["I_2:out0", "multiply_1:in1"]],
"src_out_tensor": ["multiply_2:out0", "add_1:out0"],
"acu_lys_alias": ["lstmunit"],
"src_acu_in_tensor_map": [["I:out0", "lstmunit:in0"],["I_1:out0", "lstmunit:in1"],["I_2:out0", "lstmunit:in2"],],
"src_acu_out_tensor_map": [["multiply_2:out0_0", "lstmunit:out0"], ["multiply_2:out0_1", "lstmunit:out1"],
                           ["add_1:out0_1", "lstmunit:out2"]],
"param_map":{
},
"blob_map": {
},

"acu_inter_flow": [],
"priority_tip": 0,
"extension": [],
"pre_condition": None,
"src_ops_main_version": None,
"src_ops_minior_version": [1, -1]}
# ruler_list.append(r_lstm)

r_conv_pool = {
    "ruler_name": "r_conv_pooling",
    "src_ops_alias": ["convolution", "pooling"],
    "src_inter_flow": [["convolution:out0", "pooling:in0"]],
    "src_in_anchor": [["I:out0", "convolution:in0"]],
    "src_out_tensor": ["pooling:out0"],
    "acu_lys_alias": ["convolutionrelupooling"],
    "src_acu_in_tensor_map": [["I:out0", "convolutionrelupooling:in0"]],
    "src_acu_out_tensor_map": [["pooling:out0", "convolutionrelupooling:out0"]],
    "param_map": {
        "convolutionrelupooling": {
            'weights': ['INT', 'CODE', "self.attr_pick(node['convolution'], 'weights')"],
            'padding': ['STRING', 'CODE', "self.attr_pick(node['convolution'], 'padding')"],
            'bias': ['BOOL', 'CODE', "self.is_exist_params(node['convolution'], 'bias')"],
            'group_number': ['INT', 'CODE', "self.attr_pick(node['convolution'], 'group_number')"],
            'ksize_h': ['INT', 'CODE', "self.attr_pick(node['convolution'], 'ksize_h')"],
            'ksize_w': ['INT', 'CODE', "self.attr_pick(node['convolution'], 'ksize_w')"],
            'stride_h': ['INT', 'CODE', "self.attr_pick(node['convolution'], 'stride_h')"],
            'stride_w': ['INT', 'CODE', "self.attr_pick(node['convolution'], 'stride_w')"],
            'pad_h': ['INT', 'CODE', "self.attr_pick(node['convolution'], 'pad_h')"],
            'pad_w': ['INT', 'CODE', "self.attr_pick(node['convolution'], 'pad_w')"],
            'dilation': ['INTS', 'CODE', "self.attr_pick(node['convolution'], 'dilation')"],
            'pad_method': ['STRING', 'CODE', "self.attr_pick(node['convolution'], 'pad_method')"],
            'pad': ['INTS', 'CODE', "self.attr_pick(node['convolution'], 'pad')"],
            'enable_relu': ['BOOL', 'VALUE', False],
            'pooling_size': ['INT', 'CODE', "self.attr_pick(node['pooling'], 'ksize_h')"],
            'pooling_stride': ['INT', 'CODE', "self.attr_pick(node['pooling'], 'stride_h')"],
            'pooling_pad': ['INTS', 'CODE', "self.attr_pick(node['pooling'], 'pad')"],
        }
    },
    "blob_map": {"convolutionrelupooling": {'weight': ['CODE', "self.get_value_attr(node['convolution'],"
                                                               "'weight')"],
                                            'bias': ['CODE', "self.get_value_attr(node['convolution'],"
                                                             "'bias')"]}},
    "acu_inter_flow": [],
    "priority_tip": 0,
    "pre_condition": None,
    "extension": [
        ["CODE",
         "self.qnt_out_tensor(acu_ly['convolutionrelupooling'], tensor['pooling:out0'])"],
    ],
    "src_ops_main_version": None,
    "src_ops_minior_version": [1, -1]
}
# ruler_list.append(r_conv_pool)

def gen_acuity_ruler(dst_path):
    # print(json.dumps(ruler_list))
    dst_path = os.path.join(dst_path, 'ac_ruler_db.json')

    with open(dst_path, 'w+') as f:
        json.dump(ruler_list, f, indent=1)

    # To Verify ruler follow synatx
    with open(dst_path, 'r') as f:
        x_val = json.load(f)
def main():
    gen_acuity_ruler(sys.argv[1])

if  __name__ == '__main__':
    main()