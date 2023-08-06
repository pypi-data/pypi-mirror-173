
# dpkg


* dpkg is a package that collects functions frequently used in recommendation algorithms.

# apk : 


Computes the average precision at k. This function computes the average prescision at k between two lists of items.

Parameters
----------
* actual : list
> A list of elements that are to be predicted (order doesn't matter)
* predicted : list
> A list of predicted elements (order does matter)
* k : int, optional
> The maximum number of predicted elements

Returns
-------
* score : double The average precision at k over the input lists
