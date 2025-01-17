import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt


def pearson_correlation(x, y):
    """
    Calculate the Pearson correlation coefficient for two given columns of data.

    Inputs:
    - x: An array containing a column of m numeric values.
    - y: An array containing a column of m numeric values. 

    Returns:
    - The Pearson correlation coefficient between the two columns.    
    """
    # Ensure that x and y are numpy arrays
    x = np.array(x)
    y = np.array(y)
    
    # Calculate the means of x and y
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    # Calculate the numerator of the Pearson correlation coefficient
    numerator = np.sum((x - mean_x) * (y - mean_y))
    
    # Calculate the denominator of the Pearson correlation coefficient
    denominator = np.sqrt(np.sum((x - mean_x)**2) * np.sum((y - mean_y)**2))
    
    # Calculate the Pearson correlation coefficient
    result = numerator / denominator
    
    return result

def feature_selection(X, y, n_features=5):
    """
    Select the best features using pearson correlation.

    Input:
    - X: Input data (m instances over n features).
    - y: True labels (m instances).

    Returns:
    - best_features: list of best features (names - list of strings).  
    """

    y = np.array(y)
    X["date"] = pd.to_numeric(pd.to_datetime(X["date"]))
    # Initialize an empty list to store the feature names and their correlation coefficients
    correlations = []
    
    # Iterate over each feature in the dataframe
    for feature in X.columns:
        corr = pearson_correlation(X[feature], y)
        correlations.append((feature, abs(corr)))
    
    # Sort the features by the absolute value of their correlation coefficient in descending order
    correlations.sort(key=lambda x: x[1], reverse=True)
    
    # Select the top n_features
    best_features = [feature for feature, _ in correlations[:n_features]]
    
    return best_features

