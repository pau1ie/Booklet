"""
Tests for the matrix module
"""
import unittest
from booklet.utils import matrix

class TestMatrixMethods(unittest.TestCase):
    "Test the matrix module"

    def test_matrix_split_object_invalid(self):
        "Errors if object isn't iterable."
        with self.assertRaises(TypeError):
            matrix.split_list(1,1)

    def test_matrix_split_shape_invalid(self):
        "Test an invalid matrix shape"
        list1 = [1,2,3,4,5]
        with self.assertRaises(ValueError):
            matrix.split_list(list1, 2)

    def test_matrix_split_shape_length(self):
        "Split by length test"
        list1=[1,2,3,4,5,6]
        n=3
        m=len(list1)/n
        list2=matrix.split_list(list1,n)
        self.assertEqual(len(list2),m)
        self.assertEqual(len(list2[0]), n)

    def test_matrix_split_shape_width(self):
        "Split by width test"
        list1=[1,2,3,4,5,6]
        n=3
        m=len(list1)/n
        list2=matrix.split_list(list1,n,'n')
        self.assertEqual(len(list2),n)
        self.assertEqual(len(list2[0]),m)

    def test_matrix_transpose(self):
        "Transpose test"
        list1=[[1,2],[3,4],[5,6]]
        x=len(list1)
        y=len(list1[0])
        list2=matrix.transpose(list1)
        for i in range(x):
            for j in range(y):
                self.assertEqual(list1[i][j], list2[j][i])

    def test_matrix_flip(self):
        "flip test"
        list1=[[1,2],[3,4],[5,6]]
        x=len(list1)
        y=len(list1[0])
        list2=matrix.flip(list1)
        for i in range(x):
            for j in range(y):
                #print(f"i {i}, j{j}")
                self.assertEqual(list1[i][j], list2[x-i-1][j])

    def test_matrix_reshape_wrong_shape(self):
        "Reshape wrong shape"
        list1=[1,2,3,4,5,6]
        with self.assertRaises(ValueError):
            matrix.reshape(list1,[4,5])

    def test_matrix_reshape_right_shape(self):
        "Reshape correct shape"
        list1=[1,2,3,4,5,6]
        shape=[2,3]
        list2 = matrix.reshape(list1,shape)
        self.assertEqual(shape[0],len(list2))
        # Could maybe check all rows. Just the first for now.
        self.assertEqual(shape[2],len(list2[0]))
