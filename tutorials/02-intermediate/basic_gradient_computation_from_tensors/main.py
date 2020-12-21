import torch
from torch.autograd import Variable

''' Compute basic gradients from the sample tensors using PyTorch

First some basics of Pytorch terminology

Autograd: This class is an engine to calculate derivatives (Jacobian-vector product to be more precise). It records a graph of all the operations performed on a gradient enabled tensor and creates an acyclic graph called the dynamic computational graph. The leaves of this graph are input tensors and the roots are output tensors. Gradients are calculated by tracing the graph from the root to the leaf and multiplying every gradient in the way using the chain rule.

A Variable class wraps a tensor. You can access this tensor by calling .data attribute of a Variable.

The Variable also stores the gradient of a scalar quantity (say, loss) with respect to the parameter it holds. This gradient can be accessed by calling the .grad attribute. This is basically the gradient computed up to this particular node, and the gradient of the every subsequent node, can be computed by multiplying the edge weight with the gradient computed at the node just before it.

The third attribute a Variable holds is a grad_fn, a Function object which created the variable.

Variable: The Variable, just like a Tensor is a class that is used to hold data. It differs, however, in the way it’s meant to be used. Variables are specifically tailored to hold values which change during training of a neural network, i.e. the learnable paramaters of our network. Tensors on the other hand are used to store values that are not to be learned. For example, a Tensor maybe used to store the values of the loss generated by each example.

Every variable object has several members one of them is grad:

grad: grad holds the value of gradient. If requires_grad is False it will hold a None value. Even if requires_grad is True, it will hold a None value unless .backward() function is called from some other node. For example, if you call out.backward() for some variable out that involved x in its calculations then x.grad will hold ∂out/∂x.

Backward() function Backward is the function which actually calculates the gradient by passing it’s argument (1x1 unit tensor by default) through the backward graph all the way up to every leaf node traceable from the calling root tensor. The calculated gradients are then stored in .grad of every leaf node. Remember, the backward graph is already made dynamically during the forward pass. Backward function only calculates the gradient using the already made graph and stores them in leaf nodes. '''


def forward(x):
    return x * w


w = Variable(torch.Tensor([1.0]), requires_grad=True)
# On setting .requires_grad = True they start forming a backward graph
# that tracks every operation applied on them to calculate the gradients
# using something called a dynamic computation graph (DCG)
# When you finish your computation you can call .backward() and have
# all the gradients computed automatically. The gradient for this tensor
# will be accumulated into .grad attribute.

# Now create an array of data.
# By PyTorch’s design, gradients can only be calculated
# for floating point tensors which is why I’ve created a float type
# array before making it a gradient enabled PyTorch tensor
x_data = [11.0, 22.0, 33.0]
y_data = [21.0, 14.0, 64.0]


def loss_function(x, y):
    y_pred = forward(x)
    return (y_pred - y) * (y_pred - y)


# Now running the training loop
for epoch in range(10):
    for x_val, y_val in zip(x_data, y_data):
        l = loss_function(x_val, y_val)
        l.backward()
        print("\tgrad: ", x_val, y_val, w.grad.data[0])
        w.data = w.data - 0.01 * w.grad

        # Manually set the gradient to zero after updating weights
        w.grad.data.zero_()

        print('progress: ', epoch, l.data[0])
