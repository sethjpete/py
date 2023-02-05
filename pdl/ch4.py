# %%
import numpy as np
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
# %%
x,y = make_classification(n_samples = 1000, weights=(.9,.1))
# %%
x.shape
# %%
len(np.where(y == 0)[0])
# %%
len(np.where(y == 1)[0])
# %%



# EXAMPLE: PARTITIONING BY CLASS
# Maintains the class balance in the training, validation, and testing sets
# Guarantees proper ratio

# %%
#
# Create the dummy dataset, split into class 0 and class 1 collections, and 
# store the class 0 and class 1 collections in separate variables.
#
a,b = make_classification(n_samples = 10000, weights=(.9,.1))
idx = np.where(b == 0)[0]
x0 = a[idx,:]
y0 = b[idx]
idx = np.where(b == 1)[0]
x1 = a[idx,:]
y1 = b[idx]
idx, x0, y0, x1, y1
# %%
#
# Randomly shuffle the class 0 and class 1 collections,
#
idx = np.argsort(np.random.random(y0.shape))
y0 = y0[idx]
x0 = x0[idx]
idx = np.argsort(np.random.random(y1.shape))
y1 = y1[idx]
x1 = x1[idx]
idx, x0, y0, x1, y1 #shuffled feature and label vectors
# %%
#
# Extract 90% of the class 0 and class 1 collections for training
# Build training subset in xtrn and ytrn
# 
ntrn0 = int(0.9*x0.shape[0])
ntrn1 = int(0.9*x1.shape[0])
xtrn = np.zeros((int(ntrn0 + ntrn1),20))
ytrn = np.zeros(int(ntrn0 + ntrn1))
xtrn[:ntrn0] = x0[:ntrn0]
xtrn[ntrn0:] = x1[:ntrn1]
ytrn[:ntrn0] = y0[:ntrn0]
ytrn[ntrn0:] = y1[:ntrn1]
xtrn, ytrn
# %%
#
# Extract 5% of the class 0 and class 1 collections for validation
# Build validation subset in xval and yval
#
n0 = int(x0.shape[0] - ntrn0)
n1 = int(x1.shape[0] - ntrn1)
xval = np.zeros((int(n0/2 + n1/2),20))
yval = np.zeros(int(n0/2 + n1/2))
xval[:int(n0/2)] = x0[ntrn0:ntrn0+int(n0/2)]
xval[int(n0/2):] = x1[ntrn1:ntrn1+int(n1/2)]
yval[:int(n0/2)] = y0[ntrn0:ntrn0+int(n0/2)]
yval[int(n0/2):] = y1[ntrn1:ntrn1+int(n1/2)]
xval, yval
# %%
#
# Extract 5% of the class 0 and class 1 collections for testing
# Build testing subset in xtst and ytst
#
xtst = np.concatenate((x0[ntrn0+int(n0/2):],x1[ntrn1+int(n1/2):]))
ytst = np.concatenate((y0[ntrn0+int(n0/2):],y1[ntrn1+int(n1/2):]))
xtst, ytst
# %%







# %%
# 
# Random Sampling Approach
# Randomizing the first dataset, then extracting top 90, 5, 5
# 
# %%
# Randomize the dummy dataset into x and y
x,y = make_classification(n_samples=10000, weights=(.9, .1))
idx = np.argsort(np.random.random(y.shape[0]))
x = x[idx]
y = y[idx]
# %%
# Compute the number of samples in each set
ntrn = int(.9 * y.shape[0])
nval = int(0.05 * y.shape[0])
# %%
# Create the datasets
xtrn = x[:ntrn]
ytrn = y[:ntrn]
xval = x[ntrn : ntrn + nval]
yval = y[ntrn : ntrn + nval]
xtst = x[ntrn + nval : ]
ytst = y[ntrn + nval : ]
# %%




# %%
#
# Numpy summary statistics
#
f = [.34, 3.02, 4.35, 2.13, 2.76, 2.79, 4.82, 0.07, 3.99, 0.98, 2.39, 2.00, 1.78, 1.54, 2.32]
f = np.array(f)
print(f"mean = {f.mean():.2f}")
print(f"std = {f.std():.2f}")
print(f"s.e. = {f.std()/np.sqrt(f.shape[0]):.2f}")
print(f"median = {np.median(f):.2f}")
print(f"min = {f.min():.2f}")
print(f"max = {f.max():.2f}")
# %%
# Matplotlib histogram works with numpy arrays
plt.boxplot(f)
plt.show()
# %%
