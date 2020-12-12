print("===== testing translation =====")
import AffineWarping
affine_test_temp = [1,2,3,4,5,6,7,8,9]
affine_test_X = [[]]*9
for i in range(9): affine_test_X[i] = affine_test_temp
affine_test_Tw = [0,0]
AffineWarping.translation(affine_test_X, affine_test_Tw)
print()
affine_test_Tw = [1,4]
AffineWarping.translation(affine_test_X, affine_test_Tw)
print()
affine_test_Tw = [1,-4]
AffineWarping.translation(affine_test_X, affine_test_Tw)
print()
affine_test_Tw = [5,1]
AffineWarping.translation(affine_test_X, affine_test_Tw)
print()
affine_test_Tw = [-5,1]
AffineWarping.translation(affine_test_X, affine_test_Tw)
print("^^^^^ END of testing translation ^^^^^")
print()