class LogisticRegressionGD(object):
    """
    Logistic Regression Classifier using gradient descent.

    Parameters
    ------------
    eta : float
      Learning rate (between 0.0 and 1.0)
    n_iter : int
      Passes over the training dataset.
    eps : float
      minimal change in the cost to declare convergence
    random_state : int
      Random number generator seed for random weight
      initialization.
    """

    def __init__(self, eta=0.00005, n_iter=10000, eps=0.000001, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.eps = eps
        self.random_state = random_state

        # model parameters
        self.theta = None

        # iterations history
        self.Js = []
        self.thetas = []

    def fit(self, X, y):
        """
        Fit training data (the learning phase).
        Update the theta vector in each iteration using gradient descent.
        Store the theta vector in self.thetas.
        Stop the function when the difference between the previous cost and the current is less than eps
        or when you reach n_iter.
        The learned parameters must be saved in self.theta.
        This function has no return value.

        Parameters
        ----------
        X : {array-like}, shape = [n_examples, n_features]
          Training vectors, where n_examples is the number of examples and
          n_features is the number of features.
        y : array-like, shape = [n_examples]
          Target values.

        """
        # set random seed
        np.random.seed(self.random_state)
        X = self.apply_bias_trick(X)
        self.theta = np.random.random(X.shape[1])
        
        for i in range(self.n_iter):
          sigmoid = self.sigmoid(X.dot(self.theta))
          gradient = self.eta * (X.T.dot(sigmoid - y))
          self.theta = self.theta - gradient
          self.thetas.append(self.theta)
          self.Js.append(self.cost_function(sigmoid, y))
          
          if i > 1 and (self.Js[-2] - self.Js[-1]) < self.eps:
            break
          
    def predict(self, X):
        """
        Return the predicted class labels for a given instance.
        Parameters
        ----------
        X : {array-like}, shape = [n_examples, n_features]
        """
        X = self.apply_bias_trick(X)
        h_x = self.sigmoid(X.dot(self.theta))
        preds = np.where(h_x >= 0.5, 1,0)
        
        return preds
    
    def sigmoid(self, X):
        return 1 / (1 + np.exp(-X))
    
    def cost_function(self, h, y):
        m = h.shape[0]
        
        return (y.dot(np.log(h)) + (1-y).dot(np.log(1-h))) / -m

    def apply_bias_trick(self, X):
      """
      Applies the bias trick to the input data.

      Input:
      - X: Input data (m instances over n features).

      Returns:
      - X: Input data with an additional column of ones in the
          zeroth position (m instances over n+1 features).
      """
      ones_matrix = np.ones(X.shape[0]) # create a vector of ones
      
      return np.column_stack((ones_matrix, X))
    
def cross_validation(X, y, folds, algo, random_state):
    """
    This function performs cross validation as seen in class.

    1. shuffle the data and creates folds
    2. train the model on each fold
    3. calculate aggregated metrics

    Parameters
    ----------
    X : {array-like}, shape = [n_examples, n_features]
      Training vectors, where n_examples is the number of examples and
      n_features is the number of features.
    y : array-like, shape = [n_examples]
      Target values.
    folds : number of folds (int)
    algo : an object of the classification algorithm
    random_state : int
      Random number generator seed for random weight
      initialization.

    Returns the cross validation accuracy.
    """

    cv_accuracy = 0

    # set random seed
    np.random.seed(random_state)
    shuffled_indices = np.random.permutation(X.shape[0])
    X_shuffled = X[shuffled_indices]
    y_shuffled = y[shuffled_indices]
    num_of_elements = X.shape[0] // folds
    elements_lst = list(range(X.shape[0]))
    for i in range(1, folds + 1):
      start_threshhold = (i - 1) * num_of_elements
      end_threshhold = i * num_of_elements
      test_list = elements_lst[start_threshhold:end_threshhold]
      X_train = np.delete(X_shuffled, test_list, axis = 0)
      X_test = X_shuffled[test_list]
      y_train = np.delete(y_shuffled, test_list, axis = 0)
      y_test = y_shuffled[test_list]
      algo.fit(X_train, y_train)
      test_predict = algo.predict(X_test)
      fold_accuracy = np.mean(test_predict == y_test)
      cv_accuracy += fold_accuracy
      
    return cv_accuracy / folds

    # set random seed
    np.random.seed(random_state)

    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return cv_accuracy

def norm_pdf(data, mu, sigma):
    """
    Calculate normal desnity function for a given data,
    mean and standrad deviation.
 
    Input:
    - x: A value we want to compute the distribution for.
    - mu: The mean value of the distribution.
    - sigma:  The standard deviation of the distribution.
 
    Returns the normal distribution pdf according to the given mu and sigma for the given x.    
    """
    p = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(data - mu)**2 /(2 * (sigma**2)))
    
    return p

