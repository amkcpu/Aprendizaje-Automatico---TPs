import pandas as pd
import numpy as np
from ml_tps.utils.distance_utils import euclidean_distance


def initialize_centroids(X: pd.DataFrame, k: int):
    """Randomly picks k examples from data set as centroids."""
    indexes = np.arange(len(X))
    np.random.shuffle(indexes)
    indexes = list(indexes)
    centroids = pd.DataFrame([X.iloc[i] for i in indexes[:k]], index=range(1, k+1))
    return centroids


def assign_centroids(X: pd.DataFrame, centroids: pd.DataFrame):
    """Assigns the nearest centroid to each training example."""
    X_assigned = X.copy()

    for idx, row in X.iterrows():
        distances = {i: euclidean_distance(row, r) for i, r in centroids.iterrows()}    # calc distance to each centroid
        closest_centroid = min(distances, key=distances.get)    # assign training example to closest centroid
        X_assigned.at[idx, "Centroid"] = closest_centroid

    return X_assigned


def move_centroids(X_assigned: pd.DataFrame, centroids: pd.DataFrame):
    """Moves the centroids to the mean of their corresponding examples."""
    for idx, row in centroids.iterrows():
        assigned_rows = X_assigned[X_assigned["Centroid"] == idx]
        centroids.at[idx, :] = assigned_rows.drop("Centroid", axis=1).mean()

    return centroids


class KMeans:

    def __init__(self, initial_centroids: pd.DataFrame = None):
        self.centroids = initial_centroids

    def fit(self, X: pd.DataFrame, k: int, iters: int = 1000, tol: float = 0.001, initial_centroids: pd.DataFrame = None):
        """Clusters a given data set into k clusters using the K-Means algorithm.

        :param X: Data set on which to perform clustering.
        :param k: Number of clusters to be found.
        :param iters: Maximum number of iterations before clustering is stopped.
        :param tol: Stop criteria for clustering. If the clustering error falls below the tolerance, clustering is stopped.
        :param initial_centroids: If so wished, the starting centroids can be passed.
        """
        if initial_centroids is not None:
            if not len(initial_centroids.columns) == len(X.columns):
                raise ValueError("The centroids that were passed (initial_centroids) have a different dimension ({0}) "
                                 "than the data set ({1}).".format(len(initial_centroids.columns), len(X.columns)))
            self.centroids = initial_centroids
        elif self.centroids is not None:
            if not len(self.centroids.columns) == len(X.columns):
                raise ValueError("Already assigned centroids have a different dimension ({0}) "
                                 "than the data set that was passed ({1}).".format(len(self.centroids.columns), len(X.columns)))
        else:
            self.centroids = initialize_centroids(X, k)

        X_assigned = assign_centroids(X, self.centroids)
        error = self.cost(X_assigned)
        it = 0
        while it < iters and error > tol:
            centroids_prev = self.centroids.copy()
            self.centroids = move_centroids(X_assigned, self.centroids)
            X_assigned = assign_centroids(X, self.centroids)

            error = self.cost(X_assigned)
            it += 1
            if self.centroids.equals(centroids_prev):    # break if centroids are stable
                print("Centroids stable. K-Means finished.")
                break

        print("Finished after {} iterations.".format(it))
        print("Converged with error (cost) = {}.".format(error))

    def predict(self, X: pd.DataFrame):
        if self.centroids is None:
            raise ValueError("Model has not been fitted yet (centroids = None).")

        predictions = list()
        for idx, row in X.iterrows():
            distances = {i: euclidean_distance(row, r) for i, r in self.centroids.iterrows()}
            predictions.append(min(distances, key=distances.get))

        return pd.Series(predictions, index=X.index)

    def cost(self, X_assigned) -> float:
        if self.centroids is None:
            raise ValueError("Model has not been fitted yet (centroids = None).")

        costs = list()
        for idx, row in self.centroids.iterrows():
            assigned_rows = X_assigned[X_assigned["Centroid"] == idx].drop("Centroid", axis=1)
            cost = sum([euclidean_distance(row, r) for i, r in assigned_rows.iterrows()])
            costs.append(cost)

        n = len(X_assigned)
        return sum(costs) / n