class EM(object):
    """
    Naive Bayes Classifier using Gauusian Mixture Model (EM) for calculating the likelihood.

    Parameters
    ------------
    k : int
      Number of gaussians in each dimension
    n_iter : int
      Passes over the training dataset in the EM proccess
    eps: float
      minimal change in the cost to declare convergence
    random_state : int
      Random number generator seed for random params initialization.
    """

    def __init__(self, k=1, n_iter=1000, eps=0.01, random_state=1991):
        self.k = k
        self.n_iter = n_iter
        self.eps = eps
        self.random_state = random_state

        np.random.seed(self.random_state)

        self.responsibilities = None
        self.weights = None
        self.mus = None
        self.sigmas = None
        self.costs = []

    # initial guesses for parameters
    def init_params(self, data):
        """
        Initialize distribution params
        """
        self.weights = np.ones(self.k) / self.k

        # initialize mus by selecting random data points
        random_indices = np.random.choice(len(data), self.k, replace=False)
        self.mus = data[random_indices]

        self.sigmas = np.full(self.k, np.std(data))

    def expectation(self, data):
        """
        E step - This function should calculate and update the responsibilities
        """        
        self.responsibilities =  np.zeros((data.shape[0],0))
        for i in range(self.k):
            likelihood_col_i = self.weights[i] * norm_pdf(data, self.mus[i], self.sigmas[i])
            self.responsibilities = np.c_[self.responsibilities, likelihood_col_i]

        row_sums = self.responsibilities.sum(axis=1)
        self.responsibilities = self.responsibilities / row_sums[:, np.newaxis]

    def maximization(self, data):
        """
        M step - This function should calculate and update the distribution params
        """
        self.weights = np.mean(self.responsibilities, axis = 0)
        self.mus = (1 / (data.shape[0] * self.weights)) * (self.responsibilities.T.dot(data).flatten())
        for i in range(self.k):
            self.sigmas[i] = self.responsibilities.T[i].dot((data - self.mus[i])**2)
            
        self.sigmas = np.sqrt((1 / (data.shape[0] * self.weights)) * self.sigmas)

    def fit(self, data):
        """
        Fit training data (the learning phase).
        Use init_params and then expectation and maximization function in order to find params
        for the distribution.
        Store the params in attributes of the EM object.
        Stop the function when the difference between the previous cost and the current is less than eps
        or when you reach n_iter.
        """        
        self.init_params(data)
        for i in range(self.n_iter):  
          self.expectation(data)
          self.maximization(data)
          cost=0
          for d in range(data.shape[0]):
              cost -= np.log2(gmm_pdf(data[d], self.weights,self.mus, self.sigmas))
              pass
            
          self.costs.append(cost)          
          if i>1 and (self.costs[-2] - self.costs[-1]) < self.eps:
              break 
          
    def get_dist_params(self):
        return self.weights, self.mus, self.sigmas

def gmm_pdf(data, weights, mus, sigmas):
    """
    Calculate gmm desnity function for a given data,
    mean and standrad deviation.
 
    Input:
    - data: A value we want to compute the distribution for.
    - weights: The weights for the GMM
    - mus: The mean values of the GMM.
    - sigmas:  The standard deviation of the GMM.
 
    Returns the GMM distribution pdf according to the given mus, sigmas and weights
    for the given data.    
    """
    k = len(weights)
    pdf = sum(weights[j] * norm_pdf(data, mus[j], sigmas[j]) for j in range(k))
    
    return pdf

class NaiveBayesGaussian(object):
    """
    Naive Bayes Classifier using Gaussian Mixture Model (EM) for calculating the likelihood.

    Parameters
    ------------
    k : int
      Number of gaussians in each dimension
    random_state : int
      Random number generator seed for random params initialization.
    """

    def __init__(self, k=1, random_state=1991):
        self.k = k
        self.random_state = random_state
        self.prior = {}
        self.dist_params = {}
        
    def fit(self, X, y):
        """
        Fit training data.

        Parameters
        ----------
        X : array-like, shape = [n_examples, n_features]
          Training vectors, where n_examples is the number of examples and
          n_features is the number of features.
        y : array-like, shape = [n_examples]
          Target values.
        """        
        for data_class in np.unique(y):
          self.dist_params[data_class] = []
          sub_data =  X[y == data_class]
          self.prior[data_class] = sub_data.shape[0] / X.shape[0]
          for j in range(sub_data.shape[1]):
              em = EM(self.k, random_state = self.random_state)
              em.fit(sub_data[:,j])
              self.dist_params[data_class].append(em.get_dist_params())

    def predict(self, X):
        """
        Return the predicted class labels for a given instance.
        Parameters
        ----------
        X : {array-like}, shape = [n_examples, n_features]
        """
        postiriors_matrix = np.zeros((X.shape[0], 0))
        for data_class in self.prior.keys():
            column_posterior = np.ones(X.shape[0])
            for j in range(X.shape[1]):
              column_posterior *= gmm_pdf(X[:,j], *self.dist_params[data_class][j])
            column_posterior *= self.prior[data_class]
            column_posterior = column_posterior.reshape((-1,1))
            postiriors_matrix = np.hstack((postiriors_matrix, column_posterior))
        
        preds = np.argmax(postiriors_matrix,axis=1)

        return np.array(preds)

def model_evaluation(x_train, y_train, x_test, y_test, k, best_eta, best_eps):
    ''' 
    Read the full description of this function in the notebook.

    You should use visualization for self debugging using the provided
    visualization functions in the notebook.
    Make sure you return the accuracies according to the return dict.

    Parameters
    ----------
    x_train : array-like, shape = [n_train_examples, n_features]
      Training vectors, where n_examples is the number of examples and
      n_features is the number of features.
    y_train : array-like, shape = [n_train_examples]
      Target values.
    x_test : array-like, shape = [n_test_examples, n_features]
      Training vectors, where n_examples is the number of examples and
      n_features is the number of features.
    y_test : array-like, shape = [n_test_examples]
      Target values.
    k : Number of gaussians in each dimension
    best_eta : best eta from cv
    best_eps : best eta from cv
    ''' 

    lor_train_acc = None
    lor_test_acc = None
    bayes_train_acc = None
    bayes_test_acc = None
    
    lor = LogisticRegressionGD(eta= best_eta, eps = best_eps)
    lor.fit(x_train, y_train)
    lor_train_acc = compute_accuracy(lor.predict(x_train), y_train)
    lor_test_acc = compute_accuracy(lor.predict(x_test), y_test)

    bayes = NaiveBayesGaussian(k)
    bayes.fit(x_train, y_train)
    bayes_train_acc = compute_accuracy(bayes.predict(x_train),y_train)
    bayes_test_acc = compute_accuracy(bayes.predict(x_test),y_test)

    return {'lor_train_acc': lor_train_acc,
            'lor_test_acc': lor_test_acc,
            'bayes_train_acc': bayes_train_acc,
            'bayes_test_acc': bayes_test_acc}

def compute_accuracy(preds_vector, actual_classes):
    return np.mean(preds_vector == actual_classes)

def generate_datasets():
    from scipy.stats import multivariate_normal
    '''
    This function should have no input.
    It should generate the two dataset as described in the jupyter notebook,
    and return them according to the provided return dict.
    '''
    dataset_a_features = None
    dataset_a_labels = None
    dataset_b_features = None
    dataset_b_labels = None
    
    gaussian1_class0 = multivariate_normal([10,0,0], 2*np.eye(3)).rvs(500)
    gaussian2_class0 = multivariate_normal([-15,2,0], np.eye(3)).rvs(500)

    gaussian1_class1 = multivariate_normal([0,-4,0], 3*np.eye(3)).rvs(500)
    gaussian2_class1 = multivariate_normal([5,6,0], 1.5*np.eye(3)).rvs(500)

    dataset_a_features = np.vstack([gaussian1_class0,gaussian2_class0,gaussian1_class1,gaussian2_class1])
    dataset_a_labels = np.hstack([np.zeros(1000),np.ones(1000)])

    gaussian1 = multivariate_normal([1.5,1.5,0], [[1,0.8,0.8],
                                             [0.8,1,0.8],
                                             [0.8,0.8,1]]).rvs(1000)
    gaussian2 = multivariate_normal([0,0,0], [[1,0.8,0.8],
                                              [0.8,1,0.8],
                                              [0.8,0.8,1]]).rvs(1000)

    dataset_b_features = np.vstack([gaussian1,gaussian2])
    dataset_b_labels = np.hstack([np.zeros(1000),np.ones(1000)])

    return{'dataset_a_features': dataset_a_features,
           'dataset_a_labels': dataset_a_labels,
           'dataset_b_features': dataset_b_features,
           'dataset_b_labels': dataset_b_labels
           }

# Function for ploting the decision boundaries of a model
def plot_decision_regions(X, y, classifier, resolution=0.01, title=""):

    # setup marker generator and color map
    markers = ('.', '.')
    colors = ['blue', 'red']
    cmap = ListedColormap(colors[:len(np.unique(y))])
    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.title(title)
        plt.scatter(x=X[y == cl, 0], 
                    y=X[y == cl, 1],
                    alpha=0.8, 
                    c=colors[idx],
                    marker=markers[idx], 
                    label=cl, 
                    edgecolor='black')
    plt.show()